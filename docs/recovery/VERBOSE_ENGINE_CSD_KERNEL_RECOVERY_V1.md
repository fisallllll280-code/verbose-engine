# verbose-engine CSD Kernel Recovery Plan v1

**Status:** PARTIAL / RECOVERY REQUIRED  
**Target:** `vaixlns/csd/kernel.py` on the default branch  
**Baseline observed during review:** `ffe607b29d36cff6f05494f7ec3fd11f2395ec4b`  
**Working branch:** `recovery/csd-kernel-audit-v1`

## Why this recovery is necessary

The current kernel file contains material that appears to mix Python with an LNS root document, Rust-shaped declarations, TOML-like sections, and Markdown. These are heuristic observations from source inspection, not a claim that every marker is active code or that the whole file fails to parse. The existing CI run inspected during review failed during checkout, before tests; it is not evidence of a Python source failure.

The repository history also includes a plan for twelve CSD laws, Merkle state hashing, XV/VV/VX coupling, attack simulation, replay verification, and a `verify-kernel` CLI. A plan in a commit message is not proof those deliverables exist or work.

## Safe first increment

This branch adds a **read-only structural audit** and unit tests. It deliberately does not rewrite the legacy kernel or extract embedded sections automatically. The original source remains intact, preserving provenance and avoiding destructive guesses about section boundaries.

Run:

```bash
python -m unittest tests.test_csd_kernel_audit
python scripts/audit_csd_kernel.py
python scripts/audit_csd_kernel.py --strict
```

The default audit emits JSON and exits successfully when it can read the file. `--strict` exits nonzero when heuristic markers are found. The audit is a triage aid, not a language parser or proof of correctness.

## Required next gates

1. Capture and preserve the exact baseline tree and file hashes.
2. Run a real Python syntax check and the existing test suite in a reproducible environment; record failures without relabeling them as source defects unless logs prove that.
3. Split only after reviewing exact source boundaries:
   - canonical root document to a dedicated `.lns` file;
   - Rust source to a Rust module only if a valid complete Rust unit exists;
   - TOML configuration to a dedicated configuration file;
   - Markdown explanations to documentation;
   - Python implementation and tests to Python modules.
4. Replace placeholder checks with actual invariant implementations. A check that unconditionally returns success is not a verification.
5. Add negative tests for every invariant, malformed root, missing dependency, dependency cycle, invalid authority, stale evidence, replay divergence, and tampered ledger.
6. Run the correct toolchain for every language present. Python CI alone cannot validate Rust.
7. Connect ARC-X as an evidence/provenance gate and VX as the bounded executor. Neither the kernel nor a candidate agent may self-grant canonical authority.
8. Merge only after review and green, reproducible checks. No production-readiness claim until enforcement, persistence, trust roots, recovery, and write-path tests are independently evidenced.

## VAIXLNS integration boundary

- **VAIXLNS / `project.genome` / Ω.000:** canonical authority; unchanged by this recovery.
- **VV / VLNS:** discovery, indexing, capability and contract metadata.
- **ARC-X:** claim/evidence/provenance and contradiction review; absent evidence remains unknown or pending.
- **VX:** execution only through separately authorized, testable interfaces.
- **verbose-engine:** experimental kernel candidate; it does not become canonical merely because its tests pass.

## Acceptance criteria

- Source archive and baseline hash retained.
- Structural audit and tests pass.
- All extracted files have explicit source-line provenance.
- Python syntax and language-specific builds are tested separately.
- Each claimed invariant has both acceptance and rejection tests.
- CI receipts point to the exact tested commit.
- No claim of VERIFIED beyond the tested scope.
