"""应用命名约定：配置键与图标路径的唯一来源。

宿主设置面板里的 `<APP>_DOWNLOAD` / `<APP>_STORAGE`、以及 `icons/<APP>.png`
此前散落在 main.py、factory.py、base_application.py 三处字符串拼接里，
改一处忘一处就会静默失效；统一收敛到这里，并由测试锁定。
"""

DOWNLOAD_SUFFIX = "_DOWNLOAD"
STORAGE_SUFFIX = "_STORAGE"


def download_key(app_name: str) -> str:
    return f"{app_name}{DOWNLOAD_SUFFIX}"


def storage_key(app_name: str) -> str:
    return f"{app_name}{STORAGE_SUFFIX}"


def config_keys(app_name: str) -> tuple[str, str]:
    """返回 (download_key, storage_key)。"""
    return download_key(app_name), storage_key(app_name)


def icon_path(app_name: str) -> str:
    return f"icons/{app_name}.png"
