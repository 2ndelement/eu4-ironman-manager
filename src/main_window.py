#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
主窗口模块
"""

import os
import sys
import logging
from datetime import datetime

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSplitter,
    QPushButton,
    QLabel,
    QLineEdit,
    QComboBox,
    QListWidget,
    QListWidgetItem,
    QTabWidget,
    QGroupBox,
    QCheckBox,
    QSpinBox,
    QFileDialog,
    QMessageBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QTextEdit,
    QCompleter,
    QMenu,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)
from PySide6.QtCore import Qt, QSize, QTimer, Signal, QThread, QSettings, QEvent
from PySide6.QtGui import QIcon, QAction, QFont, QColor, QPalette, QPixmap

from src.config import get_config, save_config, get_save_files, format_file_size
from src.backup_manager import BackupManager
from src.styles import get_dark_style, get_light_style


class MainWindow(QMainWindow):
    """主窗口类"""

    def __init__(self):
        super().__init__()

        # 初始化配�?
        self.config = get_config()

        # 初始化备份管理器
        self.backup_manager = BackupManager()
        # 设置窗口属性
        self.setWindowTitle("欧陆风云IV 存档管理器")
        self.setMinimumSize(1000, 600)

        # 加载图标
        icon_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "resources", "icon.ico"
        )
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # 应用主题样式
        self.apply_theme()

        # 设置中心窗口部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 创建布局
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        # 创建界面组件
        self.setup_ui()

        # 加载存档数据
        self.load_save_files()

        # 创建定时器用于自动刷新
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.auto_refresh)
        self.timer.start(60000)  # 1分钟刷新一次

    def setup_ui(self):
        """设置UI界面"""
        # 创建顶部工具栏
        self.create_toolbar()

        # 创建分割器，左边是存档列表，右边是备份详�?
        self.splitter = QSplitter(Qt.Horizontal)
        self.main_layout.addWidget(self.splitter)

        # 左侧存档面板
        self.left_panel = QWidget()
        self.left_layout = QVBoxLayout(self.left_panel)
        self.splitter.addWidget(self.left_panel)

        # 右侧备份面板
        self.right_panel = QWidget()
        self.right_layout = QVBoxLayout(self.right_panel)
        self.splitter.addWidget(self.right_panel)

        # 设置分割器的初始大小
        self.splitter.setSizes([300, 700])

        # 设置左侧面板内容
        self.setup_left_panel()

        # 设置右侧面板内容
        self.setup_right_panel()

        # 创建状态栏
        self.status_bar = self.statusBar()
        self.status_label = QLabel("就绪")
        self.status_bar.addWidget(self.status_label)

    def create_toolbar(self):
        """创建顶部工具栏"""
        self.toolbar = self.addToolBar("工具栏")
        self.toolbar.setMovable(False)
        self.toolbar.setIconSize(QSize(24, 24))

        # 刷新按钮
        refresh_action = QAction("刷新", self)
        refresh_action.triggered.connect(self.load_save_files)
        self.toolbar.addAction(refresh_action)

        # 添加分隔�?
        self.toolbar.addSeparator()

        # 创建备份按钮
        backup_action = QAction("创建备份", self)
        backup_action.triggered.connect(self.create_backup)
        self.toolbar.addAction(backup_action)

        # 恢复备份按钮
        restore_action = QAction("恢复备份", self)
        restore_action.triggered.connect(self.restore_backup)
        self.toolbar.addAction(restore_action)

        # 添加分隔�?
        self.toolbar.addSeparator()

        # 设置按钮
        settings_action = QAction("设置", self)
        settings_action.triggered.connect(self.show_settings)
        self.toolbar.addAction(settings_action)

    def setup_left_panel(self):
        """设置左侧面板内容"""
        # 存档过滤区域
        filter_layout = QHBoxLayout()
        self.left_layout.addLayout(filter_layout)

        filter_label = QLabel("搜索:")
        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText("输入存档名称进行过滤...")
        self.filter_edit.textChanged.connect(self.filter_saves)

        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.filter_edit)

        # 存档列表
        self.save_list = QListWidget()
        self.save_list.setSelectionMode(QListWidget.SingleSelection)
        self.save_list.currentItemChanged.connect(self.on_save_selected)
        self.save_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.save_list.customContextMenuRequested.connect(self.show_save_context_menu)
        self.left_layout.addWidget(self.save_list)

    def setup_right_panel(self):
        """设置右侧面板内容"""
        # 存档信息区域
        self.save_info_group = QGroupBox("存档信息")
        self.save_info_layout = QFormLayout(self.save_info_group)

        self.save_name_label = QLabel("-")
        self.save_size_label = QLabel("-")
        self.save_date_label = QLabel("-")

        self.save_info_layout.addRow("存档名称:", self.save_name_label)
        self.save_info_layout.addRow("文件大小:", self.save_size_label)
        self.save_info_layout.addRow("修改日期:", self.save_date_label)

        self.right_layout.addWidget(self.save_info_group)

        # 备份列表
        self.backup_group = QGroupBox("备份历史")
        backup_layout = QVBoxLayout(self.backup_group)

        # 备份表格
        self.backup_table = QTableWidget()
        self.backup_table.setColumnCount(4)
        self.backup_table.setHorizontalHeaderLabels(
            ["备份时间", "游戏进度", "描述", "大小"]
        )
        self.backup_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeToContents
        )
        self.backup_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeToContents
        )
        self.backup_table.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.Stretch
        )
        self.backup_table.horizontalHeader().setSectionResizeMode(
            3, QHeaderView.ResizeToContents
        )
        self.backup_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.backup_table.setSelectionMode(QTableWidget.SingleSelection)
        self.backup_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.backup_table.customContextMenuRequested.connect(
            self.show_backup_context_menu
        )

        backup_layout.addWidget(self.backup_table)

        # 备份操作按钮区域
        backup_actions_layout = QHBoxLayout()

        self.create_backup_btn = QPushButton("创建备份")
        self.restore_backup_btn = QPushButton("恢复备份")
        self.edit_backup_btn = QPushButton("编辑信息")
        self.delete_backup_btn = QPushButton("删除备份")

        self.create_backup_btn.clicked.connect(self.create_backup)
        self.restore_backup_btn.clicked.connect(self.restore_backup)
        self.edit_backup_btn.clicked.connect(self.edit_backup)
        self.delete_backup_btn.clicked.connect(self.delete_backup)

        backup_actions_layout.addWidget(self.create_backup_btn)
        backup_actions_layout.addWidget(self.restore_backup_btn)
        backup_actions_layout.addWidget(self.edit_backup_btn)
        backup_actions_layout.addWidget(self.delete_backup_btn)

        backup_layout.addLayout(backup_actions_layout)

        self.right_layout.addWidget(self.backup_group)

    def load_save_files(self):
        """加载存档文件"""
        self.save_list.clear()
        save_files = get_save_files()

        if not save_files:
            self.status_label.setText("未找到存档文件")
            return

        for save_file in save_files:
            item = QListWidgetItem(save_file["name"])
            item.setData(Qt.UserRole, save_file)
            self.save_list.addItem(item)

        self.status_label.setText(f"已加载{len(save_files)} 个存档文件")

        # 如果有存档，自动选中第一个存档
        if self.save_list.count() > 0:
            self.save_list.setCurrentRow(0)

    def filter_saves(self):
        """过滤存档列表"""
        filter_text = self.filter_edit.text().lower()

        for i in range(self.save_list.count()):
            item = self.save_list.item(i)
            save_name = item.text().lower()

            if filter_text in save_name:
                item.setHidden(False)
            else:
                item.setHidden(True)

    def on_save_selected(self, current, previous):
        """当选择存档时更新界面信息"""
        if not current:
            self.clear_save_info()
            return

        save_data = current.data(Qt.UserRole)

        # 更新存档信息
        self.save_name_label.setText(save_data["name"])
        self.save_size_label.setText(format_file_size(save_data["size"]))
        self.save_date_label.setText(
            save_data["modified"].strftime("%Y-%m-%d %H:%M:%S")
        )

        # 加载该存档的备份列表
        self.load_backups_for_save(save_data["name"].split(".")[0])

    def load_backups_for_save(self, save_name):
        """加载指定存档的备份列表"""
        self.backup_table.setRowCount(0)

        backups = self.backup_manager.get_backups_for_save(save_name)

        for i, backup in enumerate(backups):
            self.backup_table.insertRow(i)

            # 备份时间
            backup_time = datetime.fromisoformat(backup["time"]).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            time_item = QTableWidgetItem(backup_time)
            self.backup_table.setItem(i, 0, time_item)

            # 游戏进度
            game_date = backup.get("game_date", "-")
            date_item = QTableWidgetItem(game_date)
            self.backup_table.setItem(i, 1, date_item)

            # 备份描述
            desc_item = QTableWidgetItem(backup.get("description", ""))
            self.backup_table.setItem(i, 2, desc_item)

            # 备份大小
            size = backup.get("size", 0)
            size_item = QTableWidgetItem(format_file_size(size))
            self.backup_table.setItem(i, 3, size_item)

            # 存储备份ID
            time_item.setData(Qt.UserRole, backup["id"])

        # 自动调整行高
        self.backup_table.resizeRowsToContents()

    def clear_save_info(self):
        """清除存档信息显示"""
        self.save_name_label.setText("-")
        self.save_size_label.setText("-")
        self.save_date_label.setText("-")
        self.backup_table.setRowCount(0)

    def create_backup(self):
        """创建备份"""
        # 获取当前选中的存档
        current_item = self.save_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "警告", "请先选择一个存档！")
            return

        save_data = current_item.data(Qt.UserRole)

        # 显示备份对话�?
        dialog = BackupDialog(self, save_data["name"])
        if dialog.exec() != QDialog.Accepted:
            return
        # 创建备份
        description = dialog.description_edit.toPlainText()
        tags = [
            tag.strip() for tag in dialog.tags_edit.text().split(",") if tag.strip()
        ]
        game_date = dialog.game_date_edit.text()

        backup_id = self.backup_manager.create_backup(
            save_data["path"], description, tags
        )

        # 如果成功创建备份且输入了游戏时间，则更新元数据
        if backup_id and game_date:
            self.backup_manager.update_backup_metadata(
                backup_id, description=None, tags=None, game_date=game_date
            )

        if backup_id:
            QMessageBox.information(self, "成功", f"成功创建备份: {backup_id}")
            # 刷新备份列表
            self.load_backups_for_save(save_data["name"].split(".")[0])
        else:
            QMessageBox.critical(self, "错误", "创建备份失败，请检查日志获取更多信息。")

    def restore_backup(self):
        """恢复备份"""
        current_row = self.backup_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "请先选择一个备份！")
            return

        backup_id = self.backup_table.item(current_row, 0).data(Qt.UserRole)
        # 显示确认对话�?
        reply = QMessageBox.question(
            self,
            "确认恢复",
            "确定要恢复这个备份吗？当前的存档将被备份的版本覆盖！",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.No:
            return

        # 恢复备份
        if self.backup_manager.restore_backup(backup_id):
            QMessageBox.information(self, "成功", "成功恢复备份！")
        else:
            QMessageBox.critical(self, "错误", "恢复备份失败，请检查日志获取更多信息。")

    def edit_backup(self):
        """编辑备份信息"""
        current_row = self.backup_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "请先选择一个备份！")
            return

        backup_id = self.backup_table.item(current_row, 0).data(Qt.UserRole)
        current_desc = self.backup_table.item(current_row, 2).text()

        # 显示编辑对话�?
        dialog = EditBackupDialog(self, backup_id, current_desc)
        if dialog.exec() != QDialog.Accepted:
            return

        # 更新备份信息
        description = dialog.description_edit.toPlainText()
        tags = [
            tag.strip() for tag in dialog.tags_edit.text().split(",") if tag.strip()
        ]
        game_date = (
            dialog.game_date_edit.text() if dialog.game_date_edit.text() else None
        )

        if self.backup_manager.update_backup_metadata(
            backup_id, description, tags, game_date
        ):
            # 更新表格显示
            self.backup_table.item(current_row, 1).setText(game_date or "-")
            self.backup_table.item(current_row, 2).setText(description)
            QMessageBox.information(self, "成功", "成功更新备份信息！")
        else:
            QMessageBox.critical(
                self, "错误", "更新备份信息失败，请检查日志获取更多信息。"
            )

    def delete_backup(self):
        """删除备份"""
        current_row = self.backup_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "请先选择一个备份！")
            return

        backup_id = self.backup_table.item(current_row, 0).data(Qt.UserRole)
        # 显示确认对话�?
        reply = QMessageBox.question(
            self,
            "确认删除",
            "确定要删除这个备份吗？此操作不可恢复！",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.No:
            return

        # 删除备份
        if self.backup_manager.delete_backup(backup_id):
            # 从表格中移除
            self.backup_table.removeRow(current_row)
            QMessageBox.information(self, "成功", "成功删除备份！")
        else:
            QMessageBox.critical(self, "错误", "删除备份失败，请检查日志获取更多信息。")

    def show_settings(self):
        """显示设置对话话框"""
        dialog = SettingsDialog(self)
        if dialog.exec() == QDialog.Accepted:
            # 重新加载配置
            self.config = get_config()

            # 应用新主�?
            self.apply_theme()

            # 重新加载存档
            self.load_save_files()

    def apply_theme(self):
        """应用主题样式"""
        theme = self.config.get("theme", "dark")

        if theme == "dark":
            self.setStyleSheet(get_dark_style())
        else:
            self.setStyleSheet(get_light_style())

    def show_save_context_menu(self, position):
        """显示存档右键菜单"""
        current_item = self.save_list.currentItem()
        if not current_item:
            return

        context_menu = QMenu(self)

        backup_action = context_menu.addAction("创建备份")
        backup_action.triggered.connect(self.create_backup)

        context_menu.exec(self.save_list.mapToGlobal(position))

    def show_backup_context_menu(self, position):
        """显示备份右键菜单"""
        current_row = self.backup_table.currentRow()
        if current_row < 0:
            return

        context_menu = QMenu(self)

        restore_action = context_menu.addAction("恢复此备份")
        restore_action.triggered.connect(self.restore_backup)

        edit_action = context_menu.addAction("编辑信息")
        edit_action.triggered.connect(self.edit_backup)

        context_menu.addSeparator()

        delete_action = context_menu.addAction("删除")
        delete_action.triggered.connect(self.delete_backup)

        context_menu.exec(self.backup_table.mapToGlobal(position))

    def auto_refresh(self):
        """自动刷新存档列表"""
        # 保存当前选择的存档名
        current_save_name = None
        current_item = self.save_list.currentItem()
        if current_item:
            current_save = current_item.data(Qt.UserRole)
            current_save_name = current_save["name"]

        # 重新加载存档
        self.load_save_files()

        # 恢复之前的选择
        if current_save_name:
            for i in range(self.save_list.count()):
                item = self.save_list.item(i)
                save_data = item.data(Qt.UserRole)
                if save_data["name"] == current_save_name:
                    self.save_list.setCurrentItem(item)
                    break


class BackupDialog(QDialog):
    """备份对话框"""

    def __init__(self, parent=None, save_name=""):
        super().__init__(parent)

        self.setWindowTitle(f"创建备份 - {save_name}")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)

        # 游戏时间
        game_date_group = QGroupBox("游戏进度")
        game_date_layout = QVBoxLayout(game_date_group)

        self.game_date_edit = QLineEdit()
        self.game_date_edit.setPlaceholderText("输入游戏内日期，例如 1456.8.15")
        game_date_layout.addWidget(self.game_date_edit)

        layout.addWidget(game_date_group)

        # 描述
        description_group = QGroupBox("备份描述")
        description_layout = QVBoxLayout(description_group)

        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("输入备份的描述信息...")
        description_layout.addWidget(self.description_edit)

        layout.addWidget(description_group)

        # 标签
        tags_group = QGroupBox("标签")
        tags_layout = QVBoxLayout(tags_group)

        self.tags_edit = QLineEdit()
        self.tags_edit.setPlaceholderText("输入标签，用逗号分隔...")
        tags_layout.addWidget(self.tags_edit)

        layout.addWidget(tags_group)

        # 按钮
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)


class EditBackupDialog(QDialog):
    """编辑备份对话框"""

    def __init__(self, parent=None, backup_id="", current_desc=""):
        super().__init__(parent)

        self.setWindowTitle(f"编辑备份信息")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)

        # 显示备份ID
        id_label = QLabel(f"备份ID: {backup_id}")
        layout.addWidget(id_label)

        # 游戏日期
        date_group = QGroupBox("游戏进度")
        date_layout = QVBoxLayout(date_group)

        self.game_date_edit = QLineEdit()
        self.game_date_edit.setPlaceholderText("输入游戏内日期，例如 1456.8.15")
        date_layout.addWidget(self.game_date_edit)

        layout.addWidget(date_group)

        # 描述
        description_group = QGroupBox("备份描述")
        description_layout = QVBoxLayout(description_group)

        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("输入备份的描述信息...")
        self.description_edit.setText(current_desc)
        description_layout.addWidget(self.description_edit)

        layout.addWidget(description_group)

        # 标签
        tags_group = QGroupBox("标签")
        tags_layout = QVBoxLayout(tags_group)

        self.tags_edit = QLineEdit()
        self.tags_edit.setPlaceholderText("输入标签，用逗号分隔...")
        tags_layout.addWidget(self.tags_edit)

        layout.addWidget(tags_group)

        # 按钮
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)


class SettingsDialog(QDialog):
    """设置对话框"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.config = get_config()

        self.setWindowTitle("设置")
        self.setMinimumWidth(500)

        layout = QVBoxLayout(self)

        # 创建选项
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # 常规设置选项
        self.general_tab = QWidget()
        self.tab_widget.addTab(self.general_tab, "常规")
        self.setup_general_tab()

        # 外观选项
        self.appearance_tab = QWidget()
        self.tab_widget.addTab(self.appearance_tab, "外观")
        self.setup_appearance_tab()

        # 按钮
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.save_settings)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def setup_general_tab(self):
        """设置常规选项"""
        layout = QFormLayout(self.general_tab)

        # 存档目录
        self.save_dir_edit = QLineEdit(self.config["eu4_save_dir"])
        self.save_dir_edit.setReadOnly(True)
        save_dir_layout = QHBoxLayout()
        save_dir_layout.addWidget(self.save_dir_edit)
        save_dir_btn = QPushButton("浏览...")
        save_dir_btn.clicked.connect(self.choose_save_dir)
        save_dir_layout.addWidget(save_dir_btn)
        layout.addRow("存档目录:", save_dir_layout)

        # 备份目录
        self.backup_dir_edit = QLineEdit(self.config["backup_dir"])
        self.backup_dir_edit.setReadOnly(True)
        backup_dir_layout = QHBoxLayout()
        backup_dir_layout.addWidget(self.backup_dir_edit)
        backup_dir_btn = QPushButton("浏览...")
        backup_dir_btn.clicked.connect(self.choose_backup_dir)
        backup_dir_layout.addWidget(backup_dir_btn)
        layout.addRow("备份目录:", backup_dir_layout)

        # 自动备份间隔
        self.backup_interval = QSpinBox()
        self.backup_interval.setRange(5, 120)
        self.backup_interval.setValue(self.config["auto_backup_interval"])
        self.backup_interval.setSuffix(" 分钟")
        layout.addRow("自动备份间隔:", self.backup_interval)

        # 每存档最大备份数
        self.max_backups = QSpinBox()
        self.max_backups.setRange(1, 100)
        self.max_backups.setValue(self.config["max_backups_per_save"])
        layout.addRow("每存档最大备份数:", self.max_backups)

    def setup_appearance_tab(self):
        """设置外观选项"""
        layout = QVBoxLayout(self.appearance_tab)

        # 主题选择
        theme_group = QGroupBox("主题")
        theme_layout = QVBoxLayout(theme_group)

        self.dark_theme_rb = QCheckBox("暗色主题")
        self.light_theme_rb = QCheckBox("亮色主题")

        self.dark_theme_rb.setChecked(self.config["theme"] == "dark")
        self.light_theme_rb.setChecked(self.config["theme"] == "light")

        # 互斥选择
        self.dark_theme_rb.clicked.connect(
            lambda: self.light_theme_rb.setChecked(not self.dark_theme_rb.isChecked())
        )
        self.light_theme_rb.clicked.connect(
            lambda: self.dark_theme_rb.setChecked(not self.light_theme_rb.isChecked())
        )

        theme_layout.addWidget(self.dark_theme_rb)
        theme_layout.addWidget(self.light_theme_rb)

        layout.addWidget(theme_group)
        layout.addStretch()

    def choose_save_dir(self):
        """选择存档目录"""
        directory = QFileDialog.getExistingDirectory(
            self, "选择存档目录", self.save_dir_edit.text()
        )
        if directory:
            self.save_dir_edit.setText(directory)

    def choose_backup_dir(self):
        """选择备份目录"""
        directory = QFileDialog.getExistingDirectory(
            self, "选择备份目录", self.backup_dir_edit.text()
        )
        if directory:
            self.backup_dir_edit.setText(directory)

    def save_settings(self):
        """保存设置"""
        self.config["eu4_save_dir"] = self.save_dir_edit.text()
        self.config["backup_dir"] = self.backup_dir_edit.text()
        self.config["auto_backup_interval"] = self.backup_interval.value()
        self.config["max_backups_per_save"] = self.max_backups.value()

        if self.dark_theme_rb.isChecked():
            self.config["theme"] = "dark"
        else:
            self.config["theme"] = "light"

        if save_config(self.config):
            self.accept()
        else:
            QMessageBox.critical(self, "错误", "保存设置失败，请检查日志获取更多信息。")
