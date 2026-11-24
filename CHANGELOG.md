# Changelog

## [1.4.0] - 2026-11-24

架构整理版本，无用户可见的新功能；行为变化均为缺陷修复。

### Changed

- 统一错误模型：所有应用适配器在存储文件缺失时抛 `StorageFileNotFound`，
  由 `query` 转成带路径的提示项，不再出现"有的报错、有的静默返回空列表"
- `ConcreteFactory` 拆分为 `AcronymService`（缩写表）与 `SuggestionService`（建议项），
  工厂只负责实例化
- 配置键 `<APP>_DOWNLOAD` / `<APP>_STORAGE` 与 `icons/<APP>.png` 收敛到 `src/core/naming.py`，
  新增 `BaseApplication.validate_storage()`
- `ContextData` 结构化为 `{"command": ..., "path": ...}`，右键菜单不再依赖参数位置

### Fixed

- 右键菜单在含空格/中文路径、VSCode SSH、无效数据时崩溃（原实现用正则 + `data[1]`）
- "Copy path" 在文本含 `&`、`|`、引号时被 shell 改写；改用 Win32 剪贴板 API
- `os.startfile` 打开资源管理器，路径含空格不再被拆分

### Tooling

- 接入 mypy 1.13 基线（`python_version=3.9`、`platform=win32`），CI lint job 执行
- 测试从 40 增至 58 个，新增剪贴板、右键菜单、naming、服务层用例

### Not done

- 统一"最近使用"排序：三类数据源时间语义不一致，明确不做（见 docs/ARCHITECTURE.md 13.2）

## [1.3.1] - 2026-11-24

### Fixed

- Windows 上 `fuzzywuzzy` 的 `UserWarning` 写入 stderr，被 Flow 判为失败并抛
  `FlowPluginException`（#10、#11）：入口抑制 warning 并隔离 stderr
- `print()` 污染 stdout，导致 JSON 解析失败
- 模糊匹配第二参传字符串（按字符比较）且阈值 `> 90` 永不命中：改用标准库 `difflib`

### Changed

- 发布包改为 Windows 构建 + 纯 Python 依赖，移除 `Levenshtein` / `RapidFuzz` / `PyYAML` / `click`
- 删除 `fuzzywuzzy`，运行时依赖从 19 个降至 3 个；zip 从 26.1 MB 降至 1.4 MB
- CI 覆盖 Python 3.9 / 3.11 / 3.13；发布前对产物做冒烟测试
- 架构文档入库
