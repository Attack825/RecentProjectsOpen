import os
from typing import Optional

from .logger import get_logger

logger = get_logger()


class Project:
    def __init__(
        self, app_name: str, path: str, command_args: Optional[list[str]] = None
    ):
        self.app_name = app_name
        self.path = path
        self.name = os.path.basename(path)
        self.command_args: Optional[list[str]] = command_args

    def get_command(self, app_download: str) -> list[str]:
        """获取完整的命令列表"""
        if self.command_args is not None:
            return [app_download] + self.command_args
        return [app_download, self.path]
