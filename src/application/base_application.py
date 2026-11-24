from abc import abstractmethod

from ..core.logger import get_logger
from ..core.project import Project

logger = get_logger()
ICON_SUFFIX = "_icon.png"


class BaseApplication:
    def __init__(
        self,
        download_path: str,
        storage_file: str,
    ):
        self.name = "BASE"
        self.acronyms = "base"
        self.icon_path = self.acronyms + ICON_SUFFIX
        self.download_path = download_path
        self.storage_file = storage_file
        self.projects = None

    @abstractmethod
    def get_projects(self) -> list[Project]:
        pass
