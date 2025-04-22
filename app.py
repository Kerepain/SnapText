"""
SnapText - 批量图片文字处理工具
主程序入口
"""
import sys
import os

# 将项目根目录添加到模块搜索路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from src.utils.logger import logger

def main():
    """程序入口函数"""
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        logger.critical(f"应用程序异常: {str(e)}")
        raise

if __name__ == "__main__":
    main() 