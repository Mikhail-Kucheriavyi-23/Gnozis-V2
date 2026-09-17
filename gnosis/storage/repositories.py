from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any

from gnosis.core import Candidate, Relation, State, TestResult, TransitionRecord
from gnosis.instances.instance import Instance, InstanceStatus
from .database import GENESIS_HASH, transaction

class StorageCorruptionError(ValueError): pass
class SecretMaterialError(ValueError): pass
_SECRET_KEYS = re.compile(r"(password|passwd|token|api[_-]?key|private[_-]?key|secret|authorization|credential)", re.I)
_SECRET_VALUES = re.compile(r"(-----BEGIN .*PRIVATE KEY-----|sk-[A-Za-z0-9_-]{16,}|Bearer\s+[A-Za-z0-9._-]{16,})")
def utc_now() -> str: return datetime.now(timezone.utc).isoformat()
def _plain(value: Any) -> Any:
    if isinstance(value, Mapping): return {str(k): _plain(v) for k,v in value.items()}
    if isinstance(value, (list, tuple)): return [_plain(v) for v in value]
    if isinstance(value, (set, frozenset)): return sorted((_plain(v) for v in value), key=repr)
    if value is None or isinstance(value, (str, int, float, bool)): return value
    raise TypeError(f"unsupported persistence value: {type(value).__name__}")
def _reject_secrets(value: Any, path: str = "payload") -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            if _SECRET_KEYS.search(str(key)): raise SecretMaterialError(f"secret-bearing field rejected: {path}.{key}")
            _reject_secrets(item, f"{path}.{key}")
    elif isinstance(value, (list, tuple, set, frozenset)):
        for index, item in enumerate(value): _reject_secrets(item, f"{path}[{index}]")
    elif isinstance(value, str) and _SECRET_VALUES.search(value): raise SecretMaterialError(f"secret-like value rejected at {path}")
def canonical_json(value: Any) -> str:
    _reject_secrets(value); return json.dumps(_plain(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
def state_payload(state: State) -> str: return canonical_json({"elements": state.elements, "version": state.version})
def _decode_payload(payload: str) -> dict[str, Any]:
    try: value=json.loads(payload)
    except (TypeError,json.JSONDecodeError) as exc: raise StorageCorruptionError("malformed state JSON") from exc
    if not isinstance(value,dict) or set(value)!={"elements","version"} or not isinstance(value["version"],int): raise StorageCorruptionError("invalid state payload structure")
    return value
def save_state(conn: sqlite3.Connection,state: State,*,created_at: str|None=None)->None:
    created_at=created_at or utc_now(); payload=state_payload(state); existing=conn.execute("SELECT version,payload FROM states WHERE state_id=?",(state.state_id,)).fetchone()
    if existing:
        if existing[0]!=state.version or existing[1]!=payload: raise StorageCorruptionError("state_id collision or tampering")
        return
    conn.execute("INSERT INTO states(state_id,version,payload,created_at) VALUES(?,?,?,?)",(state.state_id,state.version,payload,created_at))
    for order,relation in enumerate(state.relations):
        value=None if relation.value is None else canonical_json(relation.value); conn.execute("INSERT INTO relations(state_id,relation_order,relation_id,source_id,target_id,relation_type,value,created_at) VALUES(?,?,?,?,?,?,?,?)",(state.state_id,order,relation.relation_id,relation.source,relation.target,relation.relation_type,value,created_at))
def load_state(conn: sqlite3.Connection,state_id: str)->State:
    row=conn.execute("SELECT version,payload FROM states WHERE state_id=?",(state_id,)).fetchone()
    if row is None: raise StorageCorruptionError(f"state not found: {state_id}")
    payload=_decode_payload(row[1]); relations=[]
    for rel in conn.execute("SELECT relation_id,source_id,target_id,relation_type,value FROM relations WHERE state_id=? ORDER BY relation_order",(state_id,)):
        try: value=None if rel[4] is None else json.loads(rel[4])
        except json.JSONDecodeError as exc: raise StorageCorruptionError("malformed relation JSON") from exc
        relation=Relation(rel[1],rel[2],rel[3],value)
        if relation.relation_id!=rel[0]: raise StorageCorruptionError(f"relation hash mismatch: {rel[0]}")
        relations.append(relation)
    state=State(elements=payload["elements"],relations=relations,version=payload["version"])
    if state.state_id!=state_id: raise StorageCorruptionError(f"state hash mismatch: {state_id}")
    return state
def save_candidate(conn: sqlite3.Connection,candidate: Candidate,*,created_at: str|None=None)->None:
    created_at=created_at or utc_now(); load_state(conn,candidate.parent_state_id); save_state(conn,candidate.proposed_state,created_at=created_at); row=conn.execute("SELECT parent_state_id,candidate_state_id,origin,seed FROM candidates WHERE candidate_id=?",(candidate.candidate_id,)).fetchone(); expected=(candidate.parent_state_id,candidate.proposed_state.state_id,candidate.origin,candidate.seed)
    if row and tuple(row)!=expected: raise StorageCorruptionError("candidate_id collision")
    if not row: conn.execute("INSERT INTO candidates(candidate_id,parent_state_id,candidate_state_id,origin,seed,created_at) VALUES(?,?,?,?,?,?)",(candidate.candidate_id,*expected,created_at))
def load_candidate(conn: sqlite3.Connection,candidate_id: str)->Candidate:
    row=conn.execute("SELECT parent_state_id,candidate_state_id,origin,seed FROM candidates WHERE candidate_id=?",(candidate_id,)).fetchone()
    if row is None: raise StorageCorruptionError(f"candidate not found: {candidate_id}")
    candidate=Candidate(row[0],load_state(conn,row[1]),row[2],row[3])
    if candidate.candidate_id!=candidate_id: raise StorageCorruptionError("candidate hash mismatch")
    return candidate
def transition_id(record: TransitionRecord)->str:
    raw=canonical_json({"candidate_id":record.candidate_id,"from":record.from_state_id,"to":record.to_state_id,"accepted":record.accepted,"reasons":record.test_result.reasons,"test_rule_id":record.test_rule_id}); return hashlib.sha256(raw.encode()).hexdigest()
def load_transition_records(conn: sqlite3.Connection,instance_id: str|None=None)->list[TransitionRecord]:
    query="SELECT candidate_id,from_state_id,to_state_id,accepted,reasons,test_rule_id FROM transitions"
    params: tuple[Any,...]=()
    if instance_id is not None: query += " WHERE instance_id=?"; params=(instance_id,)
    query += " ORDER BY created_at,transition_id"
    records=[]
    for row in conn.execute(query,params):
        try: reasons=tuple(json.loads(row[4]))
        except (TypeError,json.JSONDecodeError) as exc: raise StorageCorruptionError("malformed transition reasons") from exc
        result=TestResult(passed=bool(row[3]),reasons=reasons)
        records.append(TransitionRecord(from_state_id=row[1],to_state_id=row[2],candidate_id=row[0],test_result=result,accepted=bool(row[3]),reason=("committed" if row[3] else "rejected: "+"; ".join(reasons)),test_rule_id=row[5]))
    return records

def _audit_hash(event: dict[str,Any])->str: return hashlib.sha256(canonical_json(event).encode()).hexdigest()
def append_audit(conn: sqlite3.Connection,*,actor: str,action: str,resource: str,result: str,timestamp: str|None=None,event_key: str|None=None,transition_id_value: str|None=None)->str:
    timestamp=timestamp or utc_now(); key=event_key or hashlib.sha256(canonical_json({"actor":actor,"action":action,"resource":resource,"result":result}).encode()).hexdigest(); existing=conn.execute("SELECT event_hash,actor,action,resource,result,transition_id FROM audit_events WHERE event_id=?",(key,)).fetchone()
    if existing:
        if tuple(existing[1:])!=(actor,action,resource,result,transition_id_value): raise StorageCorruptionError("conflicting audit replay")
        return existing[0]
    last=conn.execute("SELECT sequence,event_hash FROM audit_events ORDER BY sequence DESC LIMIT 1").fetchone(); sequence=1 if last is None else int(last[0])+1; prev=GENESIS_HASH if last is None else last[1]; event={"event_id":key,"sequence":sequence,"transition_id":transition_id_value,"actor":actor,"action":action,"resource":resource,"result":result,"timestamp":timestamp,"prev_hash":prev}; event_hash=_audit_hash(event); conn.execute("INSERT INTO audit_events(event_id,sequence,transition_id,actor,action,resource,result,timestamp,prev_hash,event_hash) VALUES(?,?,?,?,?,?,?,?,?,?)",(key,sequence,transition_id_value,actor,action,resource,result,timestamp,prev,event_hash)); return event_hash
def verify_audit_chain(conn: sqlite3.Connection)->tuple[int,str]:
    previous=GENESIS_HASH; last=(0,previous)
    for row in conn.execute("SELECT event_id,sequence,transition_id,actor,action,resource,result,timestamp,prev_hash,event_hash FROM audit_events ORDER BY sequence"):
        if row[1]!=last[0]+1 or row[8]!=previous: raise StorageCorruptionError("audit sequence/link mismatch")
        event={"event_id":row[0],"sequence":row[1],"transition_id":row[2],"actor":row[3],"action":row[4],"resource":row[5],"result":row[6],"timestamp":row[7],"prev_hash":row[8]};
        if _audit_hash(event)!=row[9]: raise StorageCorruptionError(f"audit event hash mismatch: {row[0]}")
        previous=row[9]; last=(row[1],previous)
    return last

def save_instance(conn: sqlite3.Connection,instance: Instance,*,actor: str|None=None)->None:
    with transaction(conn):
        save_state(conn,instance.engine.state); b=instance.engine.budget; conn.execute("INSERT INTO instances(instance_id,parent_instance_id,owner_id,root_state_id,current_state_id,generation,status,budget_total,budget_spent,created_at) VALUES(?,?,?,?,?,?,?,?,?,?)",(instance.instance_id,instance.parent_instance_id,instance.owner_id,instance.engine.state.state_id,instance.engine.state.state_id,instance.generation,instance.status.value,b.total,b.spent,instance.created_at)); append_audit(conn,actor=actor or instance.owner_id,action="instance.create",resource=instance.instance_id,result="accepted",event_key=f"instance:{instance.instance_id}:create")
def load_instance(conn: sqlite3.Connection,instance_id: str)->Instance:
    row=conn.execute("SELECT instance_id,owner_id,root_state_id,current_state_id,parent_instance_id,generation,status,budget_total,budget_spent,created_at FROM instances WHERE instance_id=?",(instance_id,)).fetchone()
    if row is None: raise StorageCorruptionError(f"instance not found: {instance_id}")
    from gnosis.core import Budget,Engine
    budget=Budget(total=row[7],spent=row[8]); return Instance(row[0],row[1],Engine(load_state(conn,row[3]),budget=budget),row[4],row[5],InstanceStatus(row[6]),row[9])
def recover_instance(conn: sqlite3.Connection,instance_id: str)->Instance: verify_durable_graph(conn); return load_instance(conn,instance_id)
def verify_durable_graph(conn: sqlite3.Connection)->tuple[int,str]:
    chain=verify_audit_chain(conn)
    for row in conn.execute("SELECT instance_id,root_state_id,current_state_id,parent_instance_id,generation FROM instances"):
        load_state(conn,row[1]);
        if conn.execute("SELECT 1 FROM audit_events WHERE action='instance.create' AND resource=?",(row[0],)).fetchone() is None: raise StorageCorruptionError("instance lacks creation audit evidence")
        transitions=list(conn.execute("SELECT transition_id,candidate_id,from_state_id,to_state_id,accepted FROM transitions WHERE instance_id=? ORDER BY created_at,transition_id",(row[0],)))
        if row[3] is None and row[4]!=0: raise StorageCorruptionError("invalid root generation")
        if row[3] is not None:
            parent=conn.execute("SELECT generation FROM instances WHERE instance_id=?",(row[3],)).fetchone()
            if parent is None or row[4]!=parent[0]+1: raise StorageCorruptionError("invalid fork lineage")
        if not transitions and row[2]!=row[1]: raise StorageCorruptionError("current head lacks transition provenance")
        if transitions:
            accepted=[t for t in transitions if t[4]]
            if not accepted and row[2]!=row[1]: raise StorageCorruptionError("current head lacks transition provenance")
            if accepted and accepted[-1][3]!=row[2]: raise StorageCorruptionError("current head lacks accepted transition provenance")
            expected=row[1]
            for t in transitions:
                expected_tid = transition_id(load_transition_records(conn,row[0])[0]) if False else None
                cand=load_candidate(conn,t[1])
                if cand.parent_state_id!=t[2] or cand.proposed_state.state_id!=t[3]: raise StorageCorruptionError("transition/candidate mismatch")
                record=TransitionRecord(from_state_id=t[2],to_state_id=t[3],candidate_id=t[1],test_result=TestResult(passed=bool(t[4]),reasons=tuple(json.loads(conn.execute("SELECT reasons FROM transitions WHERE transition_id=?",(t[0],)).fetchone()[0]))),accepted=bool(t[4]),reason=("committed" if t[4] else "rejected"),test_rule_id=conn.execute("SELECT test_rule_id FROM transitions WHERE transition_id=?",(t[0],)).fetchone()[0])
                if transition_id(record)!=t[0]: raise StorageCorruptionError("transition identity mismatch")
                if t[4] and t[2]!=expected: raise StorageCorruptionError("broken accepted transition continuity")
                if t[4]: expected=t[3]
                if conn.execute("SELECT 1 FROM audit_events WHERE transition_id=? AND resource=?",(t[0],row[0])).fetchone() is None: raise StorageCorruptionError("transition lacks audit evidence")
    return chain

def persist_transition(conn: sqlite3.Connection,instance: Instance,candidate: Candidate,record: TransitionRecord,*,actor: str,failure_at: str|None=None)->None:
    def inject(point: str)->None:
        if failure_at==point: raise RuntimeError(f"injected failure at {point}")
    if candidate.parent_state_id!=record.from_state_id: raise ValueError("candidate parent does not match transition source")
    tid=transition_id(record); inject("before_begin")
    with transaction(conn):
        inject("after_begin"); db=load_instance(conn,instance.instance_id)
        if db.engine.state.state_id==record.to_state_id and conn.execute("SELECT 1 FROM transitions WHERE transition_id=?",(tid,)).fetchone(): return
        if db.engine.state.state_id!=record.from_state_id: raise ValueError("stale instance head")
        save_candidate(conn,candidate); inject("after_candidate")
        conn.execute("INSERT INTO transitions(transition_id,instance_id,candidate_id,from_state_id,to_state_id,accepted,reasons,test_rule_id,created_at) VALUES(?,?,?,?,?,?,?,?,?)",(tid,instance.instance_id,candidate.candidate_id,record.from_state_id,record.to_state_id,int(record.accepted),canonical_json(record.test_result.reasons),record.test_rule_id,utc_now())); inject("after_transition")
        append_audit(conn,actor=actor,action="transition.commit" if record.accepted else "transition.reject",resource=instance.instance_id,result="accepted" if record.accepted else "rejected",event_key=f"transition:{tid}",transition_id_value=tid); inject("after_audit")
        if record.accepted: conn.execute("UPDATE instances SET current_state_id=?,budget_total=?,budget_spent=? WHERE instance_id=?",(record.to_state_id,instance.engine.budget.total,instance.engine.budget.spent,instance.instance_id)); inject("after_head")
        inject("before_commit")
    inject("after_commit")
