from click import UsageError

from .jsonrpc import settings
from .logger import get_logger

logger = get_logger()


class Config(dict):
    def __init__(self):
        super().__init__()
        self._parse_settings()

    def _parse_settings(self) -> None:
        """解析从 Flow Launcher 获取的配置"""
        flow_settings = settings()
        if not flow_settings:
            return
        
        # 解析 program_path 配置
        program_path = flow_settings.get("program_path") if "program_path" in flow_settings else None
        if program_path:
            # 解析多行配置，格式如: KEY=VALUE\nKEY2=VALUE2
            for line in program_path.split("\n"):
                line = line.strip()
                if line and "=" in line:
                    key, value = line.split("=", 1)
                    self[key.strip()] = value.strip()
        # 解析 acronyms_list 配置
        acronyms_list = flow_settings.get("acronyms_list") if "acronyms_list" in flow_settings else None
        if acronyms_list:
            self["acronyms_list"] = [s.strip() for s in acronyms_list.split("\n") if s.strip()]
        # 解析其他配置
        for key, value in flow_settings.items():
            if key not in self and key not in ("acronyms_list", "program_path"):
                self[key] = value

    def get(self, key: str) -> str:
        """获取配置值，如果不存在则抛出异常"""
        value = super().get(key)
        if not value:
            raise UsageError(f"Missing config key: {key}")
        return value


config = Config()
