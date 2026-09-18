"""Fail-closed, resource-bounded sandbox execution for evolution experiments.

The sandbox is an evidence boundary, not a Core authority boundary. Execution is
performed in a child process with a wall-clock deadline; the parent process never
accepts a successful result after timeout or worker failure.
"""
from __future__ import annotations

import hashlib
import json
import multiprocessing
import queue
from dataclasses import dataclass
from typing import Any, Callable, Mapping

from gnosis.core.types import Candidate, State

ObservationFn = Callable[[State, Candidate], Mapping[str, Any]]


@dataclass(frozen=True)
class SandboxBudget:
    max_operations: int = 20
    timeout_seconds: float = 1.0

    def __post_init__(self) -> None:
        if not 1 <= self.max_operations <= 20:
            raise ValueError("sandbox max_operations must be in range 1..20")
        if self.timeout_seconds <= 0:
            raise ValueError("sandbox timeout_seconds must be positive")


@dataclass(frozen=True)
class SandboxExecution:
    candidate_id: str
    parent_state_id: str
    operations: int
    status: str
    evidence_digest: str
    observations: Mapping[str, Any]


@dataclass(frozen=True)
class SandboxResult:
    execution: SandboxExecution
    accepted_for_evaluation: bool


def _digest(observations: Mapping[str, Any]) -> str:
    payload = json.dumps(
        observations, sort_keys=True, separators=(",", ":"), default=str
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _worker(
    output: Any,
    state: State,
    candidate: Candidate,
    observe: ObservationFn,
) -> None:
    try:
        observations = dict(observe(state, candidate))
        output.put(("COMPLETED", observations))
    except Exception as exc:
        output.put(
            (
                "FAILED",
                {"execution_error": type(exc).__name__, "error": str(exc)},
            )
        )


def run_sandbox(
    state: State,
    candidate: Candidate,
    observe: ObservationFn,
    *,
    budget: SandboxBudget = SandboxBudget(),
) -> SandboxResult:
    """Run one bounded experiment and return evidence only.

    One worker invocation consumes one gas/operation. Timeout and worker failure
    are terminal for this execution. No Engine, persistence handle, or
    activation API crosses the sandbox boundary.
    """
    if candidate.parent_state_id != state.state_id:
        raise ValueError("candidate parent does not match sandbox state")

    if budget.max_operations < 1:
        raise ValueError("sandbox operation budget exhausted")

    ctx = multiprocessing.get_context("fork" if "fork" in multiprocessing.get_all_start_methods() else "spawn")
    output = ctx.Queue(maxsize=1)
    process = ctx.Process(target=_worker, args=(output, state, candidate, observe))
    process.start()
    process.join(budget.timeout_seconds)

    if process.is_alive():
        process.terminate()
        process.join()
        observations = {
            "execution_error": "ExecutionTimeout",
            "timeout_seconds": budget.timeout_seconds,
        }
        return SandboxResult(
            SandboxExecution(
                candidate.candidate_id,
                state.state_id,
                1,
                "TIMEOUT",
                _digest(observations),
                observations,
            ),
            False,
        )

    try:
        status, observations = output.get_nowait()
    except queue.Empty:
        status = "FAILED"
        observations = {
            "execution_error": "WorkerFailure",
            "exit_code": process.exitcode,
        }

    if status != "COMPLETED":
        return SandboxResult(
            SandboxExecution(
                candidate.candidate_id,
                state.state_id,
                1,
                "FAILED",
                _digest(observations),
                observations,
            ),
            False,
        )

    return SandboxResult(
        SandboxExecution(
            candidate.candidate_id,
            state.state_id,
            1,
            "COMPLETED",
            _digest(observations),
            observations,
        ),
        True,
    )
