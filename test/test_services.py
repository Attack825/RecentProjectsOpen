import sys
import unittest
from os.path import abspath, dirname

TEST_DIR = dirname(abspath(__file__))
PROJECT_ROOT = dirname(TEST_DIR)
sys.path.append(PROJECT_ROOT)

from src.core.acronyms import AcronymService  # noqa: E402
from src.core.suggestions import SuggestionService  # noqa: E402


class TestAcronymService(unittest.TestCase):
    def test_defaults_present(self):
        acronyms = AcronymService.get_map({})
        self.assertEqual(acronyms["idea"], "INTELLIJ_IDEA")
        self.assertEqual(acronyms["vsc"], "VSCODE")

    def test_custom_acronym_overrides_default(self):
        acronyms = AcronymService.get_map({"custom_acronyms_map": {"VSCODE": "vs"}})
        self.assertEqual(acronyms["vs"], "VSCODE")
        self.assertNotIn("vsc", acronyms)


class TestSuggestionService(unittest.TestCase):
    def test_explicit_suggestions_keep_order_and_score(self):
        config = {
            "suggestions_list": ["INTELLIJ_IDEA", "VSCODE"],
            "plugin_trigger_keyword": "r",
        }
        items = SuggestionService.build(config)
        self.assertEqual([item["title"] for item in items], ["INTELLIJ_IDEA", "VSCODE"])
        self.assertEqual(items[0]["subTitle"], "idea")
        self.assertEqual(items[0]["icoPath"], "icons/INTELLIJ_IDEA.png")
        self.assertEqual(items[0]["jsonRPCAction"]["parameters"], ["r idea ", False])
        self.assertEqual(items[0]["score"], 1000000)
        self.assertEqual(items[1]["score"], 990000)

    def test_suggestions_inferred_from_configured_apps(self):
        config = {
            "suggestions_list": None,
            "INTELLIJ_IDEA_DOWNLOAD": "C:/idea64.exe",
            "INTELLIJ_IDEA_STORAGE": "C:/recentProjects.xml",
        }
        items = SuggestionService.build(config)
        self.assertEqual([item["title"] for item in items], ["INTELLIJ_IDEA"])

    def test_unknown_program_is_skipped(self):
        items = SuggestionService.build({"suggestions_list": ["NOT_REGISTERED"]})
        self.assertEqual(items, [])


if __name__ == "__main__":
    unittest.main()
