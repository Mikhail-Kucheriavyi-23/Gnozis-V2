"""Build a deterministic, read-only project context snapshot.

This module deliberately does not execute tasks, mutate the repository, or grant
any authority. It assembles durable project documents plus repository identity
into one machine-readable structure for a newly connected product.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import subprocess
from typing import Any


@dataclass(frozen=True)
class ContextSnapshot:
    repository: str
    branch: str
    head: str
    source_documents: dict[str, str]
    active_phase: str
    active_task: str
    implementation_state: str
    verification_state: str
    acceptance_state: str
    next_permitted_action: str
    open_findings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _git(root: Path, *args: str) -> str:
    try:
        return subprocess.check_output(
            ["git", *args], cwd=root, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "UNKNOWN"


def _read(root: Path, relative: str) -> str:
    path = root / relative
    if not path.is_file():
        return "UNKNOWN"
    return path.read_text(encoding="utf-8")


def build_context_snapshot(root: str | Path = ".") -> dict[str, Any]:
    """Return project context without changing files or repository state."""
    root = Path(root).resolve()
    docs = {
        "docs/PHASE_LEDGER.md": _read(root, "docs/PHASE_LEDGER.md"),
        "AI_CONTEXT.md": _read(root, "AI_CONTEXT.md"),
        "STATUS.md": _read(root, "STATUS.md"),
    }
    phase = docs["docs/PHASE_LEDGER.md"]
    return ContextSnapshot(
        repository=_git(root, "config", "--get", "remote.origin.url"),
        branch=_git(root, "branch", "--show-current"),
        head=_git(root, "rev-parse", "HEAD"),
        source_documents=docs,
        active_phase=phase if phase != "UNKNOWN" else "UNKNOWN",
        active_task="UNKNOWN — recover from canonical handoff documents",
        implementation_state="UNKNOWN — inspect current source",
        verification_state="UNKNOWN — inspect reproducible evidence",
        acceptance_state="UNKNOWN — require explicit integration gate",
        next_permitted_action="Read-only context recovery; do not infer authority from connectivity.",
        open_findings=[],
    ).to_dict()
