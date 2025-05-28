#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
样式表模块
"""


def get_dark_style():
    """获取暗色主题样式表"""
    return """
    /* 全局样式 */
    QWidget {
        background-color: #2D2D30;
        color: #E0E0E0;
        font-family: "Microsoft YaHei", "Segoe UI", Arial;
    }
    
    /* 主窗口 */
    QMainWindow {
        background-color: #252526;
    }
    
    /* 按钮样式 */
    QPushButton {
        background-color: #0078D7;
        color: white;
        border: none;
        padding: 6px 12px;
        border-radius: 3px;
    }
    
    QPushButton:hover {
        background-color: #1C97EA;
    }
    
    QPushButton:pressed {
        background-color: #00588A;
    }
    
    QPushButton:disabled {
        background-color: #3D3D3D;
        color: #787878;
    }
    
    /* 工具栏 */
    QToolBar {
        background-color: #2D2D30;
        spacing: 6px;
        padding: 3px;
        border: none;
    }
    
    QToolBar::separator {
        background-color: #3D3D3D;
        width: 1px;
        margin: 4px 8px;
    }
    
    /* 菜单 */
    QMenu {
        background-color: #2D2D30;
        border: 1px solid #3E3E40;
    }
    
    QMenu::item {
        padding: 5px 30px 5px 20px;
    }
    
    QMenu::item:selected {
        background-color: #3E3E40;
    }
    
    /* 选项卡 */
    QTabWidget::pane {
        border: 1px solid #3E3E40;
    }
    
    QTabBar::tab {
        background-color: #2D2D30;
        padding: 8px 16px;
        margin-right: 2px;
        border: none;
        border-bottom: 2px solid transparent;
    }
    
    QTabBar::tab:selected {
        background-color: #1E1E1E;
        border-bottom: 2px solid #0078D7;
    }
    
    QTabBar::tab:hover:!selected {
        background-color: #3E3E40;
    }
    
    /* 分组框 */
    QGroupBox {
        background-color: #252526;
        border: 1px solid #3E3E40;
        border-radius: 5px;
        margin-top: 15px;
        padding-top: 15px;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0 5px;
        color: #E0E0E0;
    }
    
    /* 列表 */
    QListWidget {
        background-color: #252526;
        border: 1px solid #3E3E40;
        alternate-background-color: #2A2A2A;
    }
    
    QListWidget::item {
        padding: 5px;
    }
    
    QListWidget::item:selected {
        background-color: #0078D7;
        color: white;
    }
    
    QListWidget::item:hover:!selected {
        background-color: #3E3E40;
    }
    
    /* 表格 */
    QTableWidget {
        background-color: #252526;
        border: 1px solid #3E3E40;
        gridline-color: #3E3E40;
    }
    
    QTableWidget::item {
        padding: 5px;
    }
    
    QTableWidget::item:selected {
        background-color: #0078D7;
        color: white;
    }
    
    QHeaderView::section {
        background-color: #2D2D30;
        padding: 5px;
        border: none;
        border-bottom: 1px solid #3E3E40;
        border-right: 1px solid #3E3E40;
    }
    
    /* 滚动条 */
    QScrollBar:vertical {
        border: none;
        background-color: #2D2D30;
        width: 10px;
        margin: 0px 0px 0px 0px;
    }
    
    QScrollBar::handle:vertical {
        background-color: #3E3E40;
        min-height: 20px;
        border-radius: 5px;
    }
    
    QScrollBar::handle:vertical:hover {
        background-color: #525252;
    }
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }
    
    QScrollBar:horizontal {
        border: none;
        background-color: #2D2D30;
        height: 10px;
        margin: 0px 0px 0px 0px;
    }
    
    QScrollBar::handle:horizontal {
        background-color: #3E3E40;
        min-width: 20px;
        border-radius: 5px;
    }
    
    QScrollBar::handle:horizontal:hover {
        background-color: #525252;
    }
    
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
        width: 0px;
    }
    
    /* 输入框 */
    QLineEdit, QTextEdit, QPlainTextEdit {
        background-color: #1E1E1E;
        color: #E0E0E0;
        border: 1px solid #3E3E40;
        border-radius: 3px;
        padding: 5px;
    }
    
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
        border: 1px solid #0078D7;
    }
    
    /* 组合框和下拉框 */
    QComboBox {
        background-color: #1E1E1E;
        color: #E0E0E0;
        border: 1px solid #3E3E40;
        border-radius: 3px;
        padding: 5px;
    }
    
    QComboBox::drop-down {
        width: 20px;
        border: none;
        background-color: #0078D7;
    }
    
    QComboBox::down-arrow {
        image: url(dropdown_arrow.png);
    }
    
    QComboBox QAbstractItemView {
        background-color: #1E1E1E;
        color: #E0E0E0;
        border: 1px solid #3E3E40;
    }
    
    /* 单选和复选框 */
    QCheckBox, QRadioButton {
        spacing: 8px;
    }
    
    QCheckBox::indicator, QRadioButton::indicator {
        width: 16px;
        height: 16px;
    }
    
    QCheckBox::indicator:checked, QRadioButton::indicator:checked {
        background-color: #0078D7;
    }
    
    /* 状态栏 */
    QStatusBar {
        background-color: #2D2D30;
        color: #E0E0E0;
    }
    
    QStatusBar::item {
        border: none;
    }
    
    /* 分割器 */
    QSplitter::handle {
        background-color: #3E3E40;
    }
    
    QSplitter::handle:horizontal {
        width: 2px;
    }
    
    QSplitter::handle:vertical {
        height: 2px;
    }
    
    /* 对话框 */
    QDialog {
        background-color: #2D2D30;
    }
    
    /* 提示框 */
    QToolTip {
        background-color: #2D2D30;
        color: #E0E0E0;
        border: 1px solid #3E3E40;
        padding: 3px;
    }
    """


def get_light_style():
    """获取亮色主题样式表"""
    return """
    /* 全局样式 */
    QWidget {
        background-color: #FAFAFA;
        color: #212121;
        font-family: "Microsoft YaHei", "Segoe UI", Arial;
    }
    
    /* 主窗口 */
    QMainWindow {
        background-color: #F0F0F0;
    }
    
    /* 按钮样式 */
    QPushButton {
        background-color: #0078D7;
        color: white;
        border: none;
        padding: 6px 12px;
        border-radius: 3px;
    }
    
    QPushButton:hover {
        background-color: #1C97EA;
    }
    
    QPushButton:pressed {
        background-color: #00588A;
    }
    
    QPushButton:disabled {
        background-color: #CCCCCC;
        color: #888888;
    }
    
    /* 工具栏 */
    QToolBar {
        background-color: #F0F0F0;
        spacing: 6px;
        padding: 3px;
        border: none;
        border-bottom: 1px solid #E0E0E0;
    }
    
    QToolBar::separator {
        background-color: #E0E0E0;
        width: 1px;
        margin: 4px 8px;
    }
    
    /* 菜单 */
    QMenu {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
    }
    
    QMenu::item {
        padding: 5px 30px 5px 20px;
    }
    
    QMenu::item:selected {
        background-color: #E0E0E0;
    }
    
    /* 选项卡 */
    QTabWidget::pane {
        border: 1px solid #E0E0E0;
    }
    
    QTabBar::tab {
        background-color: #F0F0F0;
        padding: 8px 16px;
        margin-right: 2px;
        border: none;
        border-bottom: 2px solid transparent;
    }
    
    QTabBar::tab:selected {
        background-color: #FFFFFF;
        border-bottom: 2px solid #0078D7;
    }
    
    QTabBar::tab:hover:!selected {
        background-color: #E0E0E0;
    }
    
    /* 分组框 */
    QGroupBox {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 5px;
        margin-top: 15px;
        padding-top: 15px;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0 5px;
        color: #212121;
    }
    
    /* 列表 */
    QListWidget {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        alternate-background-color: #F5F5F5;
    }
    
    QListWidget::item {
        padding: 5px;
    }
    
    QListWidget::item:selected {
        background-color: #0078D7;
        color: white;
    }
    
    QListWidget::item:hover:!selected {
        background-color: #E0E0E0;
    }
    
    /* 表格 */
    QTableWidget {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        gridline-color: #E0E0E0;
    }
    
    QTableWidget::item {
        padding: 5px;
    }
    
    QTableWidget::item:selected {
        background-color: #0078D7;
        color: white;
    }
    
    QHeaderView::section {
        background-color: #F0F0F0;
        padding: 5px;
        border: none;
        border-bottom: 1px solid #E0E0E0;
        border-right: 1px solid #E0E0E0;
    }
    
    /* 滚动条 */
    QScrollBar:vertical {
        border: none;
        background-color: #F0F0F0;
        width: 10px;
        margin: 0px 0px 0px 0px;
    }
    
    QScrollBar::handle:vertical {
        background-color: #CCCCCC;
        min-height: 20px;
        border-radius: 5px;
    }
    
    QScrollBar::handle:vertical:hover {
        background-color: #AAAAAA;
    }
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }
    
    QScrollBar:horizontal {
        border: none;
        background-color: #F0F0F0;
        height: 10px;
        margin: 0px 0px 0px 0px;
    }
    
    QScrollBar::handle:horizontal {
        background-color: #CCCCCC;
        min-width: 20px;
        border-radius: 5px;
    }
    
    QScrollBar::handle:horizontal:hover {
        background-color: #AAAAAA;
    }
    
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
        width: 0px;
    }
    
    /* 输入框 */
    QLineEdit, QTextEdit, QPlainTextEdit {
        background-color: #FFFFFF;
        color: #212121;
        border: 1px solid #E0E0E0;
        border-radius: 3px;
        padding: 5px;
    }
    
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
        border: 1px solid #0078D7;
    }
    
    /* 组合框和下拉框 */
    QComboBox {
        background-color: #FFFFFF;
        color: #212121;
        border: 1px solid #E0E0E0;
        border-radius: 3px;
        padding: 5px;
    }
    
    QComboBox::drop-down {
        width: 20px;
        border: none;
        background-color: #0078D7;
    }
    
    QComboBox::down-arrow {
        image: url(dropdown_arrow.png);
    }
    
    QComboBox QAbstractItemView {
        background-color: #FFFFFF;
        color: #212121;
        border: 1px solid #E0E0E0;
    }
    
    /* 单选和复选框 */
    QCheckBox, QRadioButton {
        spacing: 8px;
    }
    
    QCheckBox::indicator, QRadioButton::indicator {
        width: 16px;
        height: 16px;
    }
    
    QCheckBox::indicator:checked, QRadioButton::indicator:checked {
        background-color: #0078D7;
    }
    
    /* 状态栏 */
    QStatusBar {
        background-color: #F0F0F0;
        color: #212121;
        border-top: 1px solid #E0E0E0;
    }
    
    QStatusBar::item {
        border: none;
    }
    
    /* 分割器 */
    QSplitter::handle {
        background-color: #E0E0E0;
    }
    
    QSplitter::handle:horizontal {
        width: 2px;
    }
    
    QSplitter::handle:vertical {
        height: 2px;
    }
    
    /* 对话框 */
    QDialog {
        background-color: #FAFAFA;
    }
    
    /* 提示框 */
    QToolTip {
        background-color: #FFFFFF;
        color: #212121;
        border: 1px solid #E0E0E0;
        padding: 3px;
    }
    """
