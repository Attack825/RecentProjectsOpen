import contextlib
import sys
import unittest

from src.core.clipboard import copy_text, read_text


@unittest.skipUnless(sys.platform == "win32", "Windows clipboard API only")
class TestClipboard(unittest.TestCase):
    def setUp(self):
        try:
            self._previous = read_text()
        except OSError as exc:  # 剪贴板被其他进程占用时跳过，避免 CI 抖动
            self.skipTest(f"clipboard unavailable: {exc}")

    def tearDown(self):
        with contextlib.suppress(OSError):
            copy_text(self._previous)

    def _assert_roundtrip(self, text):
        try:
            copy_text(text)
            actual = read_text()
        except OSError as exc:
            self.skipTest(f"clipboard unavailable: {exc}")
        self.assertEqual(actual, text)

    def test_roundtrip_chinese_text(self):
        self._assert_roundtrip("最近项目：中文路径 / D:/项目/我的 项目")

    def test_roundtrip_shell_metacharacters(self):
        self._assert_roundtrip('a & b | c "quoted" %PATH% \\backslash')

    def test_empty_text(self):
        self._assert_roundtrip("")


if __name__ == "__main__":
    unittest.main()
