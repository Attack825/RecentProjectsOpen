import os
import sys
import warnings

parent_folder_path = os.path.abspath(os.path.dirname(__file__))
log_folder_path = os.path.join(parent_folder_path, "logs")
os.makedirs(log_folder_path, exist_ok=True)

# Flow Launcher 会把子进程的任何 stderr 输出当作插件失败：
#   JsonRPCPlugin.ExecuteAsync: case (_, not 0) => throw new InvalidDataException(stderr)
# 一旦 stderr 非空，即使 stdout 已经输出了合法 JSON，本次查询也会被丢弃。
# 因此插件必须保证 stderr 始终为空：先压制所有 warning，再把残余输出重定向到日志文件。
warnings.filterwarnings("ignore")
sys.stderr = open(  # noqa: SIM115 - 必须与进程同生命周期，不能提前关闭
    os.path.join(log_folder_path, "stderr.log"), "a", buffering=1, encoding="utf-8"
)

sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, "lib"))
sys.path.append(os.path.join(parent_folder_path, "src"))

from src.core.main import RecentProjectsOpen  # noqa: E402

if __name__ == "__main__":
    RecentProjectsOpen()
