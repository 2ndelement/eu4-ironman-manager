#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
配置和工具模块
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime

# 应用目录
APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESOURCES_DIR = os.path.join(APP_DIR, "resources")

# EU4 存档路径 - 使用用户文档目录，确保跨用户通用
EU4_SAVE_DIR = os.path.join(
    os.path.expanduser("~"),
    "Documents",
    "Paradox Interactive",
    "Europa Universalis IV",
    "save games",
)
BACKUP_DIR = os.path.join(APP_DIR, "backups")

# 配置文件路径
CONFIG_FILE = os.path.join(APP_DIR, "config.json")

# 默认配置
DEFAULT_CONFIG = {
    "eu4_save_dir": EU4_SAVE_DIR,
    "backup_dir": BACKUP_DIR,
    "auto_backup_interval": 30,  # 自动备份间隔（分钟）
    "max_backups_per_save": 10,  # 每个存档最多保留的备份数
    "theme": "dark",
    "first_run": True,
}


def setup_logging():
    """设置日志系统"""
    os.makedirs("logs", exist_ok=True)

    log_file = os.path.join("logs", f'app_{datetime.now().strftime("%Y%m%d")}.log')

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def create_config_if_not_exists():
    """如果配置文件不存在，则创建默认配置"""
    if not os.path.exists(CONFIG_FILE):
        os.makedirs(BACKUP_DIR, exist_ok=True)
        os.makedirs(os.path.join(APP_DIR, "logs"), exist_ok=True)

        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, ensure_ascii=False, indent=4)

        logging.info(f"创建了默认配置文件: {CONFIG_FILE}")
    else:
        logging.info(f"配置文件已存在: {CONFIG_FILE}")


def get_config():
    """获取配置"""
    if not os.path.exists(CONFIG_FILE):
        create_config_if_not_exists()

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
            # 确保所有默认配置项都存在
            for key, value in DEFAULT_CONFIG.items():
                if key not in config:
                    config[key] = value
            return config
    except Exception as e:
        logging.error(f"读取配置文件失败: {e}")
        return DEFAULT_CONFIG


def save_config(config):
    """保存配置"""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        logging.error(f"保存配置文件失败: {e}")
        return False


def get_save_files():
    """获取EU4存档文件"""
    config = get_config()
    save_dir = config["eu4_save_dir"]

    if not os.path.exists(save_dir):
        logging.error(f"存档目录不存在: {save_dir}")
        return []

    # 获取所有.eu4文件
    save_files = []
    for file in os.listdir(save_dir):
        if file.endswith(".eu4"):
            file_path = os.path.join(save_dir, file)
            save_files.append(
                {
                    "name": file,
                    "path": file_path,
                    "size": os.path.getsize(file_path),
                    "modified": datetime.fromtimestamp(os.path.getmtime(file_path)),
                }
            )

    # 按最后修改时间排序（最新的在前）
    save_files.sort(key=lambda x: x["modified"], reverse=True)

    return save_files


def format_file_size(size_bytes):
    """格式化文件大小"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes/1024:.2f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes/(1024*1024):.2f} MB"
    else:
        return f"{size_bytes/(1024*1024*1024):.2f} GB"
