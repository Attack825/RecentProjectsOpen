import json
import os
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOCK_XML = os.path.join(ROOT, "test", "mock_data", "test_jetbrains_recent_project.xml")


def _settings():
    return {
        "program_path": (
            "INTELLIJ_IDEA_DOWNLOAD=C:/fake/idea64.exe\n"
            f"INTELLIJ_IDEA_STORAGE={MOCK_XML}"
        ),
        "suggestions_list": "",
        "plugin_trigger_keyword": "r",
        "custom_acronyms_map": "",
    }


class JsonRpcChannelTest(unittest.TestCase):
    """Flow Launcher 的 JSON-RPC 契约：stdout 只能是 JSON，stderr 必须为空。

    JsonRPCPlugin.ExecuteAsync 的判定是 `switch (stdout.Length, stderr.Length)`，
    只要 stderr 有任意字节就会抛 InvalidDataException，并丢弃已经产生的 stdout。
    """

    def _run(self, query, extra_env=None):
        request = json.dumps(
            {"method": "query", "parameters": [query], "settings": _settings()}
        )
        env = os.environ.copy()
        env.setdefault("PYTHONIOENCODING", "utf-8")
        if extra_env:
            env.update(extra_env)
        return subprocess.run(
            [sys.executable, os.path.join(ROOT, "main.py"), request],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=120,
            env=env,
        )

    def test_query_writes_only_json_to_stdout(self):
        proc = self._run("idea")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertGreaterEqual(len(payload["result"]), 1)

    def test_stderr_stays_empty_even_with_warnings_enabled(self):
        proc = self._run("idea", {"PYTHONWARNINGS": "always"})
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(
            proc.stderr, "", "stderr 非空会让 Flow 抛出 InvalidDataException"
        )
