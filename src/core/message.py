from .logger import get_logger
from .project import Project

logger = get_logger()


class MessageDTO:
    """消息传输对象"""

    @staticmethod
    def asMultiFlowMessage(
        projects: list[Project], icopath, method: str, app_download: str
    ) -> list:
        message_list = []

        titles = [project.name for project in projects]
        subtitles = [project.path for project in projects]
        # jsonRPCAction参数
        parameters = []
        for project in projects:
            command = project.get_command(app_download)
            parameters.append({"ContentData": command, "parameters": command})

        for i in range(len(titles)):
            message_list.append(
                {
                    "Title": titles[i],  # unquote指示中文转码
                    "SubTitle": subtitles[i],
                    "IcoPath": icopath,
                    "ContextData": parameters[i]["ContentData"],
                    "jsonRPCAction": {
                        "method": method,
                        "parameters": parameters[i]["parameters"],
                    },
                }
            )
        return message_list

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
