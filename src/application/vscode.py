import json
import os
import urllib.parse

from ..core.logger import get_logger
from ..core.project import Project
from ..core.registry import ApplicationRegistry
from .base_application import BaseApplication

logger = get_logger()


@ApplicationRegistry.register("VSCODE")
class Vscode(BaseApplication):
    def __init__(self, download_path: str, storage_file: str):
        super().__init__(download_path, storage_file)
        self.name = "VSCODE"
        self.acronyms = "vsc"

    def get_projects(self) -> list[Project]:
        """获取vscode最近打开项目路径"""
        storage_file = self.storage_file
        if storage_file is None:
            storage_file = os.path.join(
                os.getenv("APPDATA"), "Code", "User", "globalStorage", "storage.json"
            )
        self.storage_file = storage_file
        self.validate_storage()
        # 读取文件storage.json
        with open(storage_file, encoding="utf8") as f:
            data = json.loads(f.read())
            profileAssociations = data.get("profileAssociations")
            workspaces = profileAssociations.get("workspaces")
            keys_list = list(workspaces.keys())
        # 倒序遍历，保持"最近打开的在前"
        folder_urls = [key for key in reversed(keys_list) if key.startswith("file:///")]
        return [Project(self.name, self._to_windows_path(url)) for url in folder_urls]

    @staticmethod
    def _to_windows_path(folder_url: str) -> str:
        folder_url = folder_url.replace("file:///", "")
        folder_url = urllib.parse.unquote(folder_url)
        return folder_url[0].upper() + folder_url[1:]
