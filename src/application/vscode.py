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
            if not os.path.exists(storage_file):
                raise FileNotFoundError("storage_file not found")
        folder_urls = []
        # 读取文件storage.json
        with open(storage_file, encoding="utf8") as f:
            data = json.loads(f.read())
            profileAssociations = data.get("profileAssociations")
            workspaces = profileAssociations.get("workspaces")
            keys_list = list(workspaces.keys())
            for i in range(len(keys_list) - 1, -1, -1):  # 倒序
                if keys_list[i].startswith("file:///"):
                    folder_urls.append(keys_list[i])
        projects = []
        for folder_url in folder_urls:
            folder_url = folder_url.replace("file:///", "")
            folder_url.replace("%3A", ":").replace("/", "\\")
            folder_url = urllib.parse.unquote(folder_url)
            folder_url = folder_url[0].upper() + folder_url[1:]
            project = Project(self.name, folder_url)
            projects.append(project)

        return projects
