import json
from datetime import datetime
from typing import Any

from ..core.errors import StorageFileNotFound
from ..core.project import Project
from ..core.registry import ApplicationRegistry
from .base_application import BaseApplication


@ApplicationRegistry.register("TYPORA")
class Typora(BaseApplication):
    def __init__(self, download_path: str, storage_file: str):
        super().__init__(download_path, storage_file)
        self.name = "TYPORA"
        self.acronyms = "ty"

    def get_projects(self) -> list[Project]:
        """获取Typora最近打开的项目"""
        try:
            with open(self.storage_file, encoding="utf-8") as file:
                raw_content = file.read()
        except FileNotFoundError:
            raise StorageFileNotFound(self.name, self.storage_file) from None

        # history.data 是 hex 编码的 JSON
        buffer = bytes.fromhex(raw_content)
        settings_content = json.loads(buffer.decode("utf-8"))

        # combine recentFolder and recentDocument
        all_items: list[dict[str, Any]] = []

        if "recentFolder" in settings_content:
            for folder in settings_content["recentFolder"]:
                if "path" in folder and "date" in folder:
                    # convert ISO 8601 date string to timestamp
                    timestamp = datetime.fromisoformat(
                        folder["date"].replace("Z", "+00:00")
                    ).timestamp()
                    all_items.append({"path": folder["path"], "timestamp": timestamp})

        if "recentDocument" in settings_content:
            for document in settings_content["recentDocument"]:
                if "path" in document and "date" in document:
                    timestamp = float(document["date"]) / 1000
                    all_items.append({"path": document["path"], "timestamp": timestamp})

        # sort all items by timestamp in descending order
        all_items.sort(key=lambda x: x["timestamp"], reverse=True)

        return [Project(self.name, item["path"]) for item in all_items]
