#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试配置管理功能
"""

import sys
import os
import json
import tempfile
import shutil

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config_manager import ConfigManager
from models.asset_manager import AssetManager
from models.project_manager import ProjectManager


def test_config_manager_basic():
    """测试配置管理器基本功能"""
    print("=== 测试配置管理器基本功能 ===")
    
    # 创建临时目录用于测试
    test_dir = tempfile.mkdtemp(prefix="config_test_")
    
    try:
        # 测试配置文件路径
        test_config_file = os.path.join(test_dir, "test_config.json")
        
        # 定义默认配置
        default_config = {
            "name": "TestApp",
            "version": "1.0.0",
            "settings": {
                "theme": "dark",
                "language": "zh"
            }
        }
        
        # 创建配置管理器
        config_manager = ConfigManager(
            config_file=test_config_file,
            current_version="1.0.0",
            default_config=default_config
        )
        
        # 测试创建默认配置
        config = config_manager.load_config()
        assert config["name"] == "TestApp"
        assert config["version"] == "1.0.0"
        assert config["settings"]["theme"] == "dark"
        print("✅ 默认配置创建测试通过")
        
        # 测试保存和加载配置
        config["settings"]["theme"] = "light"
        config["new_field"] = "test_value"
        assert config_manager.save_config(config)
        
        # 重新加载配置
        loaded_config = config_manager.load_config()
        assert loaded_config["settings"]["theme"] == "light"
        assert loaded_config["new_field"] == "test_value"
        print("✅ 配置保存和加载测试通过")
        
        # 测试版本迁移
        # 创建旧版本配置文件
        old_config = {
            "name": "OldApp",
            "settings": {
                "theme": "blue"
            },
            "version": "0.9.0"
        }
        
        with open(test_config_file, 'w', encoding='utf-8') as f:
            json.dump(old_config, f, ensure_ascii=False, indent=2)
        
        # 重新加载配置（应该触发迁移）
        migrated_config = config_manager.load_config()
        assert migrated_config["name"] == "OldApp"  # 保留旧值
        assert migrated_config["settings"]["theme"] == "blue"  # 保留旧值
        assert migrated_config["settings"]["language"] == "zh"  # 新字段使用默认值
        assert migrated_config["version"] == "1.0.0"  # 版本已更新
        print("✅ 配置版本迁移测试通过")
        
    finally:
        # 清理测试目录
        shutil.rmtree(test_dir)
    
    print("✅ 配置管理器基本功能测试完成\n")


def test_asset_manager_config():
    """测试资产管理器配置功能"""
    print("=== 测试资产管理器配置功能 ===")
    
    # 创建临时目录用于测试
    test_dir = tempfile.mkdtemp(prefix="asset_config_test_")
    
    try:
        # 保存当前工作目录并切换到测试目录
        original_cwd = os.getcwd()
        os.chdir(test_dir)
        
        # 创建config目录
        config_dir = "config"
        os.makedirs(config_dir, exist_ok=True)
        
        # 创建资产管理器
        asset_manager = AssetManager()
        
        # 检查配置是否正确加载
        assert "默认" in asset_manager.categories
        assert "全部" in asset_manager.categories
        print("✅ 资产管理器初始化测试通过")
        
        # 添加资源测试
        test_resource = {
            "name": "TestResource",
            "path": "/test/path",
            "category": "测试",
            "cover": "",
            "doc": "",
            "date_added": "2023-01-01 12:00:00"
        }
        
        asset_manager.resources.append(test_resource)
        assert asset_manager.save_data()
        
        # 重新加载验证
        asset_manager.load_data()
        assert len(asset_manager.resources) == 1
        assert asset_manager.resources[0]["name"] == "TestResource"
        print("✅ 资源保存和加载测试通过")
        
        # 添加分类测试
        assert asset_manager.add_category("新分类")
        assert "新分类" in asset_manager.categories
        print("✅ 分类管理测试通过")
        
    finally:
        # 恢复工作目录并清理测试目录
        os.chdir(original_cwd)
        shutil.rmtree(test_dir)
    
    print("✅ 资产管理器配置功能测试完成\n")


def test_project_manager_config():
    """测试项目管理器配置功能"""
    print("=== 测试项目管理器配置功能 ===")
    
    # 创建临时目录用于测试
    test_dir = tempfile.mkdtemp(prefix="project_config_test_")
    
    try:
        # 保存当前工作目录并切换到测试目录
        original_cwd = os.getcwd()
        os.chdir(test_dir)
        
        # 创建config目录
        config_dir = "config"
        os.makedirs(config_dir, exist_ok=True)
        
        # 创建项目管理器
        project_manager = ProjectManager()
        
        # 检查配置是否正确加载
        assert isinstance(project_manager.recent_projects, list)
        print("✅ 项目管理器初始化测试通过")
        
        # 添加项目测试
        test_project = {
            "name": "TestProject",
            "path": "/test/project.uproject",
            "dir": "/test",
            "size": 1024,
            "modified": "2023-01-01T12:00:00",
            "created": "2023-01-01T12:00:00"
        }
        
        project_manager.recent_projects.append(test_project)
        assert project_manager.save_config()
        
        # 重新加载验证
        project_manager.load_config()
        assert len(project_manager.recent_projects) == 1
        assert project_manager.recent_projects[0]["name"] == "TestProject"
        print("✅ 项目保存和加载测试通过")
        
    finally:
        # 恢复工作目录并清理测试目录
        os.chdir(original_cwd)
        shutil.rmtree(test_dir)
    
    print("✅ 项目管理器配置功能测试完成\n")


def test_version_migration():
    """测试版本迁移功能"""
    print("=== 测试版本迁移功能 ===")
    
    # 创建临时目录用于测试
    test_dir = tempfile.mkdtemp(prefix="migration_test_")
    
    try:
        # 保存当前工作目录并切换到测试目录
        original_cwd = os.getcwd()
        os.chdir(test_dir)
        
        # 创建config目录
        config_dir = "config"
        os.makedirs(config_dir, exist_ok=True)
        
        # 创建旧版本资产配置文件
        old_assets_config = {
            "resources": [
                {
                    "name": "OldResource",
                    "path": "/old/path",
                    "category": "旧分类"
                }
            ],
            "categories": ["旧分类"],
            "version": "0.5.0"
        }
        
        with open(os.path.join(config_dir, "ue_assets.json"), 'w', encoding='utf-8') as f:
            json.dump(old_assets_config, f, ensure_ascii=False, indent=2)
        
        # 创建资产管理器（应该触发迁移）
        asset_manager = AssetManager()
        
        # 检查迁移结果
        assert len(asset_manager.resources) == 1
        assert asset_manager.resources[0]["name"] == "OldResource"
        # 注意：迁移后categories会包含"全部"，所以需要检查"默认"是否在categories中
        categories_without_all = [cat for cat in asset_manager.categories if cat != "全部"]
        assert "默认" in categories_without_all or "旧分类" in asset_manager.categories
        assert asset_manager.config["version"] == "1.0.0"  # 版本已更新
        print("✅ 资产配置版本迁移测试通过")
        
        # 创建旧版本项目配置文件
        old_projects_config = {
            "recent_projects": [
                {
                    "name": "OldProject",
                    "path": "/old/project.uproject"
                }
            ],
            "version": "0.8.0"
        }
        
        with open(os.path.join(config_dir, "ue_projects.json"), 'w', encoding='utf-8') as f:
            json.dump(old_projects_config, f, ensure_ascii=False, indent=2)
        
        # 创建项目管理器（应该触发迁移）
        project_manager = ProjectManager()
        
        # 检查迁移结果
        assert len(project_manager.recent_projects) == 1
        assert project_manager.recent_projects[0]["name"] == "OldProject"
        assert project_manager.config["version"] == "1.0.0"  # 版本已更新
        assert "settings" in project_manager.config  # 新增的设置字段
        print("✅ 项目配置版本迁移测试通过")
        
    finally:
        # 恢复工作目录并清理测试目录
        os.chdir(original_cwd)
        shutil.rmtree(test_dir)
    
    print("✅ 版本迁移功能测试完成\n")


if __name__ == "__main__":
    print("开始测试配置管理功能...")
    
    test_config_manager_basic()
    test_asset_manager_config()
    test_project_manager_config()
    test_version_migration()
    
    print("🎉 所有配置管理功能测试完成！")