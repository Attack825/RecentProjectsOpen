from .acronyms import AcronymService
from .naming import config_keys, icon_path


class SuggestionService:
    """空查询时展示的应用建议（Flow 的 ChangeQuery 补全项）。"""

    @classmethod
    def build(cls, plugin_config) -> list[dict]:
        suggestions = plugin_config.get("suggestions_list")
        trigger = plugin_config.get("plugin_trigger_keyword", "r")
        acronyms = AcronymService.get_map(plugin_config)
        reverse = {prog: acr for acr, prog in acronyms.items()}

        if suggestions is None:
            suggestions = []
            for program in acronyms.values():
                download_key, storage_key = config_keys(program)
                if download_key in plugin_config and storage_key in plugin_config:
                    suggestions.append(program)

        messages = []
        for idx, program in enumerate(suggestions):
            acronym = reverse.get(program)
            if acronym is None:
                continue
            messages.append(
                {
                    "title": program,
                    "subTitle": acronym,
                    "icoPath": icon_path(program),
                    "jsonRPCAction": {
                        "method": "Flow.Launcher.ChangeQuery",
                        "parameters": [f"{trigger} {acronym} ", False],
                        "dontHideAfterAction": True,
                    },
                    # 按原始顺序排序
                    "score": (100 - idx) * 10000,
                }
            )
        return messages
