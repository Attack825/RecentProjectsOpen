"""发布产物冒烟测试。

流程：解包 zip -> 校验 lib 中无平台相关二进制 -> 用给定解释器执行一次 query
     -> 断言退出码为 0、stderr 为空、stdout 是合法 JSON 且 result 非空。

Flow Launcher 的 JSON-RPC 契约要求 stderr 必须为空（JsonRPCPlugin.ExecuteAsync），
因此这里把 stderr 作为硬性断言，防止"源码绿、产物坏"再次发生。

用法：
    python tools/smoke_test.py RecentProjectsOpen.zip --python python
    python tools/smoke_test.py RecentProjectsOpen.zip --python 3.9 --python 3.13
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import zipfile

MOCK_RECENT_PROJECTS = """<?xml version="1.0" encoding="UTF-8"?>
<application>
  <component name="RecentProjectsManager">
    <option name="additionalInfo">
      <map>
        <entry key="D:/smoke/demo-project">
          <value><RecentProjectMetaInfo frameTitle="demo" /></value>
        </entry>
      </map>
    </option>
  </component>
</application>
"""

NATIVE_SUFFIXES = (".pyd", ".so", ".dll", ".dylib")


def find_native_binaries(root):
    return [
        os.path.join(dirpath, name)
        for dirpath, _dirnames, filenames in os.walk(os.path.join(root, "lib"))
        for name in filenames
        if name.lower().endswith(NATIVE_SUFFIXES)
    ]


def build_request(storage_file):
    program_path = (
        "INTELLIJ_IDEA_DOWNLOAD=C:/smoke/idea64.exe\n"
        f"INTELLIJ_IDEA_STORAGE={storage_file}"
    )
    return json.dumps(
        {
            "method": "query",
            "parameters": ["idea"],
            "settings": {"program_path": program_path},
        }
    )


def run_case(python, plugin_dir, request):
    proc = subprocess.run(
        [python, os.path.join(plugin_dir, "main.py"), request],
        cwd=plugin_dir,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=120,
    )
    return proc


def main():
    parser = argparse.ArgumentParser(description="Flow Launcher 插件发布产物冒烟测试")
    parser.add_argument("zip_path", help="待验证的发布包")
    parser.add_argument(
        "--python",
        action="append",
        dest="pythons",
        help="用于运行插件的解释器，可重复指定（默认当前解释器）",
    )
    args = parser.parse_args()
    pythons = args.pythons or [sys.executable]

    failures = []
    with tempfile.TemporaryDirectory(prefix="rpo-smoke-") as tmp:
        with zipfile.ZipFile(args.zip_path) as zf:
            zf.extractall(tmp)

        if not os.path.isfile(os.path.join(tmp, "main.py")):
            print("FAIL: 发布包根目录缺少 main.py")
            return 1

        native = find_native_binaries(tmp)
        if native:
            print("FAIL: lib 中存在平台相关二进制（不可移植）：")
            for path in native:
                print("  -", os.path.relpath(path, tmp))
            failures.append("native-binaries")

        storage = os.path.join(tmp, "smoke-recent-projects.xml")
        with open(storage, "w", encoding="utf-8") as fh:
            fh.write(MOCK_RECENT_PROJECTS)
        request = build_request(storage)

        for python in pythons:
            label = "python=" + python
            try:
                proc = run_case(python, tmp, request)
            except (OSError, subprocess.TimeoutExpired) as exc:
                print(f"FAIL [{label}]: 无法执行插件：{exc}")
                failures.append(label)
                continue

            if proc.returncode != 0:
                print(f"FAIL [{label}]: 退出码 {proc.returncode}")
                failures.append(label)
                continue
            if proc.stderr != "":
                print(f"FAIL [{label}]: stderr 非空（Flow 会抛 InvalidDataException）")
                print(proc.stderr[:800])
                failures.append(label)
                continue
            try:
                payload = json.loads(proc.stdout)
            except json.JSONDecodeError as exc:
                print(f"FAIL [{label}]: stdout 不是合法 JSON：{exc}")
                print(proc.stdout[:800])
                failures.append(label)
                continue
            if not payload.get("result"):
                print(f"FAIL [{label}]: result 为空")
                failures.append(label)
                continue
            print(f"PASS [{label}]: result={len(payload['result'])}")

    if failures:
        print(f"\n冒烟测试失败：{len(failures)} 项")
        return 1
    print("\n冒烟测试通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
