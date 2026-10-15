# verbose-engine CSD Kernel Recovery Plan v1

**Status:** PARTIAL / RECOVERY REQUIRED  
**Executable facade:** `vaixlns/csd/kernel.py` (reports `MISSING` and fails closed)  
**Baseline observed during review:** `ffe607b29d36cff6f05494f7ec3fd11f2395ec4b`  
**Working branch:** `recovery/csd-kernel-audit-v1`

## Why this recovery is necessary

The former `vaixlns/csd/kernel.py` contained 63,558 bytes of mixed-language and conversational material, and CI confirmed a Python syntax error before the tests could run. PR #8 preserves that exact source as `vaixlns/csd/kernel.mixed-source.txt` and replaces the Python path with a fail-closed facade that reports `MISSING`; it does not claim an executable CSD kernel exists. The same PR preserves the malformed imported path inventory and original Git tree references so checkout can proceed without a history rewrite.

The repository history also includes a plan for twelve CSD laws, Merkle state hashing, XV/VV/VX coupling, attack simulation, replay verification, and a `verify-kernel` CLI. A plan in a commit message is not proof those deliverables exist or work.

## Safe first increment

This branch adds a **read-only structural audit** against `vaixlns/csd/kernel.mixed-source.txt` and unit tests. It does not execute the archive or extract embedded sections automatically. The original 63,558-byte source is preserved byte-for-byte; the .py path is only a fail-closed status facade until a separately reviewed implementation exists.

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
