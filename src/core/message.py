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
            {
                "Title": project.name,  # unquote指示中文转码
                "SubTitle": project.path,
                "IcoPath": icopath,
                "ContextData": project.get_command(app_download),
                "jsonRPCAction": {
                    "method": method,
                    "parameters": project.get_command(app_download),
                },
            }
            for project in projects
        ]

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
