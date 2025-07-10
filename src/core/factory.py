from abc import ABC, abstractmethod
from typing import Dict, List

from .registry import ApplicationRegistry


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
    def get_application_acronyms(cls) -> Dict[str, str]:
        """
        获取应用的缩写字典
        返回格式:
        {
            "vsc": "VSCODE",
            "idea": "IDEA",
            "pycharm": "PYCHARM"
        }
        """
        ApplicationRegistry.load_applications()
        return ApplicationRegistry.get_acronyms_map()

    @classmethod
    def get_application_message(cls, acronyms_list):
        """
        根据传入的 acronyms_list 生成 Flow Launcher 消息列表。
        如果未传入，则只展示用户已配置路径的应用。
        """
        from src.core.config import config

        acronyms_dict = cls.get_application_acronyms()
        if acronyms_list is None:
            acronyms_list = []
            # 遍历所有应用的缩写，检查用户配置
            for acr, app_name in acronyms_dict.items():
                download_key = app_name + "_DOWNLOAD"
                storage_key = app_name + "_STORAGE"
                if download_key in config and storage_key in config:
                    acronyms_list.append(acr)
        return [
            {
                "title": acronyms_dict.get(acronyms, acronyms),
                "subTitle": acronyms,
                "icoPath": f"icons/{acronyms}_icon.png",
                "jsonRPCAction": {
                    "method": "Flow.Launcher.ChangeQuery",
                    "parameters": [f"r {acronyms} ", False],
                    "dontHideAfterAction": True,
                },
                "score": 0,
            }
            for acronyms in acronyms_list
        ]
