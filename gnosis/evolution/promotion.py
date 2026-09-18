"""Non-authoritative promotion candidates."""
from __future__ import annotations
import hashlib
from dataclasses import dataclass
@dataclass(frozen=True)
class PromotionCandidate:
    candidate_id:str; evidence_digest:str; evaluation_status:str; shadow_status:str; invariant_status:str; governance_decision:str; status:str="PROPOSED"
    @property
    def can_activate(self)->bool: return False
def make_promotion_candidate(*,candidate_id,evidence_digest,evaluation_status,shadow_status,invariant_status,governance_decision)->PromotionCandidate:
    if not candidate_id or not evidence_digest: raise ValueError("promotion candidate requires candidate_id and evidence_digest")
    raw="|".join((candidate_id,evidence_digest,evaluation_status,shadow_status,invariant_status,governance_decision))
    return PromotionCandidate("promotion:"+hashlib.sha256(raw.encode()).hexdigest()[:24],evidence_digest,evaluation_status,shadow_status,invariant_status,governance_decision)
