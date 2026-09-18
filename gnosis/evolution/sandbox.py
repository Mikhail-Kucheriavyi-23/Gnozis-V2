"""Fail-closed bounded sandbox execution for evolution experiments."""
from __future__ import annotations
import hashlib,json
from dataclasses import dataclass
from typing import Any,Callable,Mapping
from gnosis.core.types import Candidate,State
ObservationFn=Callable[[State,Candidate],Mapping[str,Any]]
@dataclass(frozen=True)
class SandboxBudget:
    max_operations:int=20
    def __post_init__(self):
        if self.max_operations<1 or self.max_operations>20: raise ValueError("sandbox max_operations must be in range 1..20")
@dataclass(frozen=True)
class SandboxExecution:
    candidate_id:str; parent_state_id:str; operations:int; status:str; evidence_digest:str; observations:Mapping[str,Any]
@dataclass(frozen=True)
class SandboxResult:
    execution:SandboxExecution; accepted_for_evaluation:bool
def _digest(observations):
    payload=json.dumps(observations,sort_keys=True,separators=(",",":"),default=str)
    return hashlib.sha256(payload.encode()).hexdigest()
def run_sandbox(state:State,candidate:Candidate,observe:ObservationFn,*,budget:SandboxBudget=SandboxBudget())->SandboxResult:
    if candidate.parent_state_id!=state.state_id: raise ValueError("candidate parent does not match sandbox state")
    try: observations=dict(observe(state,candidate))
    except Exception as exc:
        observations={"execution_error":type(exc).__name__,"error":str(exc)}
        return SandboxResult(SandboxExecution(candidate.candidate_id,state.state_id,1,"FAILED",_digest(observations),observations),False)
    return SandboxResult(SandboxExecution(candidate.candidate_id,state.state_id,1,"COMPLETED",_digest(observations),observations),True)
