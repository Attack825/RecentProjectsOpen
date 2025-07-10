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
        program_path = (
            flow_settings.get("program_path")
            if "program_path" in flow_settings
            else None
        )
        if program_path:
            # 解析多行配置，格式如: KEY=VALUE\nKEY2=VALUE2
            for line in program_path.split("\n"):
                line = line.strip()
                if line and "=" in line:
                    key, value = line.split("=", 1)
                    self[key.strip()] = value.strip()

        # 解析 suggestions_list 配置（每行一个程序名称）
        suggestions_list = (
            flow_settings.get("suggestions_list")
            if "suggestions_list" in flow_settings
            else None
        )
        if suggestions_list:
            self["suggestions_list"] = [
                s.strip().upper() for s in suggestions_list.split("\n") if s.strip()
            ]

        # 解析 acronyms_map 配置
        custom_acronyms_map = (
            flow_settings.get("custom_acronyms_map")
            if "custom_acronyms_map" in flow_settings
            else None
        )
        if custom_acronyms_map:
            self["custom_acronyms_map"] = {}
            for line in custom_acronyms_map.split("\n"):
                line = line.strip()
                if line and "=" in line:
                    program, acronyms = line.split("=", 1)
                    program = program.strip().upper()
                    acronyms = acronyms.strip()
                    self["custom_acronyms_map"][program] = acronyms

        # 解析其他配置
        for key, value in flow_settings.items():
            if key not in self and key not in (
                "suggestions_list",
                "program_path",
                "custom_acronyms_map",
            ):
                self[key] = value

    def get(self, key: str, default=None) -> str:
        """获取配置值，支持默认值参数"""
        return super().get(key, default)


config = Config()
