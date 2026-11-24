"""领域异常。

适配器与调用方之间不再用"返回空列表"表达失败：所有"配置文件不存在"都抛
StorageFileNotFound，由 main.query 统一转成 Flow 的提示项。
"""


class StorageFileNotFound(FileNotFoundError):
    """IDE / 编辑器保存"最近项目"的文件不存在。"""

    def __init__(self, app_name: str, path: str):
        self.app_name = app_name
        self.path = path
        super().__init__(f"{app_name}: storage file not found: {path}")
