import importlib
import os
from typing import ClassVar

from ..application.base_application import BaseApplication


class ApplicationRegistry:
    _applications: ClassVar[dict[str, type[BaseApplication]]] = {}
    _acronyms_map: ClassVar[dict[str, str]] = {}
    _loaded: ClassVar[bool] = False

    @classmethod
    def register(cls, app_name: str):
        """应用注册装饰器"""

        def wrapper(application_class: type[BaseApplication]):
            cls._applications[app_name] = application_class
            temp_instance = application_class("", "")
            cls._acronyms_map[temp_instance.acronyms] = app_name
            return application_class

        return wrapper

    @classmethod
    def load_applications(cls):
        """自动加载所有应用模块"""

        # 获取applications目录的绝对路径
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        applications_dir = os.path.join(current_dir, "application")

        # 遍历应用目录下的所有.py文件
        for filename in os.listdir(applications_dir):
            if (
                filename.endswith(".py")
                and filename != "__init__.py"
                and filename != "base_application.py"
                and filename != "base_jetbrains.py"
            ):
                module_name = filename[:-3]
                # 动态导入模块
                importlib.import_module(
                    f"..application.{module_name}", package=__package__
                )

        cls._loaded = True

    @classmethod
    def get_application(cls, name: str):
        """获取注册的应用类"""
        return cls._applications.get(name)

    @classmethod
    def get_all_applications(cls):
        """获取所有注册的应用"""
        return cls._applications

    @classmethod
    def get_acronyms_map(cls) -> dict[str, str]:
        """获取所有应用的缩写映射"""
        return cls._acronyms_map
