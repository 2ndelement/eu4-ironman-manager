#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
欧陆风云IV (EU4) 存档管理器
author: GitHub Copilot
date: 2025-05-28
"""

import sys
import os
from PySide6.QtWidgets import QApplication
from src.main_window import MainWindow
from src.config import setup_logging, create_config_if_not_exists

if __name__ == "__main__":
    # 设置日志
    setup_logging()

    # 创建配置文件（如果不存在）
    create_config_if_not_exists()

    # 创建Qt应用
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # 使用Fusion风格，更现代化的界面

    # 设置应用信息
    app.setApplicationName("EU4存档管理器")
    app.setApplicationVersion("1.0.0")

    # 创建主窗口并显示
    window = MainWindow()
    window.show()

    # 运行应用程序事件循环
    sys.exit(app.exec())
