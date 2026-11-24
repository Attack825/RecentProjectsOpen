# 1.4.0 验证记录（Proof）

本轮为架构整理（13.2 的 6 项），排序抽象按决策**不做**。以下证据均在 Windows 本机实测。

## 1. 统一错误模型

同一请求（TYPORA_STORAGE 指向不存在的文件）：

| 版本 | 适配器行为 | query 输出 |
| --- | --- | --- |
| 1.3.x | `get_projects()` 返回 `[]` | `{"result": []}`（静默无提示） |
| 1.4.0 | 抛 `StorageFileNotFound("TYPORA: storage file not found: ...")` | 1 条 warn 项，Title 含应用名与路径 |

## 2. ContextData 与右键菜单

| 输入 | 1.3.x | 1.4.0 |
| --- | --- | --- |
| `{"command": [...], "path": ...}` | `KeyError: 1` | `["copy_to_clipboard", "open_url"]` |
| 旧命令数组（VSCode SSH） | `TypeError: asWarnFlowMessage() missing 1 required positional argument` | `["copy_to_clipboard", "open_url"]` |
| `None` | `KeyError: 'jsonRPCAction'` | `["open_url"]` |

含空格/中文路径、反斜杠路径均由 `os.path.normpath` + `os.path.exists` 处理；
路径存在时才出现 "Open in explorer"。

## 3. 剪贴板

| 版本 | 输入 `a & b | c "quoted" 中文` 回读 |
| --- | --- |
| 1.3.x（echo \| clip） | `'"a & b | c \"quoted\" 中文" \r\n'`（被 shell 改写） |
| 1.4.0（Win32 API） | 与输入完全相等 |

## 4. 工厂拆分等价性

4 组配置（显式建议 / 自动推断 / 自定义缩写 / 未注册程序）分别调用旧
`ConcreteFactory.get_application_acronyms` + `get_application_message` 与新
`AcronymService.get_map` + `SuggestionService.build`，输出 JSON 的 SHA256 相同。

## 5. 类型基线

| 指标 | 接入前 | 接入后 |
| --- | --- | --- |
| mypy 错误 | 11（registry 1 + typora 10） | 0（30 个源文件） |
| ruff | 0 | 0 |
| unittest | 40 | 58（9 个模块） |

CPython 3.9.13 / 3.11.1 / 3.13.5 均通过。

## 6. 端到端

Flow harness（复刻 `JsonRPCPlugin.ExecuteAsync`）运行 query `idea`：
exit=0、stderr=0B、result=3。
