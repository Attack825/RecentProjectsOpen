import os
import sys
import unittest
from unittest.mock import patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.core.config import Config


class TestConfig(unittest.TestCase):
    @patch("src.core.config.settings")
    def test_settings_parsing(self, mock_settings):
        """测试配置解析功能"""
        mock_settings.return_value = {
            "program_path": "VSCODE_DOWNLOAD=C:/Program Files/Microsoft VS Code/Code.exe\nVSCODE_STORAGE=C:/Users/TestUser/AppData/Roaming/Code/User/globalStorage/storage.json\nCURSOR_DOWNLOAD=C:/Program Files/Cursor/Cursor.exe\nCURSOR_STORAGE=C:/Users/TestUser/AppData/Roaming/Cursor/User/globalStorage/storage.json\nTYPORA_DOWNLOAD=C:/Program Files/Typora/Typora.exe\nTYPORA_STORAGE=C:/Users/TestUser/AppData/Roaming/Typora/history.data"
        }

        config = Config()

        self.assertEqual(
            config.get("VSCODE_DOWNLOAD"), "C:/Program Files/Microsoft VS Code/Code.exe"
        )
        self.assertEqual(
            config.get("VSCODE_STORAGE"),
            "C:/Users/TestUser/AppData/Roaming/Code/User/globalStorage/storage.json",
        )
        self.assertEqual(
            config.get("CURSOR_DOWNLOAD"), "C:/Program Files/Cursor/Cursor.exe"
        )
        self.assertEqual(
            config.get("CURSOR_STORAGE"),
            "C:/Users/TestUser/AppData/Roaming/Cursor/User/globalStorage/storage.json",
        )
        self.assertEqual(
            config.get("TYPORA_DOWNLOAD"), "C:/Program Files/Typora/Typora.exe"
        )
        self.assertEqual(
            config.get("TYPORA_STORAGE"),
            "C:/Users/TestUser/AppData/Roaming/Typora/history.data",
        )

    @patch("src.core.config.settings")
    def test_empty_settings(self, mock_settings):
        """测试空配置"""
        mock_settings.return_value = {}

        config = Config()

        self.assertIsNone(config.get("NONEXISTENT_KEY"))

    @patch("src.core.config.settings")
    def test_settings_default_value(self, mock_settings):
        """测试配置默认值"""
        mock_settings.return_value = {}

        config = Config()

        self.assertEqual(
            config.get("NONEXISTENT_KEY", "default_value"), "default_value"
        )


if __name__ == "__main__":
    unittest.main()
