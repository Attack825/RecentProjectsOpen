import os
import sys
import unittest
from os.path import abspath, dirname

TEST_DIR = dirname(abspath(__file__))
PROJECT_ROOT = dirname(TEST_DIR)
sys.path.append(PROJECT_ROOT)

from src.application.base_application import BaseApplication  # noqa: E402
from src.core.errors import StorageFileNotFound  # noqa: E402
from src.core.naming import config_keys, download_key, icon_path, storage_key  # noqa: E402


class _DummyApplication(BaseApplication):
    def get_projects(self):
        return []


class TestNaming(unittest.TestCase):
    def test_config_keys(self):
        self.assertEqual(config_keys("VSCODE"), ("VSCODE_DOWNLOAD", "VSCODE_STORAGE"))
        self.assertEqual(download_key("TYPORA"), "TYPORA_DOWNLOAD")
        self.assertEqual(storage_key("TYPORA"), "TYPORA_STORAGE")

    def test_icon_path(self):
        self.assertEqual(icon_path("INTELLIJ_IDEA"), "icons/INTELLIJ_IDEA.png")

    def test_icon_path_property_follows_name(self):
        app = _DummyApplication("", "")
        app.name = "DEMO"
        self.assertEqual(app.icon_path, "icons/DEMO.png")

    def test_validate_storage_missing(self):
        app = _DummyApplication("", os.path.join(TEST_DIR, "mock_data", "nope.xml"))
        app.name = "DEMO"
        with self.assertRaises(StorageFileNotFound) as context:
            app.validate_storage()
        self.assertEqual(context.exception.app_name, "DEMO")
        self.assertIn("nope.xml", str(context.exception))

    def test_validate_storage_ok(self):
        storage = os.path.join(
            TEST_DIR, "mock_data", "test_jetbrains_recent_project.xml"
        )
        app = _DummyApplication("", storage)
        app.validate_storage()  # 不抛异常即通过


if __name__ == "__main__":
    unittest.main()
