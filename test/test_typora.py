import os
import sys
import unittest
from os.path import abspath, dirname

TEST_DIR = dirname(abspath(__file__))
PROJECT_ROOT = dirname(TEST_DIR)
sys.path.append(PROJECT_ROOT)

from src.application.typora import Typora  # noqa: E402
from src.core.errors import StorageFileNotFound  # noqa: E402


class TestTypora(unittest.TestCase):
    def setUp(self):
        """测试初始化"""
        self.mock_data_dir = os.path.join(TEST_DIR, "mock_data")
        self.mock_history_file = os.path.join(self.mock_data_dir, "history.data")
        self.typora = Typora(
            download_path="",
            storage_file=self.mock_history_file,
        )

    def test_get_projects_with_valid_file(self):
        """测试从有效的历史文件中获取项目列表"""
        projects = self.typora.get_projects()

        self.assertTrue(len(projects) > 0)

        first_project = projects[0]
        self.assertEqual(first_project.app_name, "TYPORA")
        self.assertEqual(first_project.path, r"C:\Users\xuwenjie\Desktop\物化生557.md")

    def test_get_projects_with_invalid_file(self):
        """配置文件不存在时应抛统一的 StorageFileNotFound，而不是静默返回空列表"""
        invalid_typora = Typora(
            download_path="",
            storage_file=os.path.join(self.mock_data_dir, "nonexistent.data"),
        )
        with self.assertRaises(StorageFileNotFound) as context:
            invalid_typora.get_projects()
        self.assertEqual(context.exception.app_name, "TYPORA")

    def test_typora_initialization(self):
        """测试Typora类的初始化"""
        self.assertEqual(self.typora.name, "TYPORA")
        self.assertEqual(self.typora.acronyms, "ty")


if __name__ == "__main__":
    unittest.main()
