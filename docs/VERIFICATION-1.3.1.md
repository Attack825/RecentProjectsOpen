# 1.3.1 验证记录（Proof）

本文件记录 1.3.1 修复的验证证据，命令均可复现。

## 1. 线上故障复现与修复（issue #10 / #11）

**故障**：Flow Launcher 把 JSON-RPC 插件进程的任何 stderr 输出视为失败
（`JsonRPCPlugin.ExecuteAsync: case (_, not 0) => throw new InvalidDataException`），
而 1.3.0 的发布包在 Windows 上无法加载随包的 Linux `.so`，导致 `fuzzywuzzy` 回落到
difflib 并输出 `UserWarning`。

**复现环境**：真实 v1.3.0 发布包（SHA256 `9695485C…398A5`），CPython 3.9.13 / 3.13.5，
用复刻 Flow `Process.Start` + 双流重定向 + 同一 `switch` 的 .NET harness 驱动。

| 场景 | 退出码 | stdout | stderr | Flow 侧结果 |
| --- | --- | --- | --- | --- |
| v1.3.0 产物 + CPython 3.13 | 0 | 949 B 合法 JSON | 258 B 警告 | `FlowPluginException` |
| v1.3.0 产物 + CPython 3.9 | 0 | 949 B 合法 JSON | 258 B 警告 | `FlowPluginException` |
| 1.3.1 产物 + CPython 3.13 | 0 | 949 B 合法 JSON | **0 B** | 解析成功，result=3 |
| 1.3.1 产物 + CPython 3.9 | 0 | 949 B 合法 JSON | **0 B** | 解析成功，result=3 |

发布包冒烟测试同时覆盖 3.9 / 3.11 / 3.13：

```text
PASS [python=3.9.13]: result=1
PASS [python=3.11.1]: result=1
PASS [python=3.13.5]: result=1
```

## 2. 发布包体积与可移植性

| 指标 | v1.3.0 | 1.3.1 |
| --- | --- | --- |
| zip 大小 | 26,101,527 B | 1,434,664 B |
| `lib/` 平台相关二进制 | 10 个 `*-linux-gnu.so` | 0 |
| 运行时依赖 | 19 个包（含 ruff / pre-commit / virtualenv） | 3 个包（flowlauncher / pypinyin / typing_extensions） |

## 3. 质量门禁

| 检查 | v1.3.0 | 1.3.1 |
| --- | --- | --- |
| ruff（0.17.6 默认规则） | 70 条告警 | 0 |
| ruff format | 通过 | 通过 |
| unittest | 19 用例（本地 18 通过） | 40 用例，3.9/3.11/3.13 全通过 |

## 4. 复现命令

```bash
# 单测（3.9 / 3.11 / 3.13）
python -m unittest discover -s test -p "test_*.py"

# lint
ruff check . && ruff format --check .

# 发布产物冒烟
python tools/smoke_test.py RecentProjectsOpen.zip --python python
```
