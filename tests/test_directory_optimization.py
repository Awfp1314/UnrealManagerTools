#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试目录结构优化功能
"""

import os
import sys
import zipfile
import tempfile
import shutil

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_triple_nested_test_zip():
    """创建一个包含三重嵌套目录结构的测试ZIP文件"""
    with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_zip:
        with zipfile.ZipFile(temp_zip.name, 'w') as zf:
            # 情况1：三重嵌套的情况 (TestAsset/TestAsset/TestAsset/source/...)
            base_name = "TestAsset"
            
            # 创建三重嵌套结构
            zf.writestr(f"{base_name}/{base_name}/{base_name}/source/Maps/Level1.umap", "地图文件内容")
            zf.writestr(f"{base_name}/{base_name}/{base_name}/source/Materials/Floor.uasset", "材质文件内容")
            zf.writestr(f"{base_name}/{base_name}/{base_name}/source/Textures/Wall.png", "纹理文件内容")
            zf.writestr(f"{base_name}/{base_name}/{base_name}/README.md", "这是资源说明文档")
            
        return temp_zip.name

def create_backrooms_style_zip():
    """创建一个模拟Backrooms风格的双重嵌套ZIP文件"""
    with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_zip:
        with zipfile.ZipFile(temp_zip.name, 'w') as zf:
            # 模拟 Backrooms_TheLobby/Backrooms_TheLobby/source/... 的结构
            base_name = "Backrooms_TheLobby"
            
            # 创建双重嵌套结构
            zf.writestr(f"{base_name}/{base_name}/source/Maps/Level1.umap", "地图文件内容")
            zf.writestr(f"{base_name}/{base_name}/source/Materials/Floor.uasset", "材质文件内容")
            zf.writestr(f"{base_name}/{base_name}/source/Textures/Wall.png", "纹理文件内容")
            zf.writestr(f"{base_name}/{base_name}/README.md", "这是资源说明文档")
            
        return temp_zip.name

def create_single_folder_zip():
    """创建只有一个顶级文件夹的ZIP"""
    with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_zip:
        with zipfile.ZipFile(temp_zip.name, 'w') as zf:
            # 只有一个顶级目录
            zf.writestr("AssetContent/Maps/Level1.umap", "地图文件内容")
            zf.writestr("AssetContent/Materials/Floor.uasset", "材质文件内容")
            zf.writestr("AssetContent/Textures/Wall.png", "纹理文件内容")
            
        return temp_zip.name

def print_directory_structure(base_path, title):
    """打印目录结构"""
    print(f"{title}:")
    if not os.path.exists(base_path):
        print("  目录不存在")
        return
        
    for root, dirs, files in os.walk(base_path):
        level = root.replace(base_path, '').count(os.sep)
        indent = '  ' * level
        print(f"{indent}{os.path.basename(root)}/")
        sub_indent = '  ' * (level + 1)
        for file in files:
            print(f"{sub_indent}{file}")

def test_directory_optimization():
    """测试目录结构优化"""
    print("开始测试目录结构优化功能...")
    
    # 导入优化类（模拟AssetCard的优化方法）
    from widgets.asset_card import AssetCard
    from utils.image_utils import ImageUtils
    
    # 创建一个简单的模拟控制器
    class MockController:
        pass
    
    # 创建AssetCard实例
    image_utils = ImageUtils()
    asset_card = AssetCard(None, {}, MockController(), image_utils)
    
    # 创建测试目录
    test_base_dir = tempfile.mkdtemp(prefix="test_extraction_")
    print(f"测试目录: {test_base_dir}")
    
    try:
        # 测试情况1：三重嵌套目录
        print("\n=== 测试情况1：三重嵌套目录 ===")
        nested_zip = create_triple_nested_test_zip()
        nested_test_dir = os.path.join(test_base_dir, "nested_test")
        os.makedirs(nested_test_dir, exist_ok=True)
        
        # 解压到临时目录
        temp_dir = os.path.join(nested_test_dir, "temp_TestAsset")
        with zipfile.ZipFile(nested_zip, 'r') as zf:
            zf.extractall(temp_dir)
        
        print_directory_structure(temp_dir, "原始解压结构")
        
        # 应用优化
        final_dir = os.path.join(nested_test_dir, "TestAsset")
        asset_card._optimize_directory_structure(temp_dir, final_dir)
        
        print_directory_structure(final_dir, "优化后结构")
        
        # 测试情况2：单一顶级文件夹
        print("\n=== 测试情况2：单一顶级文件夹 ===")
        single_zip = create_single_folder_zip()
        single_test_dir = os.path.join(test_base_dir, "single_test")
        os.makedirs(single_test_dir, exist_ok=True)
        
        temp_dir2 = os.path.join(single_test_dir, "temp_SingleAsset")
        with zipfile.ZipFile(single_zip, 'r') as zf:
            zf.extractall(temp_dir2)
        
        print_directory_structure(temp_dir2, "原始解压结构")
        
        final_dir2 = os.path.join(single_test_dir, "SingleAsset")
        asset_card._optimize_directory_structure(temp_dir2, final_dir2)
        
        print_directory_structure(final_dir2, "优化后结构")
        
        # 测试情况3：Backrooms风格的双重嵌套
        print("\n=== 测试情况3：Backrooms风格的双重嵌套 ===")
        backrooms_zip = create_backrooms_style_zip()
        backrooms_test_dir = os.path.join(test_base_dir, "backrooms_test")
        os.makedirs(backrooms_test_dir, exist_ok=True)
        
        temp_dir3 = os.path.join(backrooms_test_dir, "temp_Backrooms_TheLobby")
        with zipfile.ZipFile(backrooms_zip, 'r') as zf:
            zf.extractall(temp_dir3)
        
        print_directory_structure(temp_dir3, "原始解压结构")
        
        final_dir3 = os.path.join(backrooms_test_dir, "Backrooms_TheLobby")
        asset_card._optimize_directory_structure(temp_dir3, final_dir3)
        
        print_directory_structure(final_dir3, "优化后结构")
        
        print("\n✅ 目录结构优化测试完成！")
        
        # 清理测试文件
        os.unlink(nested_zip)
        os.unlink(single_zip)
        os.unlink(backrooms_zip)
        
    except Exception as e:
        print(f"❌ 测试出错: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 清理测试目录
        try:
            shutil.rmtree(test_base_dir)
            print(f"已清理测试目录: {test_base_dir}")
        except:
            print(f"清理测试目录失败: {test_base_dir}")

if __name__ == "__main__":
    test_directory_optimization()