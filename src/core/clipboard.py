"""Windows 剪贴板读写。

Flow Launcher 只支持 Windows，直接调用 Win32 API：
- 不走 shell，避免 `echo | clip` 对引号 / & / | 的注入与截断
- 显式 UTF-16LE + CF_UNICODETEXT，中文不会被控制台代码页破坏
"""

import ctypes
import sys
import time

CF_UNICODETEXT = 13
GMEM_MOVEABLE = 0x0002
OPEN_RETRIES = 5
OPEN_RETRY_DELAY = 0.05


def _win32():
    if sys.platform != "win32":
        raise RuntimeError("clipboard is only supported on Windows")
    return ctypes.windll.user32, ctypes.windll.kernel32


def _open_clipboard(user32) -> bool:
    """剪贴板可能被其他进程短暂占用，重试几次再失败。"""
    for _ in range(OPEN_RETRIES):
        if user32.OpenClipboard(None):
            return True
        time.sleep(OPEN_RETRY_DELAY)
    return False


def copy_text(text: str) -> None:
    """把文本写入系统剪贴板。"""
    user32, kernel32 = _win32()
    kernel32.GlobalAlloc.restype = ctypes.c_void_p
    kernel32.GlobalAlloc.argtypes = [ctypes.c_uint, ctypes.c_size_t]
    kernel32.GlobalLock.restype = ctypes.c_void_p
    kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
    kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
    user32.SetClipboardData.restype = ctypes.c_void_p
    user32.SetClipboardData.argtypes = [ctypes.c_uint, ctypes.c_void_p]

    if not _open_clipboard(user32):
        raise OSError("cannot open clipboard")
    try:
        user32.EmptyClipboard()
        data = text.encode("utf-16-le") + b"\x00\x00"
        handle = kernel32.GlobalAlloc(GMEM_MOVEABLE, len(data))
        if not handle:
            raise OSError("GlobalAlloc failed")
        pointer = kernel32.GlobalLock(handle)
        if not pointer:
            raise OSError("GlobalLock failed")
        ctypes.memmove(pointer, data, len(data))
        kernel32.GlobalUnlock(handle)
        if not user32.SetClipboardData(CF_UNICODETEXT, handle):
            raise OSError("SetClipboardData failed")
    finally:
        user32.CloseClipboard()


def read_text() -> str:
    """读取剪贴板文本（主要供测试与诊断使用）。"""
    user32, kernel32 = _win32()
    user32.GetClipboardData.restype = ctypes.c_void_p
    user32.GetClipboardData.argtypes = [ctypes.c_uint]
    kernel32.GlobalLock.restype = ctypes.c_void_p
    kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
    kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]

    if not _open_clipboard(user32):
        raise OSError("cannot open clipboard")
    try:
        handle = user32.GetClipboardData(CF_UNICODETEXT)
        if not handle:
            return ""
        pointer = kernel32.GlobalLock(handle)
        if not pointer:
            return ""
        try:
            return ctypes.wstring_at(pointer)
        finally:
            kernel32.GlobalUnlock(handle)
    finally:
        user32.CloseClipboard()
