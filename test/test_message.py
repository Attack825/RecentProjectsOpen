import sys
import unittest
from os.path import abspath, dirname

TEST_DIR = dirname(abspath(__file__))
PROJECT_ROOT = dirname(TEST_DIR)
sys.path.append(PROJECT_ROOT)

from src.core.message import MessageDTO  # noqa: E402
from src.core.project import Project  # noqa: E402


class TestMessageDTO(unittest.TestCase):
    def setUp(self):
        """测试初始化"""
        self.icon_path = "icons/app.png"
        self.method = "openProject"
        self.app_download = "code"

        self.project1 = Project("vscode", "/path/to/project1")
        self.project2 = Project("vscode", "/path/to/project2")
        self.projects = [self.project1, self.project2]

    def test_asMultiFlowMessage_normal(self):
        """测试正常情况下的MultiFlow消息生成"""
        messages = MessageDTO.asMultiFlowMessage(
            self.projects, self.icon_path, self.method, self.app_download
        )

        self.assertEqual(len(messages), 2)

        first_msg = messages[0]
        self.assertEqual(first_msg["Title"], "project1")
        self.assertEqual(first_msg["SubTitle"], "/path/to/project1")
        self.assertEqual(first_msg["IcoPath"], self.icon_path)
        self.assertEqual(
            first_msg["ContextData"],
            {
                "command": [self.app_download, "/path/to/project1"],
                "path": "/path/to/project1",
            },
        )
        self.assertEqual(
            first_msg["jsonRPCAction"],
            {
                "method": self.method,
                "parameters": [self.app_download, "/path/to/project1"],
            },
        )

        second_msg = messages[1]
        self.assertEqual(second_msg["Title"], "project2")
        self.assertEqual(second_msg["SubTitle"], "/path/to/project2")
        self.assertEqual(
            second_msg["ContextData"],
            {
                "command": [self.app_download, "/path/to/project2"],
                "path": "/path/to/project2",
            },
        )
        self.assertEqual(
            second_msg["jsonRPCAction"],
            {
                "method": self.method,
                "parameters": [self.app_download, "/path/to/project2"],
            },
        )

    def test_asMultiFlowMessage_empty_list(self):
        """测试空项目列表的情况"""
        messages = MessageDTO.asMultiFlowMessage(
            [], self.icon_path, self.method, self.app_download
        )
        self.assertEqual(messages, [])

    def test_asWarnFlowMessage(self):
        """测试警告消息生成"""
        title = "Warning Title"
        subtitle = "Warning Message"
        messages = MessageDTO.asWarnFlowMessage(title, subtitle)

        self.assertEqual(len(messages), 1)
        warn_msg = messages[0]
        self.assertEqual(warn_msg["Title"], title)
        self.assertEqual(warn_msg["SubTitle"], subtitle)
        self.assertEqual(warn_msg["IcoPath"], "icons/warn.png")

    def test_asDebugFlowMessage(self):
        """测试调试消息生成"""
        debug_message = "Debug Information"
        messages = MessageDTO.asDebugFlowMessage(debug_message)

        self.assertEqual(len(messages), 1)
        debug_msg = messages[0]
        self.assertEqual(debug_msg["Title"], debug_message)
        self.assertEqual(debug_msg["SubTitle"], "Debug")
        self.assertEqual(debug_msg["IcoPath"], "icons/app.png")


if __name__ == "__main__":
    unittest.main()
