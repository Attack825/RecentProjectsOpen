from abc import ABC, abstractmethod
from typing import Dict, List

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
        获取应用的缩写字典，优先使用用户自定义的 acronyms_map
        返回格式:
        {
            "vsc": "VSCODE",
            "idea": "IDEA",
            ...
        }
        """
        ApplicationRegistry.load_applications()
        default_acronyms_map = ApplicationRegistry.get_acronyms_map()
        custom_acronyms_map = plugin_config.get("custom_acronyms_map", None)
        if custom_acronyms_map:
            # acronyms_map: {"VSCODE": "vsc"}
            # 只合并支持的程序名
            supported_programs = set(default_acronyms_map.values())
            for prog, acr in custom_acronyms_map.items():
                if prog in supported_programs:
                    default_acronyms_map[acr] = prog
        return default_acronyms_map

    @classmethod
    def get_application_message(cls, plugin_config):
        """
        根据传入的 acronyms_suggestions_list 生成 Flow Launcher 消消息列表。
        如果未传入，则只展示用户已配置路径的应用。
        """
        custom_acronyms_map = plugin_config.get("custom_acronyms_map", None)
        acronyms_suggestions_list = plugin_config.get("acronyms_suggestions_list", None)
        plugin_trigger_keyword = plugin_config.get("plugin_trigger_keyword", "r")
        acronyms_dict = cls.get_application_acronyms(custom_acronyms_map)
        logger.debug(acronyms_suggestions_list)
        # 只显示已配置的应用建议
        if acronyms_suggestions_list is None:
            acronyms_suggestions_list = []
            for acr, app_name in acronyms_dict.items():
                download_key = app_name + "_DOWNLOAD"
                storage_key = app_name + "_STORAGE"
                if download_key in plugin_config and storage_key in plugin_config:
                    acronyms_suggestions_list.append(acr)
        return [
            {
                "title": acronyms_dict.get(acronyms),
                "subTitle": acronyms,
                "icoPath": f"icons/{acronyms_dict.get(acronyms)}.png",
                "jsonRPCAction": {
                    "method": "Flow.Launcher.ChangeQuery",
                    "parameters": [f"{plugin_trigger_keyword} {acronyms} ", False],
                    "dontHideAfterAction": True,
                },
                "score": 0,
            }
            for acronyms in acronyms_suggestions_list
        ]
