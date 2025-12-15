import os
import sys
import tempfile
import types
import unittest
from importlib.machinery import SourceFileLoader
from pathlib import Path

# Stub openpyxl to allow importing the GUI module without the dependency.
openpyxl_stub = types.ModuleType("openpyxl")
openpyxl_stub.Workbook = type("Workbook", (), {})
openpyxl_stub.load_workbook = lambda *args, **kwargs: None
sys.modules.setdefault("openpyxl", openpyxl_stub)

MODULE_PATH = Path(__file__).resolve().parent.parent / "quote_builder_gui"
quote_builder_gui = SourceFileLoader("quote_builder_gui", str(MODULE_PATH)).load_module()


class UtilsTests(unittest.TestCase):
    def test_sanitize_filename_part_removes_illegal_characters(self):
        cleaned = quote_builder_gui.sanitize_filename_part('a<>:"|?*/b')
        self.assertEqual(cleaned, "a________b")
        self.assertEqual(quote_builder_gui.sanitize_filename_part(None), "")

    def test_generate_unique_path_increments_counter(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            base = "sample.xlsx"
            first = quote_builder_gui.generate_unique_path(tmpdir, base)
            open(first, "w").close()

            second = quote_builder_gui.generate_unique_path(tmpdir, base)
            open(second, "w").close()

            self.assertTrue(first.endswith(base))
            self.assertNotEqual(first, second)
            self.assertTrue(second.endswith("_1.xlsx"))

    def test_parse_quote_filename_g_extracts_components(self):
        parsed = quote_builder_gui.parse_quote_filename_g("240101_LOT베큠_LINE_PROC_INV(TOOL).xlsx")
        self.assertEqual(parsed, ("LINE", "PROC", "INV", "TOOL"))

        self.assertIsNone(quote_builder_gui.parse_quote_filename_g("invalid_name.xlsx"))

    def test_compute_base_dir_uses_module_location(self):
        base_dir = quote_builder_gui.compute_base_dir()
        self.assertEqual(base_dir, os.path.dirname(str(MODULE_PATH)))


if __name__ == "__main__":
    unittest.main()
