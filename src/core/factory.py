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
        如果未传入，则展示所有支持的应用。
        """
        acronyms_dict = cls.get_application_acronyms()
        if acronyms_list is None:
            acronyms_list = list(acronyms_dict.keys())
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
