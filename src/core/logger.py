import atexit
import logging
import time
from pathlib import Path

LOG_PATH = Path(__file__).parent.parent / "logs"


def get_logger(log_path=None):
    if not log_path:
        log_path = LOG_PATH
    else:
        log_path = Path(log_path)
    log_path.mkdir(parents=True, exist_ok=True)
    logname = str(log_path.joinpath("chat_%s.log" % time.strftime("%Y_%m_%d")))
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s"
    )

    # 创建并配置处理器
    if not logger.handlers:
        fh = logging.FileHandler(logname, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


def close_logger():
    """关闭所有日志处理器，释放资源"""
    logger = logging.getLogger()
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)


atexit.register(close_logger)
