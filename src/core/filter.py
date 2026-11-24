from abc import ABC, abstractmethod
from difflib import SequenceMatcher

from pypinyin import Style, lazy_pinyin

from .project import Project

# 相似度阈值。原实现用 fuzzywuzzy 的 "> 90"（WRatio 在字符级比较时上限恰好是 90），
# 该分支实际永不命中。0.9 可覆盖长名称里的单字符笔误（如 recentprojectsopen），
# 又能把 project1 / project2 这类"仅末位不同"的近似名区分开；
# 片段输入由 startswith / 子串匹配负责，不依赖该阈值。
FUZZY_THRESHOLD = 0.9


class Filter(ABC):
    @classmethod
    @abstractmethod
    def query_filter(cls, query: str, items: list[Project]) -> list[Project]:
        pass


class Fuzzy_Filter(Filter):
    @classmethod
    def query_filter(cls, query: str, items: list[Project]) -> list[Project]:
        """按项目名的拼音做前缀 / 子串 / 模糊匹配"""
        if len(query) < 1:
            return items

        query_pinyin = "".join(lazy_pinyin(query, style=Style.NORMAL)).lower()
        matches = []
        for item in items:
            project_pinyin = "".join(lazy_pinyin(item.name, style=Style.NORMAL)).lower()
            if (
                project_pinyin.startswith(query_pinyin)
                or query_pinyin in project_pinyin
                or SequenceMatcher(None, query_pinyin, project_pinyin).ratio()
                >= FUZZY_THRESHOLD
            ):
                matches.append(item)
        return matches
