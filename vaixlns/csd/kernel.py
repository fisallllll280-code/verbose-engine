"""Fail-closed status facade for the CSD kernel.

The historical source was a mixed-language/conversational artifact, not executable
Python. Its exact content is preserved at kernel.mixed-source.txt. This module
does not execute or interpret the archive and does not claim that a CSD runtime is
implemented. Replace this facade only after a separately reviewed executable
implementation and invariant tests exist.
"""
from __future__ import annotations

from pathlib import Path


LEGACY_SOURCE_PATH = Path(__file__).with_name("kernel.mixed-source.txt")


class CSDKernelUnavailable(RuntimeError):
    """Raised when an operation requires the not-yet-implemented CSD runtime."""


def status() -> dict[str, object]:
    """Return an honest runtime status without parsing or executing legacy source."""
    return {
        "kernel_id": "CSD-KERNEL",
        "status": "MISSING",
        "runtime_executable": False,
        "legacy_source_path": "vaixlns/csd/kernel.mixed-source.txt",
        "legacy_source_present": LEGACY_SOURCE_PATH.is_file(),
        "reason": "MIXED_LANGUAGE_ARTIFACT_ARCHIVED_PENDING_IMPLEMENTATION",
    }


def require_runtime() -> None:
    """Fail closed until an executable, independently verified kernel is supplied."""
    raise CSDKernelUnavailable(
        "CSD kernel runtime is not implemented; inspect the preserved source and audit evidence."
    )
