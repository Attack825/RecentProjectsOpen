import re

from ..core.logger import get_logger
from ..core.project import Project
from ..core.registry import ApplicationRegistry
from .base_application import BaseApplication

logger = get_logger()


@ApplicationRegistry.register("SUMATRA")
class SumatraPDF(BaseApplication):
    def __init__(self, download_path: str, storage_file: str):
        super().__init__(download_path, storage_file)
        self.name = "SUMATRA"
        self.acronyms = "pdf"

    def get_projects(self) -> list[Project]:
        """获取SumatraPDF最近打开项目路径"""
        projects = []

        try:
            with open(self.storage_file, encoding="utf-8") as file:
                settings_content = file.read()
        except FileNotFoundError:
            logger.warning("Settings file not found: %s", self.storage_file)
            return projects

        # 使用正则表达式匹配 FilePath
        file_path_pattern = re.compile(r"\s*FilePath\s*=\s*(.+)")
        matches = file_path_pattern.findall(settings_content)

        for match in matches:
            file_path = match.strip()
            if file_path:
                projects.append(Project(self.name, file_path))

        return projects
