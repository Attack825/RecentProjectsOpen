from ..application.base_jetbrains import Jetbrains
from ..core.registry import ApplicationRegistry


@ApplicationRegistry.register("PYCHARM")
class Pycharm(Jetbrains):
    def __init__(self, download_path: str, storage_file: str):
        super().__init__(download_path, storage_file)
        self.name = "PYCHARM"
        self.acronyms = "py"
