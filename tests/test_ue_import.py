#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试导入到虚幻引擎工程功能
"""

import os
import sys
import zipfile
import tempfile
import shutil

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_test_ue_project():
    """创建一个测试用的虚幻引擎工程结构"""
    # 创建临时目录作为测试工程
    project_dir = tempfile.mkdtemp(prefix="TestUEProject_")
    
    # 创建.uproject文件
    uproject_path = os.path.join(project_dir, "TestProject.uproject")
    uproject_content = '''{
    "FileVersion": 3,
    "EngineAssociation": "5.1",
    "Category": "",
    "Description": "",
    "Modules": [
        {
            "Name": "TestProject",
            "Type": "Runtime",
            "LoadingPhase": "Default"
        }
    ],
    "Plugins": []
}'''
    
    with open(uproject_path, 'w', encoding='utf-8') as f:
        f.write(uproject_content)
    
    # 创建Content目录
    content_dir = os.path.join(project_dir, "Content")
    os.makedirs(content_dir, exist_ok=True)
    
    print(f"创建测试UE工程: {project_dir}")
    print(f"工程文件: {uproject_path}")
    print(f"Content目录: {content_dir}")
    
    return project_dir, uproject_path, content_dir

def create_test_asset_zip():
    """创建一个测试用的资产ZIP文件"""
    with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_zip:
        with zipfile.ZipFile(temp_zip.name, 'w') as zf:
            # 创建双重嵌套的UE资产结构
            base_name = "TestAsset"
            
            # 模拟典型的UE资产包结构
            zf.writestr(f"{base_name}/{base_name}/Materials/M_Floor.uasset", "材质文件内容")
            zf.writestr(f"{base_name}/{base_name}/Materials/M_Wall.uasset", "墙面材质文件内容")
            zf.writestr(f"{base_name}/{base_name}/Textures/T_Floor_Diffuse.uasset", "地板贴图文件内容")
            zf.writestr(f"{base_name}/{base_name}/Textures/T_Wall_Normal.uasset", "法线贴图文件内容")
            zf.writestr(f"{base_name}/{base_name}/Meshes/SM_Cube.uasset", "静态网格文件内容")
            zf.writestr(f"{base_name}/{base_name}/Maps/TestLevel.umap", "测试关卡文件内容")
            zf.writestr(f"{base_name}/{base_name}/Blueprints/BP_TestActor.uasset", "蓝图文件内容")
            zf.writestr(f"{base_name}/{base_name}/README.md", "这是一个测试资产包")
            
        return temp_zip.name

def test_directory_optimization_for_ue():
    """测试UE工程导入的目录结构优化"""
    print("开始测试UE工程导入功能...")
    
    try:
        # 创建测试UE工程
        project_dir, uproject_path, content_dir = create_test_ue_project()
        
        # 创建测试资产ZIP
        test_zip = create_test_asset_zip()
        print(f"创建测试ZIP文件: {test_zip}")
        
        # 导入测试
        from widgets.asset_card import AssetCard
        from utils.image_utils import ImageUtils
        
        # 创建模拟控制器
        class MockController:
            pass
        
        # 创建AssetCard实例来测试导入功能
        image_utils = ImageUtils()
        asset_card = AssetCard(None, {}, MockController(), image_utils)
        
        # 模拟导入过程
        print("\n=== 开始导入测试 ===")
        
        # 创建临时解压目录进行测试
        temp_extract_path = tempfile.mkdtemp(prefix="test_extract_")
        
        # 解压到临时目录
        import zipfile
        with zipfile.ZipFile(test_zip, 'r') as zf:
            zf.extractall(temp_extract_path)
        
        print("原始解压结构:")
        for root, dirs, files in os.walk(temp_extract_path):
            level = root.replace(temp_extract_path, '').count(os.sep)
            indent = '  ' * level
            print(f"{indent}{os.path.basename(root)}/")
            sub_indent = '  ' * (level + 1)
            for file in files:
                print(f"{sub_indent}{file}")
        
        # 测试优化并导入到Content目录
        final_import_path = os.path.join(content_dir, "TestAsset")
        asset_card._optimize_and_import_to_content(temp_extract_path, final_import_path)
        
        print(f"\n导入后的Content目录结构:")
        for root, dirs, files in os.walk(content_dir):
            level = root.replace(content_dir, '').count(os.sep)
            indent = '  ' * level
            print(f"{indent}{os.path.basename(root)}/")
            sub_indent = '  ' * (level + 1)
            for file in files:
                print(f"{sub_indent}{file}")
        
        # 验证导入结果
        expected_dirs = ["Materials", "Textures", "Meshes", "Maps", "Blueprints"]
        success = True
        
        for expected_dir in expected_dirs:
            expected_path = os.path.join(final_import_path, expected_dir)
            if os.path.exists(expected_path):
                print(f"✅ 找到预期目录: {expected_dir}")
            else:
                print(f"❌ 未找到预期目录: {expected_dir}")
                success = False
        
        # 检查是否消除了双重嵌套
        nested_path = os.path.join(final_import_path, "TestAsset")
        if not os.path.exists(nested_path):
            print("✅ 成功消除双重嵌套")
        else:
            print("❌ 仍存在双重嵌套")
            success = False
        
        if success:
            print("\n🎉 UE工程导入功能测试成功！")
            print(f"资产已成功导入到: {final_import_path}")
        else:
            print("\n❌ UE工程导入功能测试失败")
        
        # 清理测试文件
        os.unlink(test_zip)
        shutil.rmtree(project_dir)
        print(f"已清理测试文件")
        
    except Exception as e:
        print(f"❌ 测试出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_directory_optimization_for_ue()