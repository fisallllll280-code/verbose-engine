"""Fail-closed behavior and source preservation tests for the CSD kernel facade."""
from __future__ import annotations

import unittest

from vaixlns.csd.kernel import CSDKernelUnavailable, require_runtime, status


class CSDKernelFacadeTests(unittest.TestCase):
    def test_mixed_source_is_preserved_but_not_claimed_as_runtime(self):
        result = status()
        self.assertEqual(result["kernel_id"], "CSD-KERNEL")
        self.assertEqual(result["status"], "MISSING")
        self.assertFalse(result["runtime_executable"])
        self.assertTrue(result["legacy_source_present"])
        self.assertEqual(
            result["legacy_source_path"],
            "vaixlns/csd/kernel.mixed-source.txt",
        )

    def test_runtime_request_fails_closed(self):
        with self.assertRaisesRegex(CSDKernelUnavailable, "not implemented"):
            require_runtime()


if __name__ == "__main__":
    unittest.main()
