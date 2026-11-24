from .logger import get_logger
from .project import Project

logger = get_logger()


class MessageDTO:
    """消息传输对象"""

    @staticmethod
    def asMultiFlowMessage(
        projects: list[Project], icopath, method: str, app_download: str
    ) -> list:
        return [
            MessageDTO._to_message(project, icopath, method, app_download)
            for project in projects
        ]

    @staticmethod
    def _to_message(project: Project, icopath, method: str, app_download: str) -> dict:
        command = project.get_command(app_download)
        return {
            "Title": project.name,  # unquote指示中文转码
            "SubTitle": project.path,
            "IcoPath": icopath,
            # 1.4.0 起 ContextData 结构化为 {command, path}，context_menu 不再猜哪个参数是路径
            "ContextData": {"command": command, "path": project.path},
            "jsonRPCAction": {"method": method, "parameters": command},
        }

    @staticmethod
    def asWarnFlowMessage(title, subTitle) -> list:
        return [
            {
                "Title": title,
                "SubTitle": subTitle,
                "IcoPath": "icons/warn.png",
            }
        ]

    @staticmethod
    def asDebugFlowMessage(msg) -> list:
        return [
            {
                "Title": msg,
                "SubTitle": "Debug",
                "IcoPath": "icons/app.png",
            }
        ]
