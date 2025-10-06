#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理示例
演示如何在项目中使用ConfigManager类
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config_manager import ConfigManager


def example_ue_assets_config():
    """虚幻资源配置示例"""
    # 定义默认配置（包含新字段）
    DEFAULT_UE_ASSETS_CONFIG = {
        "resources": [],
        "categories": ["默认"],
        "category_paths": {},
        "settings": {
            "auto_refresh": True,
            "show_preview": True,
            "max_recent_files": 10,
            "enable_notifications": True,  # 新增字段
            "theme": "dark"  # 新增字段
        },
        "version": "1.2.0"  # 当前版本
    }
    
    # 创建config目录（如果不存在）
    config_dir = "config"
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    
    # 创建配置管理器实例
    config_manager = ConfigManager(
        config_file=os.path.join(config_dir, "ue_assets.json"),
        current_version="1.2.0",
        default_config=DEFAULT_UE_ASSETS_CONFIG
    )
    
    # 加载配置（自动处理迁移）
    config = config_manager.load_config()
    
    print("=== 虚幻资源配置示例 ===")
    print(f"当前配置版本: {config.get('version')}")
    print(f"自动刷新: {config['settings'].get('auto_refresh')}")
    print(f"显示预览: {config['settings'].get('show_preview')}")
    print(f"最大最近文件数: {config['settings'].get('max_recent_files')}")
    print(f"启用通知: {config['settings'].get('enable_notifications', '未设置')}")
    print(f"主题: {config['settings'].get('theme', '未设置')}")
    
    # 修改配置并保存
    config["settings"]["enable_notifications"] = False
    config["settings"]["theme"] = "light"
    config_manager.save_config(config)
    
    print("\n配置已更新并保存")


def example_ue_projects_config():
    """虚幻项目配置示例"""
    # 定义默认配置（包含新字段）
    DEFAULT_UE_PROJECTS_CONFIG = {
        "recent_projects": [],
        "last_updated": "",
        "settings": {
            "auto_scan": True,
            "scan_paths": ["C:\\"],
            "exclude_paths": ["C:\\Windows", "C:\\Program Files"],
            "max_projects": 50,  # 新增字段
            "enable_cache": True  # 新增字段
        },
        "version": "1.1.0"  # 当前版本
    }
    
    # 创建config目录（如果不存在）
    config_dir = "config"
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    
    # 创建配置管理器
    config_manager = ConfigManager(
        config_file=os.path.join(config_dir, "ue_projects.json"),
        current_version="1.1.0",
        default_config=DEFAULT_UE_PROJECTS_CONFIG
    )
    
    # 加载配置（自动处理迁移）
    config = config_manager.load_config()
    
    print("\n=== 虚幻项目配置示例 ===")
    print(f"当前配置版本: {config.get('version')}")
    print(f"自动扫描: {config['settings'].get('auto_scan')}")
    print(f"扫描路径: {config['settings'].get('scan_paths')}")
    print(f"排除路径: {config['settings'].get('exclude_paths')}")
    print(f"最大项目数: {config['settings'].get('max_projects', '未设置')}")
    print(f"启用缓存: {config['settings'].get('enable_cache', '未设置')}")
    
    # 修改配置并保存
    config["settings"]["max_projects"] = 100
    config["settings"]["enable_cache"] = False
    config_manager.save_config(config)
    
    print("\n配置已更新并保存")


def simulate_version_upgrade():
    """模拟版本升级场景"""
    print("\n=== 模拟版本升级场景 ===")
    
    # 创建临时目录用于测试
    import tempfile
    import shutil
    test_dir = tempfile.mkdtemp(prefix="upgrade_test_")
    
    try:
        # 保存当前工作目录并切换到测试目录
        original_cwd = os.getcwd()
        os.chdir(test_dir)
        
        # 创建config目录
        config_dir = "config"
        os.makedirs(config_dir, exist_ok=True)
        
        # 创建旧版本配置文件
        old_config = {
            "resources": [
                {
                    "name": "TestAsset",
                    "path": "C:\\TestAssets\\TestAsset",
                    "category": "测试"
                }
            ],
            "categories": ["测试"],
            "version": "1.0.0"
        }
        
        # 写入旧版本配置
        with open(os.path.join(config_dir, "temp_upgrade_test.json"), "w", encoding="utf-8") as f:
            import json
            json.dump(old_config, f, ensure_ascii=False, indent=2)
        
        # 定义新版本默认配置
        NEW_DEFAULT_CONFIG = {
            "resources": [],
            "categories": ["默认"],
            "category_paths": {},
            "settings": {
                "auto_refresh": True,
                "show_preview": True,
                "max_recent_files": 10,
                "enable_notifications": True,  # 新增字段
                "theme": "dark"  # 新增字段
            },
            "version": "1.2.0"  # 新版本
        }
        
        # 创建配置管理器
        config_manager = ConfigManager(
            config_file=os.path.join(config_dir, "temp_upgrade_test.json"),
            current_version="1.2.0",
            default_config=NEW_DEFAULT_CONFIG
        )
        
        # 加载配置（会自动迁移）
        config = config_manager.load_config()
        
        print(f"迁移后版本: {config.get('version')}")
        print(f"保留的资源: {len(config.get('resources', []))} 个")
        print(f"新增设置-启用通知: {config['settings'].get('enable_notifications')}")
        print(f"新增设置-主题: {config['settings'].get('theme')}")
        
        # 清理测试文件
        os.remove(os.path.join(config_dir, "temp_upgrade_test.json"))
        print("\n测试完成，临时文件已清理")
        
    finally:
        # 恢复工作目录并清理测试目录
        os.chdir(original_cwd)
        shutil.rmtree(test_dir)


if __name__ == "__main__":
    example_ue_assets_config()
    example_ue_projects_config()
    simulate_version_upgrade()