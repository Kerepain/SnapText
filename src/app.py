#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SnapText - 批量图片文字处理工具
主程序入口
"""
import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from src.config.constants import APP_NAME, APP_VERSION
from src.ui.main_window import MainWindow
from src.utils.logger import Logger
from src.utils.file_utils import get_resource_path

def main():
    """
    主程序入口函数。
    初始化应用程序，设置图标，创建主窗口，并处理异常。
    """
    # 初始化日志
    logger = Logger()
    logger.info(f"启动 {APP_NAME} v{APP_VERSION}")
    
    try:
        # 创建应用程序
        app = QApplication(sys.argv)
        app.setApplicationName(APP_NAME)
        
        # 设置应用图标
        icon_path = get_resource_path('assets/icon.png')
        if os.path.exists(icon_path):
            app.setWindowIcon(QIcon(icon_path))
        else:
            logger.warning(f"找不到图标文件: {icon_path}")
        
        # 创建主窗口
        window = MainWindow()
        window.show()
        
        # 启动应用程序事件循环
        exit_code = app.exec()
        logger.info(f"应用程序退出，状态码: {exit_code}")
        return exit_code
        
    except Exception as e:
        logger.error(f"应用程序发生错误: {str(e)}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main()) 