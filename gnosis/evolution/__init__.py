"""Bounded, non-canonical evolution experiments."""
from .sandbox import SandboxBudget, SandboxExecution, SandboxResult, run_sandbox
from .evaluator import ComparativeEvaluation, EvaluationResult, evaluate_comparative, evaluate_observation
from .promotion import PromotionCandidate, PromotionGate, evaluate_promotion_gate, make_promotion_candidate
from .replay import ReplayResult, replay_evidence, replay_identity
from .transaction import EvolutionTransactionResult, persist_evolution_transaction

from .gap import GapHypothesis, GapDetector
from .capability import CapabilityHypothesis, CapabilitySynthesizer
from .provenance import EvidenceProvenance, ProvenanceCrossCheck, build_provenance, canonical_digest, crosscheck_provenance, execution_id, verify_evidence_digest
from .runtime import RuntimeSliceResult, capability_candidate, run_runtime_slice

__all__ = ["GapHypothesis","GapDetector","CapabilityHypothesis","CapabilitySynthesizer","SandboxBudget","SandboxExecution","SandboxResult","run_sandbox","EvaluationResult","evaluate_observation","PromotionCandidate","PromotionGate","ReplayResult","replay_evidence","replay_identity","EvolutionTransactionResult","persist_evolution_transaction","evaluate_promotion_gate","make_promotion_candidate","RuntimeSliceResult","capability_candidate","run_runtime_slice"]
