from .registry import ApplicationRegistry


class AcronymService:
    """缩写表：默认注册表 + 用户自定义，用户自定义优先。"""

    @classmethod
    def get_map(cls, plugin_config) -> dict[str, str]:
        ApplicationRegistry.load_applications()
        default_map = ApplicationRegistry.get_acronyms_map()
        custom_map = plugin_config.get("custom_acronyms_map", {})
        acronyms = {acr: prog.upper() for prog, acr in custom_map.items()}
        for acr, prog in default_map.items():
            if prog not in acronyms.values():
                acronyms[acr] = prog
        return acronyms
