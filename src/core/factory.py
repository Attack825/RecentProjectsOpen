from abc import ABC, abstractmethod
from typing import Dict

from .registry import ApplicationRegistry
from .logger import get_logger

logger = get_logger()


class AbstractFactory(ABC):
    @classmethod
    @abstractmethod
    def create_app(cls, name: str, download_path: str, storage_file: str):
        pass


class ConcreteFactory(AbstractFactory):
    @classmethod
    def create_app(cls, name: str, download_path: str, storage_file: str):
        """通过注册表创建应用实例"""
        ApplicationRegistry.load_applications()
        try:
            application_class = ApplicationRegistry.get_application(name)
            if application_class is None:
                raise NotImplementedError(f"Application {name} not registered")
            return application_class(download_path, storage_file)
        except FileNotFoundError as e:
            raise e

    @classmethod
    def get_supported_applications(cls):
        """
        获取所有支持的应用列表
        """
        return list(ApplicationRegistry.get_all_applications().keys())

    @classmethod
    def get_application_acronyms(cls, plugin_config) -> Dict[str, str]:
        """
        获取应用的缩写字典，优先使用 plugin_config 中用户自定义的 custom_acronyms_map。
        返回格式:
        {
            "vsc": "VSCODE",
            "cs": "CURSOR",
            ...
        }
        """
        ApplicationRegistry.load_applications()
        default_acronyms_map = ApplicationRegistry.get_acronyms_map()
        custom_acronyms_map = plugin_config.get("custom_acronyms_map", {})
        acronyms_map = {acr: prog.upper() for prog, acr in custom_acronyms_map.items()}
        for acr, prog in default_acronyms_map.items():
            if prog not in acronyms_map.values():
                acronyms_map[acr] = prog
        return acronyms_map

    @classmethod
    def get_application_message(cls, plugin_config):
        """
        根据配置的 suggestions_list 生成 Flow Launcher 消息列表。
        如果未配置，则只展示用户已配置路径的应用。
        """
        suggestions_list = plugin_config.get("suggestions_list", None)
        plugin_trigger_keyword = plugin_config.get("plugin_trigger_keyword", "r")
        acronyms_dict = cls.get_application_acronyms(plugin_config)
        reverse_acronyms_dict = {v: k for k, v in acronyms_dict.items()}

        # 只显示已配置的应用建议
        if suggestions_list is None:
            suggestions_list = []
            for _, program_name in acronyms_dict.items():
                download_key = program_name + "_DOWNLOAD"
                storage_key = program_name + "_STORAGE"
                if download_key in plugin_config and storage_key in plugin_config:
                    suggestions_list.append(program_name)

        messages = []
        for idx, program_name in enumerate(suggestions_list):
            if program_name in reverse_acronyms_dict:
                acronyms = reverse_acronyms_dict[program_name]
                messages.append(
                    {
                        "title": program_name,
                        "subTitle": acronyms,
                        "icoPath": f"icons/{program_name}.png",
                        "jsonRPCAction": {
                            "method": "Flow.Launcher.ChangeQuery",
                            "parameters": [
                                f"{plugin_trigger_keyword} {acronyms} ",
                                False,
                            ],
                            "dontHideAfterAction": True,
                        },
                        # 按原始顺序排序
                        "score": (100 - idx) * 10000,
                    }
                )
        return messages
