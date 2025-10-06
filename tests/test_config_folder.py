#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试配置文件夹功能
"""

import sys
import os
import json
import tempfile
import shutil

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.asset_manager import AssetManager
from models.project_manager import ProjectManager


def test_config_folder():
    """测试配置文件夹功能"""
    print("=== 测试配置文件夹功能 ===")
    
    # 创建临时目录用于测试
    test_dir = tempfile.mkdtemp(prefix="config_folder_test_")
    
    try:
        # 保存当前工作目录并切换到测试目录
        original_cwd = os.getcwd()
        os.chdir(test_dir)
        
        # 创建config目录
        config_dir = "config"
        os.makedirs(config_dir, exist_ok=True)
        
        # 创建资产管理器
        asset_manager = AssetManager()
        
        # 检查配置文件是否在正确的位置
        assert os.path.exists(os.path.join(config_dir, "ue_assets.json"))
        print("✅ 资产配置文件位置正确")
        
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
        
        # 创建项目管理器
        project_manager = ProjectManager()
        
        # 检查配置文件是否在正确的位置
        assert os.path.exists(os.path.join(config_dir, "ue_projects.json"))
        print("✅ 项目配置文件位置正确")
        
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
    
    print("✅ 配置文件夹功能测试完成\n")


def test_config_folder_creation():
    """测试配置文件夹自动创建功能"""
    print("=== 测试配置文件夹自动创建功能 ===")
    
    # 创建临时目录用于测试
    test_dir = tempfile.mkdtemp(prefix="auto_create_test_")
    
    try:
        # 保存当前工作目录并切换到测试目录
        original_cwd = os.getcwd()
        os.chdir(test_dir)
        
        # 确保没有config目录
        if os.path.exists("config"):
            shutil.rmtree("config")
        
        # 创建资产管理器（应该自动创建config目录）
        asset_manager = AssetManager()
        
        # 检查config目录是否已创建
        assert os.path.exists("config")
        assert os.path.exists(os.path.join("config", "ue_assets.json"))
        print("✅ 配置文件夹自动创建功能正常")
        
        # 创建项目管理器（应该使用已存在的config目录）
        project_manager = ProjectManager()
        
        # 检查项目配置文件是否在正确的位置
        assert os.path.exists(os.path.join("config", "ue_projects.json"))
        print("✅ 项目配置文件位置正确")
        
    finally:
        # 恢复工作目录并清理测试目录
        os.chdir(original_cwd)
        shutil.rmtree(test_dir)
    
    print("✅ 配置文件夹自动创建功能测试完成\n")


if __name__ == "__main__":
    print("开始测试配置文件夹功能...")
    
    test_config_folder()
    test_config_folder_creation()
    
    print("🎉 所有配置文件夹功能测试完成！")