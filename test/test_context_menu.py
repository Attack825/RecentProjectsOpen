import os
import shutil
import sys
import tempfile
import unittest
from os.path import abspath, dirname

TEST_DIR = dirname(abspath(__file__))
PROJECT_ROOT = dirname(TEST_DIR)
sys.path.append(PROJECT_ROOT)

from src.core.main import RecentProjectsOpen  # noqa: E402


def _make_app():
    # 绕过 FlowLauncher.__init__（它会读取 sys.argv[1] 并立即派发请求）
    return object.__new__(RecentProjectsOpen)


class TestContextMenu(unittest.TestCase):
    def setUp(self):
        self.app = _make_app()
        self.project_dir = tempfile.mkdtemp(prefix="rpo 上下文 空格 ")

    def tearDown(self):
        shutil.rmtree(self.project_dir, ignore_errors=True)

    def _methods(self, items):
        return [item["jsonRPCAction"]["method"] for item in items]

    def _copy_params(self, items):
        for item in items:
            if item["jsonRPCAction"]["method"] == "copy_to_clipboard":
                return item["jsonRPCAction"]["parameters"]
        return None

    def test_structured_context_data_with_space_and_chinese_path(self):
        data = {
            "command": ["C:/fake/idea64.exe", self.project_dir],
            "path": self.project_dir,
        }
        items = self.app.context_menu(data)
        self.assertEqual(
            self._methods(items),
            ["copy_to_clipboard", "open_in_explorer", "open_url"],
        )
        self.assertEqual(self._copy_params(items), [os.path.normpath(self.project_dir)])

    def test_legacy_command_array(self):
        data = ["C:/fake/idea64.exe", self.project_dir]
        items = self.app.context_menu(data)
        self.assertIn("copy_to_clipboard", self._methods(items))
        self.assertIn("open_in_explorer", self._methods(items))

    def test_legacy_vscode_ssh_command_array(self):
        """旧实现取 data[1]（"--remote"）会失效；现在取命令数组最后一项"""
        data = [
            "C:/fake/code.exe",
            "--remote",
            "ssh-remote+host",
            self.project_dir,
        ]
        items = self.app.context_menu(data)
        self.assertEqual(self._copy_params(items), [os.path.normpath(self.project_dir)])

    def test_nonexistent_path_has_no_explorer_entry(self):
        data = {
            "command": ["C:/fake/idea64.exe", "D:/no/such/dir"],
            "path": "D:/no/such/dir",
        }
        items = self.app.context_menu(data)
        self.assertEqual(self._methods(items), ["copy_to_clipboard", "open_url"])

    def test_missing_context_data_only_shows_repo(self):
        for data in (None, [], "", 0):
            items = self.app.context_menu(data)
            self.assertEqual(len(items), 1)
            self.assertEqual(items[0]["jsonRPCAction"]["method"], "open_url")


if __name__ == "__main__":
    unittest.main()
