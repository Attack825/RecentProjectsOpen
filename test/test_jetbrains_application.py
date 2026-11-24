import os
import sys
import unittest

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(TEST_DIR)
sys.path.append(PROJECT_ROOT)

from src.application.base_jetbrains import Jetbrains  # noqa: E402
from src.core.errors import StorageFileNotFound  # noqa: E402


class TestJetbrainsApplication(unittest.TestCase):
    def setUp(self):
        """测试初始化"""
        self.mock_data_dir = os.path.join(TEST_DIR, "mock_data")
        self.valid_config_path = os.path.join(
            self.mock_data_dir, "test_jetbrains_recent_project.xml"
        )
        self.invalid_config_path = os.path.join(self.mock_data_dir, "nonexistent.xml")

        self.jetbrains_app = Jetbrains(
            download_path="",
            storage_file=self.valid_config_path,
        )

    def test_get_projects_with_valid_file(self):
        """测试从有效配置文件中获取项目列表"""
        projects = self.jetbrains_app.get_projects()
        self.assertEqual(len(projects), 3)
        expected_paths = [
            "D:/javaproject/java_classroom",
            "D:/Project/JavaProject/RuoYi",
            "D:/Project/JavaProject/RuoYi/ruoyi-admin",
        ]

        for project, expected_path in zip(projects, expected_paths):
            self.assertEqual(project.path, expected_path)
            self.assertEqual(project.app_name, self.jetbrains_app.name)

    def test_get_projects_with_invalid_file(self):
        """测试使用不存在的配置文件时的错误处理"""
        invalid_app = Jetbrains("", self.invalid_config_path)

        with self.assertRaises(StorageFileNotFound) as context:
            invalid_app.get_projects()

        self.assertEqual(context.exception.app_name, "BASE")
        self.assertEqual(context.exception.path, self.invalid_config_path)


if __name__ == "__main__":
    unittest.main()
