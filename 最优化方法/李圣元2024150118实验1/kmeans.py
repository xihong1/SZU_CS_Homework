import pyperclip
import time
import threading

def _safe_update_text(content: str) -> None:
    """安全地更新文本控件"""
    print(content)

class ClipboardMonitor:
    def __init__(self) -> None:
        # 初始化，记录上一次的内容
        self.previous_clipboard_content = pyperclip.paste()

        # 在单独的线程中启动监控
        self.monitoring_thread = threading.Thread(target=self.monitor_clipboard, daemon=True)
        self.monitoring_thread.start()

    def monitor_clipboard(self) -> None:
        """在后台线程中监控剪贴板"""
        while True:
            try:
                current_clipboard_content = pyperclip.paste()  # 获取剪贴板内容
                # 如果内容发生变化且不为空
                if (current_clipboard_content != self.previous_clipboard_content and
                        current_clipboard_content.strip() != ""):
                    self.previous_clipboard_content = current_clipboard_content
                    _safe_update_text(current_clipboard_content)
                time.sleep(0.5)  # 每秒检查2次
            except Exception as e:
                error_msg = f"读取剪贴板出错: {e}"
                print(error_msg)
                time.sleep(1)


def main() -> None:
    """主函数，避免全局变量污染"""
    monitor = ClipboardMonitor()
    monitor.monitoring_thread.join()

if __name__ == "__main__":
    main()