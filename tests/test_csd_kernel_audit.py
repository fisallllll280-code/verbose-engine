import importlib.util
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "audit_csd_kernel.py"
SPEC = importlib.util.spec_from_file_location("audit_csd_kernel", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class CSDKernalAuditTests(unittest.TestCase):
    def test_detects_mixed_language_and_document_markers(self):
        sample = """# Design note
class Kernel:
    pass
pub struct RootSpec {}
[build-system]
"""
        report = MODULE.audit_text(sample)
        labels = {item["marker"] for item in report["findings"]}
        self.assertIn("Markdown heading", labels)
        self.assertIn("Rust item", labels)
        self.assertIn("TOML section", labels)
        self.assertEqual(report["schema"], "vaixlns.csd-kernel-structure-audit.v1")

    def test_clean_python_sample_has_no_findings(self):
        report = MODULE.audit_text("def add(a, b):\n    return a + b\n")
        self.assertEqual(report["findings"], [])

    def test_default_target_is_preserved_mixed_source_not_runtime_facade(self):
        self.assertEqual(str(MODULE.DEFAULT_TARGET), "vaixlns/csd/kernel.mixed-source.txt")
        report = MODULE.audit_text("VAIXLNS_ROOT.lns\n")
        self.assertEqual(report["target_language"], "unclassified_mixed_source")

    def test_audit_is_heuristic_not_claim_of_invalidity(self):
        report = MODULE.audit_text("# heading\n")
        self.assertIn("not a parser", report["interpretation"])


if __name__ == "__main__":
    unittest.main()
