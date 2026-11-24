import os
from abc import abstractmethod

from ..core.errors import StorageFileNotFound
from ..core.logger import get_logger
from ..core.naming import icon_path
from ..core.project import Project

logger = get_logger()


class BaseApplication:
    def __init__(
        self,
        download_path: str,
        storage_file: str,
    ):
        self.name = "BASE"
        self.acronyms = "base"
        self.download_path = download_path
        self.storage_file = storage_file
        self.projects = None

    @property
    def icon_path(self) -> str:
        """与 `icons/<注册键>.png` 约定保持一致（子类在 super().__init__ 之后设置 name）。"""
        return icon_path(self.name)

    def validate_storage(self) -> None:
        """存储文件必须存在；不存在时抛统一的 StorageFileNotFound。"""
        if not self.storage_file or not os.path.exists(self.storage_file):
            raise StorageFileNotFound(self.name, self.storage_file or "")

    @abstractmethod
    def get_projects(self) -> list[Project]:
        pass
