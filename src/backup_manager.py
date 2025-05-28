#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
备份管理模块
"""

import os
import shutil
import json
import logging
from datetime import datetime
from pathlib import Path

from src.config import get_config, save_config


class BackupManager:
    """备份管理器类"""

    def __init__(self):
        self.config = get_config()
        self.backup_dir = self.config["backup_dir"]

        # 确保备份目录存在
        os.makedirs(self.backup_dir, exist_ok=True)

        # 加载备份记录
        self.backup_index_file = os.path.join(self.backup_dir, "backup_index.json")
        self.backup_index = self._load_backup_index()

    def _load_backup_index(self):
        """加载备份索引文件"""
        if os.path.exists(self.backup_index_file):
            try:
                with open(self.backup_index_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logging.error(f"读取备份索引文件失败: {e}")
                return {}
        else:
            return {}

    def _save_backup_index(self):
        """保存备份索引文件"""
        try:
            with open(self.backup_index_file, "w", encoding="utf-8") as f:
                json.dump(self.backup_index, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            logging.error(f"保存备份索引文件失败: {e}")
            return False

    def create_backup(self, save_file_path, description="", tags=None):
        """
        创建备份

        参数:
            save_file_path: 存档文件路径
            description: 备份描述
            tags: 标签列表

        返回:
            成功返回备份ID，失败返回None
        """
        try:
            save_file_name = os.path.basename(save_file_path)
            save_name = os.path.splitext(save_file_name)[0]  # 不含扩展名的存档名

            # 生成唯一的备份目录名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_id = f"{save_name}_{timestamp}"
            backup_dir = os.path.join(self.backup_dir, backup_id)

            # 在备份目录中创建一个子目录用于存放实际文件
            os.makedirs(backup_dir, exist_ok=True)

            # 复制存档文件
            dest_path = os.path.join(backup_dir, save_file_name)
            shutil.copy2(save_file_path, dest_path)

            # 创建备份元数据
            meta = {
                "original_file": save_file_path,
                "backup_time": datetime.now().isoformat(),
                "description": description,
                "tags": tags or [],
                "game_date": "",  # 可以从存档文件中解析游戏日期
                "size": os.path.getsize(save_file_path),
            }

            # 保存元数据
            meta_path = os.path.join(backup_dir, "meta.json")
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(meta, f, ensure_ascii=False, indent=4)

            # 更新备份索引
            if save_name not in self.backup_index:
                self.backup_index[save_name] = []

            self.backup_index[save_name].append(
                {
                    "id": backup_id,
                    "time": meta["backup_time"],
                    "description": description,
                    "tags": tags or [],
                }
            )

            # 检查是否超过最大备份数量
            max_backups = self.config["max_backups_per_save"]
            if len(self.backup_index[save_name]) > max_backups:
                # 删除最旧的备份
                oldest = sorted(self.backup_index[save_name], key=lambda x: x["time"])[
                    0
                ]
                self._remove_backup(oldest["id"])
                self.backup_index[save_name].remove(oldest)

            self._save_backup_index()
            logging.info(f"创建备份成功: {backup_id}")

            return backup_id

        except Exception as e:
            logging.error(f"创建备份失败: {e}")
            return None

    def restore_backup(self, backup_id):
        """
        从备份恢复

        参数:
            backup_id: 备份ID

        返回:
            成功返回True，失败返回False
        """
        try:
            backup_dir = os.path.join(self.backup_dir, backup_id)

            # 检查备份是否存在
            if not os.path.exists(backup_dir):
                logging.error(f"备份不存在: {backup_id}")
                return False

            # 读取元数据
            meta_path = os.path.join(backup_dir, "meta.json")
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)

            # 备份的原始存档文件名
            original_file = meta["original_file"]
            save_file_name = os.path.basename(original_file)

            # 备份的存档文件路径
            backup_file_path = os.path.join(backup_dir, save_file_name)

            # 目标存档位置
            target_dir = os.path.dirname(original_file)
            target_path = os.path.join(target_dir, save_file_name)

            # 如果目标存档存在，先创建一个临时备份
            if os.path.exists(target_path):
                current_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                temp_backup_path = os.path.join(
                    target_dir, f"{save_file_name}.{current_timestamp}.bak"
                )
                shutil.copy2(target_path, temp_backup_path)
                logging.info(f"创建了当前存档的临时备份: {temp_backup_path}")

            # 复制备份文件到目标位置
            shutil.copy2(backup_file_path, target_path)
            logging.info(f"恢复备份成功: {backup_id} -> {target_path}")

            return True

        except Exception as e:
            logging.error(f"恢复备份失败: {e}")
            return False

    def delete_backup(self, backup_id):
        """
        删除备份

        参数:
            backup_id: 备份ID

        返回:
            成功返回True，失败返回False
        """
        try:
            # 找到备份所属的存档
            save_name = None
            for name, backups in self.backup_index.items():
                for backup in backups:
                    if backup["id"] == backup_id:
                        save_name = name
                        break
                if save_name:
                    break

            if not save_name:
                logging.error(f"找不到备份ID对应的存档: {backup_id}")
                return False

            # 删除物理备份文件
            success = self._remove_backup(backup_id)
            if not success:
                return False

            # 更新索引
            self.backup_index[save_name] = [
                b for b in self.backup_index[save_name] if b["id"] != backup_id
            ]
            if not self.backup_index[save_name]:
                del self.backup_index[save_name]

            self._save_backup_index()
            logging.info(f"删除备份成功: {backup_id}")

            return True

        except Exception as e:
            logging.error(f"删除备份失败: {e}")
            return False

    def _remove_backup(self, backup_id):
        """删除备份文件"""
        try:
            backup_dir = os.path.join(self.backup_dir, backup_id)
            if os.path.exists(backup_dir):
                shutil.rmtree(backup_dir)
                return True
            else:
                logging.warning(f"备份目录不存在: {backup_dir}")
                return False
        except Exception as e:
            logging.error(f"删除备份文件失败: {e}")
            return False

    def get_backups_for_save(self, save_name):
        """
        获取指定存档的所有备份

        参数:
            save_name: 存档名称(不含扩展名)

        返回:
            备份列表，按时间从新到旧排序
        """
        if save_name in self.backup_index:
            # 按时间排序
            backups = sorted(
                self.backup_index[save_name], key=lambda x: x["time"], reverse=True
            )

            # 为每个备份添加额外信息
            result = []
            for backup in backups:
                backup_dir = os.path.join(self.backup_dir, backup["id"])
                meta_path = os.path.join(backup_dir, "meta.json")

                if os.path.exists(meta_path):
                    try:
                        with open(meta_path, "r", encoding="utf-8") as f:
                            meta = json.load(f)

                        backup_info = backup.copy()
                        backup_info["game_date"] = meta.get("game_date", "")
                        backup_info["size"] = meta.get("size", 0)
                        backup_info["description"] = meta.get(
                            "description", backup_info.get("description", "")
                        )

                        result.append(backup_info)
                    except:
                        result.append(backup)
                else:
                    result.append(backup)

            return result
        else:
            return []

    def get_all_backups(self):
        """
        获取所有备份

        返回:
            所有备份的扁平列表，按时间从新到旧排序
        """
        all_backups = []
        for save_name, backups in self.backup_index.items():
            for backup in backups:
                backup_copy = backup.copy()
                backup_copy["save_name"] = save_name
                all_backups.append(backup_copy)

        # 按时间排序
        all_backups.sort(key=lambda x: x["time"], reverse=True)
        return all_backups

    def update_backup_metadata(
        self, backup_id, description=None, tags=None, game_date=None
    ):
        """
        更新备份元数据

        参数:
            backup_id: 备份ID
            description: 新的描述（如果要更新）
            tags: 新的标签列表（如果要更新）
            game_date: 新的游戏日期（如果要更新）

        返回:
            成功返回True，失败返回False
        """
        try:
            # 查找备份所属的存档
            save_name = None
            backup_index = None
            for name, backups in self.backup_index.items():
                for i, backup in enumerate(backups):
                    if backup["id"] == backup_id:
                        save_name = name
                        backup_index = i
                        break
                if save_name:
                    break

            if not save_name:
                logging.error(f"找不到备份ID对应的存档: {backup_id}")
                return False

            # 更新索引中的元数据
            if description is not None:
                self.backup_index[save_name][backup_index]["description"] = description

            if tags is not None:
                self.backup_index[save_name][backup_index]["tags"] = tags

            # 读取并更新文件中的元数据
            meta_path = os.path.join(self.backup_dir, backup_id, "meta.json")
            if os.path.exists(meta_path):
                with open(meta_path, "r", encoding="utf-8") as f:
                    meta = json.load(f)

                if description is not None:
                    meta["description"] = description

                if tags is not None:
                    meta["tags"] = tags

                if game_date is not None:
                    meta["game_date"] = game_date

                with open(meta_path, "w", encoding="utf-8") as f:
                    json.dump(meta, f, ensure_ascii=False, indent=4)

            self._save_backup_index()
            logging.info(f"更新备份元数据成功: {backup_id}")

            return True

        except Exception as e:
            logging.error(f"更新备份元数据失败: {e}")
            return False
