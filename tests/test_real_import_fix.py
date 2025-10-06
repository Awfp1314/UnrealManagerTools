#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试实际导入过程中的进度条更新修复
"""

import os
import sys
import tempfile
import zipfile
import shutil

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def create_test_project():
    """创建一个测试用的UE项目结构"""
    # 创建临时目录作为测试项目
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
    
    print(f"创建测试UE项目: {project_dir}")
    print(f"项目文件: {uproject_path}")
    print(f"Content目录: {content_dir}")
    
    return project_dir, uproject_path, content_dir

def create_test_asset_zip():
    """创建一个测试用的资产ZIP文件"""
    with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_zip:
        with zipfile.ZipFile(temp_zip.name, 'w') as zf:
            # 创建包含多层嵌套的资产包
            base_name = "TestAsset"
            
            # 添加更多文件来测试进度
            for i in range(20):  # 20个文件用于测试进度条
                zf.writestr(f"{base_name}/{base_name}/Materials/M_Test_{i:03d}.uasset", f"材质文件内容 {i}")
            
            for i in range(15):  # 15个纹理文件
                zf.writestr(f"{base_name}/{base_name}/Textures/T_Test_{i:03d}.uasset", f"纹理文件内容 {i}")
            
            # 添加其他类型的资产
            zf.writestr(f"{base_name}/{base_name}/Meshes/SM_TestCube.uasset", "静态网格文件内容")
            zf.writestr(f"{base_name}/{base_name}/Maps/TestLevel.umap", "测试关卡文件内容")
            zf.writestr(f"{base_name}/{base_name}/Blueprints/BP_TestActor.uasset", "蓝图文件内容")
            zf.writestr(f"{base_name}/{base_name}/README.md", "测试资产包说明文档")
            
        return temp_zip.name

def test_real_import_process():
    """测试实际导入过程"""
    print("=== 测试实际导入过程中的进度条更新 ===")
    
    try:
        # 创建测试项目和资产
        project_dir, uproject_path, content_dir = create_test_project()
        test_zip = create_test_asset_zip()
        
        print(f"创建测试ZIP文件: {test_zip}")
        
        # 模拟导入过程
        from widgets.asset_card import AssetCard
        from utils.image_utils import ImageUtils
        
        # 创建模拟控制器
        class MockController:
            def show_status(self, message, status_type="info"):
                print(f"[状态] {message}")
        
        # 创建AssetCard实例来测试导入功能
        image_utils = ImageUtils()
        asset_card = AssetCard(None, {}, MockController(), image_utils)
        
        # 模拟导入过程
        print("\n=== 开始导入测试 ===")
        
        # 创建一个简单的进度回调函数用于测试
        def test_progress_callback(progress):
            print(f"进度更新: {int(progress * 100)}%")
        
        # 测试导入功能
        asset_card.import_cancelled = False  # 确保没有取消标志
        success = asset_card.import_single_archive_to_content(test_zip, content_dir, test_progress_callback)
        
        if success:
            print("✅ 导入测试成功")
            # 检查导入的文件
            imported_path = os.path.join(content_dir, "TestAsset")
            if os.path.exists(imported_path):
                print(f"✅ 资产已成功导入到: {imported_path}")
                # 列出导入的文件
                for root, dirs, files in os.walk(imported_path):
                    level = root.replace(imported_path, '').count(os.sep)
                    indent = ' ' * 2 * level
                    print(f"{indent}{os.path.basename(root)}/")
                    subindent = ' ' * 2 * (level + 1)
                    for file in files:
                        print(f"{subindent}{file}")
            else:
                print("❌ 资产未正确导入")
        else:
            print("❌ 导入测试失败")
        
        # 清理测试文件
        os.unlink(test_zip)
        shutil.rmtree(project_dir)
        print("已清理测试文件")
        
    except Exception as e:
        print(f"❌ 测试出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("开始测试实际导入过程中的进度条更新修复...")
    test_real_import_process()
    print("\n🎉 导入进度条更新测试完成！")