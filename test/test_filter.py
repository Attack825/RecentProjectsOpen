import sys
import unittest
from os.path import abspath, dirname

TEST_DIR = dirname(abspath(__file__))
PROJECT_ROOT = dirname(TEST_DIR)
sys.path.append(PROJECT_ROOT)

from src.core.filter import Fuzzy_Filter  # noqa: E402
from src.core.project import Project  # noqa: E402


def _projects(*names):
    return [Project("TEST", f"D:/projects/{name}") for name in names]


class TestFuzzyFilter(unittest.TestCase):
    def test_empty_query_returns_all(self):
        items = _projects("RuoYi", "ruoyi-admin")
        self.assertEqual(Fuzzy_Filter.query_filter("", items), items)

    def test_prefix_match(self):
        items = _projects("RuoYi", "ruoyi-admin", "Other")
        matched = Fuzzy_Filter.query_filter("ruo", items)
        self.assertEqual([p.name for p in matched], ["RuoYi", "ruoyi-admin"])

    def test_substring_match(self):
        """非前缀片段也应命中（原实现只做 startswith）"""
        items = _projects("RuoYi", "ruoyi-admin")
        matched = Fuzzy_Filter.query_filter("admin", items)
        self.assertEqual([p.name for p in matched], ["ruoyi-admin"])

    def test_typo_tolerance(self):
        """长名称里的单字符笔误命中（相似度 0.97）"""
        items = _projects("recentprojectsopen", "unrelated")
        matched = Fuzzy_Filter.query_filter("recentprojectopen", items)
        self.assertEqual([p.name for p in matched], ["recentprojectsopen"])

    def test_near_duplicate_names_are_not_confused(self):
        """project1 / project2 仅末位不同（相似度 0.875），不应互相命中"""
        items = _projects("project1", "project2")
        matched = Fuzzy_Filter.query_filter("project1", items)
        self.assertEqual([p.name for p in matched], ["project1"])

    def test_chinese_query_uses_pinyin(self):
        items = _projects("若依", "另一个项目")
        matched = Fuzzy_Filter.query_filter("ruo", items)
        self.assertEqual([p.name for p in matched], ["若依"])

    def test_no_match(self):
        items = _projects("RuoYi", "ruoyi-admin")
        self.assertEqual(Fuzzy_Filter.query_filter("zzz", items), [])

    def test_case_insensitive(self):
        items = _projects("RuoYi")
        self.assertEqual(
            [p.name for p in Fuzzy_Filter.query_filter("RUOYI", items)], ["RuoYi"]
        )


if __name__ == "__main__":
    unittest.main()
