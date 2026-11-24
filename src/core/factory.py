from abc import ABC, abstractmethod

from .logger import get_logger
from .registry import ApplicationRegistry

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
        application_class = ApplicationRegistry.get_application(name)
        if application_class is None:
            raise NotImplementedError(f"Application {name} not registered")
        return application_class(download_path, storage_file)

    @classmethod
    def get_supported_applications(cls) -> list[str]:
        """获取所有支持的应用列表"""
        return list(ApplicationRegistry.get_all_applications().keys())
