"""Bounded, non-canonical evolution experiments."""
from .sandbox import SandboxBudget, SandboxExecution, SandboxResult, run_sandbox
from .evaluator import EvaluationResult, evaluate_observation
from .promotion import PromotionCandidate, make_promotion_candidate
from .provenance import EvidenceProvenance, build_provenance, canonical_digest, execution_id, verify_evidence_digest
__all__ = ["SandboxBudget","SandboxExecution","SandboxResult","run_sandbox","EvaluationResult","evaluate_observation","PromotionCandidate","make_promotion_candidate"]
