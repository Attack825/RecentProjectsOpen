import os
from pathlib import Path
from typing import Dict, Any

from click import UsageError
from .jsonrpc import settings


class Config(dict):
    def __init__(self):
        super().__init__()
        self._parse_settings()

    def _parse_settings(self) -> None:
        """解析从 Flow Launcher 获取的配置"""
        flow_settings = settings()  # 直接从 jsonrpc 获取
        program_path = flow_settings.get("program_path", "")
        if program_path:
            # 解析多行配置，格式如: KEY=VALUE\nKEY2=VALUE2
            for line in program_path.split('\n'):
                line = line.strip()
                if line and '=' in line:
                    key, value = line.split('=', 1)
                    self[key.strip()] = value.strip()

    def get(self, key: str) -> str:
        """获取配置值，如果不存在则抛出异常"""
        value = super().get(key)
        if not value:
            raise UsageError(f"Missing config key: {key}")
        return value


config = Config()
