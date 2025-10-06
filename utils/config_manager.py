#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模块
提供JSON配置文件的版本控制和自动迁移功能
"""

import json
import os
from typing import Dict, Any, Optional


class ConfigManager:
    """配置管理器 - 支持版本控制和自动迁移"""
    
    def __init__(self, config_file: str, current_version: str, default_config: Dict[str, Any]):
        """
        初始化配置管理器
        
        Args:
            config_file: 配置文件路径
            current_version: 当前软件版本
            default_config: 默认配置字典
        """
        self.config_file = config_file
        self.current_version = current_version
        self.default_config = default_config.copy()
        # 确保默认配置包含版本字段
        self.default_config["version"] = current_version
        
        # 确保配置目录存在
        config_dir = os.path.dirname(config_file)
        if config_dir and not os.path.exists(config_dir):
            os.makedirs(config_dir)
    
    def load_config(self) -> Dict[str, Any]:
        """
        加载配置文件，必要时执行迁移
        
        Returns:
            配置字典
        """
        # 如果配置文件不存在，创建默认配置文件
        if not os.path.exists(self.config_file):
            self._create_default_config()
            return self.default_config.copy()
        
        # 读取现有配置
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"配置文件读取错误: {e}，使用默认配置")
            self._create_default_config()
            return self.default_config.copy()
        
        # 检查版本并执行迁移
        config_version = config.get("version", "0.0.0")
        if self._compare_versions(config_version, self.current_version) < 0:
            config = self._migrate_config(config, config_version)
            self.save_config(config)
        
        return config
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """
        保存配置到文件
        
        Args:
            config: 配置字典
            
        Returns:
            是否保存成功
        """
        try:
            # 确保配置包含版本信息
            if "version" not in config:
                config["version"] = self.current_version
                
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            return True
        except IOError as e:
            print(f"配置文件保存失败: {e}")
            return False
    
    def _create_default_config(self):
        """创建默认配置文件"""
        try:
            self.save_config(self.default_config.copy())
            print(f"已创建默认配置文件: {self.config_file}")
        except Exception as e:
            print(f"创建默认配置文件失败: {e}")
    
    def _migrate_config(self, old_config: Dict[str, Any], old_version: str) -> Dict[str, Any]:
        """
        迁移配置文件到新版本
        
        Args:
            old_config: 旧配置
            old_version: 旧版本号
            
        Returns:
            迁移后的新配置
        """
        print(f"正在迁移配置文件从版本 {old_version} 到 {self.current_version}")
        
        # 创建新配置，基于默认配置
        new_config = self.default_config.copy()
        
        # 保留旧配置中的字段值（除了版本号）
        for key, value in old_config.items():
            if key != "version":
                # 对于字典类型的字段，需要递归合并
                if key in new_config and isinstance(new_config[key], dict) and isinstance(value, dict):
                    # 合并字典，保留旧值
                    new_config[key].update(value)
                else:
                    # 直接使用旧值
                    new_config[key] = value
        
        # 更新版本号
        new_config["version"] = self.current_version
        
        # 根据版本差异执行特定迁移逻辑
        # 这里可以根据需要添加版本间的特定迁移处理
        # 示例：
        # if self._compare_versions(old_version, "1.1.0") < 0:
        #     # 从1.1.0之前版本迁移的特定逻辑
        #     pass
        
        print("配置文件迁移完成")
        return new_config
    
    def _compare_versions(self, version1: str, version2: str) -> int:
        """
        比较两个版本号
        
        Args:
            version1: 版本号1
            version2: 版本号2
            
        Returns:
            -1: version1 < version2
             0: version1 == version2
             1: version1 > version2
        """
        v1_parts = [int(x) for x in version1.split(".")]
        v2_parts = [int(x) for x in version2.split(".")]
        
        # 补齐版本号长度
        while len(v1_parts) < len(v2_parts):
            v1_parts.append(0)
        while len(v2_parts) < len(v1_parts):
            v2_parts.append(0)
        
        # 逐位比较
        for i in range(len(v1_parts)):
            if v1_parts[i] < v2_parts[i]:
                return -1
            elif v1_parts[i] > v2_parts[i]:
                return 1
        
        return 0


def get_user_config_dir(app_name: str = "UnrealManagerTools") -> str:
    """
    获取用户配置目录路径
    
    Args:
        app_name: 应用程序名称
        
    Returns:
        用户配置目录路径
    """
    if os.name == 'nt':  # Windows
        # Windows: 使用 AppData\Roaming
        config_dir = os.path.join(os.environ.get('APPDATA', ''), app_name)
    elif os.name == 'posix':  # macOS/Linux
        # macOS: ~/Library/Application Support/
        # Linux: ~/.config/
        if 'XDG_CONFIG_HOME' in os.environ:
            config_dir = os.path.join(os.environ['XDG_CONFIG_HOME'], app_name)
        else:
            config_dir = os.path.join(os.path.expanduser('~'), '.config', app_name)
    else:
        # 其他系统使用用户主目录
        config_dir = os.path.join(os.path.expanduser('~'), '.' + app_name)
    
    # 确保目录存在
    os.makedirs(config_dir, exist_ok=True)
    return config_dir


# 示例使用
if __name__ == "__main__":
    # 定义默认配置
    DEFAULT_UE_ASSETS_CONFIG = {
        "resources": [],
        "categories": ["默认"],
        "category_paths": {},
        "settings": {
            "auto_refresh": True,
            "show_preview": True,
            "max_recent_files": 10
        },
        "version": "1.2.0"
    }
    
    # 获取用户配置目录
    user_config_dir = get_user_config_dir()
    
    # 创建配置管理器实例
    assets_config_manager = ConfigManager(
        config_file=os.path.join(user_config_dir, "ue_assets.json"),
        current_version="1.2.0",
        default_config=DEFAULT_UE_ASSETS_CONFIG
    )
    
    # 加载配置（自动处理迁移）
    config = assets_config_manager.load_config()
    print("当前配置:", json.dumps(config, ensure_ascii=False, indent=2))
    
    # 修改配置并保存
    config["settings"]["auto_refresh"] = False
    assets_config_manager.save_config(config)
    print("配置已保存")