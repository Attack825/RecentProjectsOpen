import os
import subprocess
import webbrowser

from flowlauncher import FlowLauncher

from src.core.acronyms import AcronymService
from src.core.clipboard import copy_text
from src.core.config import config
from src.core.factory import ConcreteFactory
from src.core.filter import Fuzzy_Filter
from src.core.logger import get_logger
from src.core.message import MessageDTO
from src.core.naming import config_keys, icon_path
from src.core.suggestions import SuggestionService

logger = get_logger()

APP_ICON = "icons/app.png"
REPO_URL = "https://github.com/Attack825/RecentProjectsOpen"


class RecentProjectsOpen(FlowLauncher):
    def __init__(self):
        super().__init__()
        self.context = {}

    def query(self, param: str) -> list[dict[str, str]]:
        args = param.strip()

        # 如果没有输入参数，则根据 suggestions_list 展示建议列表
        if len(args) == 0:
            return SuggestionService.build(config)

        acronyms = args.split(" ")[0]
        acronyms_dict = AcronymService.get_map(config)

        if acronyms not in acronyms_dict:
            return MessageDTO.asWarnFlowMessage(
                f"{acronyms} is not supported",
                "Please input your software acronyms",
            )
        else:
            app_name = acronyms_dict[acronyms]
        app_icon = icon_path(app_name)
        query = "".join(args.split(" ")[1:])

        # 读取配置：键名由 naming 模块统一生成，避免三处字符串各写一遍
        download_key, storage_key = config_keys(app_name)
        app_download = config.get(download_key)
        app_storage = config.get(storage_key)
        if not app_download or not app_storage:
            return MessageDTO.asWarnFlowMessage(
                f"{app_name} app_download or app_storage is None",
                "Please check your settings",
            )

        # 读取recent_projects
        try:
            app = ConcreteFactory.create_app(app_name, app_download, app_storage)
            projects = app.get_projects()
            res = Fuzzy_Filter.query_filter(query, projects)  # 项目查询结果
        except NotImplementedError:
            return MessageDTO.asWarnFlowMessage(
                "this app is not supported", "Welcome to provide PR"
            )
        except FileNotFoundError as exc:
            return MessageDTO.asWarnFlowMessage(
                str(exc), "Please check the program path in settings"
            )
        return MessageDTO().asMultiFlowMessage(
            projects=res,
            icopath=app_icon,
            method="cmd_command",
            app_download=app_download,
        )

    def context_menu(self, data) -> list:
        """右键菜单：复制路径 / 在资源管理器中打开 / 打开仓库。"""
        path = self._extract_path(data)
        normalized = os.path.normpath(path) if path else ""

        items = []
        if normalized:
            items.append(
                {
                    "Title": "Copy path",
                    "SubTitle": "Press enter to copy the path",
                    "IcoPath": APP_ICON,
                    "jsonRPCAction": {
                        "method": "copy_to_clipboard",
                        "parameters": [normalized],
                    },
                }
            )
            if os.path.exists(normalized):
                items.append(
                    {
                        "Title": "Open in explorer",
                        "SubTitle": "Press enter to open the explorer",
                        "IcoPath": APP_ICON,
                        "jsonRPCAction": {
                            "method": "open_in_explorer",
                            "parameters": [normalized],
                        },
                    }
                )
        items.append(
            {
                "Title": "RecentProjectsOpen",
                "SubTitle": "Press enter to open the plugin repository on GitHub",
                "IcoPath": APP_ICON,
                "jsonRPCAction": {"method": "open_url", "parameters": [REPO_URL]},
            }
        )
        return items

    @staticmethod
    def _extract_path(data) -> str:
        """ContextData 自 1.4.0 起为 {"command": [...], "path": ...}，同时兼容旧的命令数组。"""
        if isinstance(data, dict):
            return str(data.get("path") or "")
        if isinstance(data, (list, tuple)) and data:
            # 旧格式：命令数组，最后一个参数始终是项目路径（含 VSCode SSH）
            return str(data[-1])
        return ""

    def open_in_explorer(self, path: str):
        """目录直接打开；文件则打开其所在目录。"""
        target = path if os.path.isdir(path) else os.path.dirname(path)
        if target:
            os.startfile(target)

    def open_url(self, url):
        webbrowser.open(url)

    def cmd_command(self, *args):
        """
        ["D:/IntelliJ IDEA 2024.3/bin/idea64.exe", "D:/Project/CloneProject/JavaProject/LeetcodeHot"]
        """
        _ = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )

    def copy_to_clipboard(self, text: str):
        copy_text(text)
