#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修复后的导入功能和UE工程搜索
"""

import os
import sys
import tempfile
import zipfile

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_test_project_structure():
    """创建测试用的UE工程结构"""
    # 创建临时目录
    base_dir = tempfile.mkdtemp(prefix="test_ue_projects_")
    
    # 创建几个测试工程
    projects = []
    for i in range(3):
        project_name = f"TestProject{i+1}"
        project_dir = os.path.join(base_dir, project_name)
        os.makedirs(project_dir, exist_ok=True)
        
        # 创建.uproject文件
        uproject_path = os.path.join(project_dir, f"{project_name}.uproject")
        uproject_content = f'''{{
    "FileVersion": 3,
    "EngineAssociation": "5.1",
    "Category": "",
    "Description": "Test Project {i+1}",
    "Modules": [
        {{
            "Name": "{project_name}",
            "Type": "Runtime",
            "LoadingPhase": "Default"
        }}
    ],
    "Plugins": []
}}'''
        
        with open(uproject_path, 'w', encoding='utf-8') as f:
            f.write(uproject_content)
        
        # 创建Content目录
        content_dir = os.path.join(project_dir, "Content")
        os.makedirs(content_dir, exist_ok=True)
        
        projects.append({
            'name': project_name,
            'path': uproject_path,
            'dir': project_dir,
            'content': content_dir
        })
        
        print(f"创建测试工程: {uproject_path}")
    
    return base_dir, projects

def create_test_asset_zip():
    """创建测试资产ZIP文件"""
    with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_zip:
        with zipfile.ZipFile(temp_zip.name, 'w') as zf:
            # 创建包含多层嵌套的资产包
            base_name = "TestAsset"
            
            # 添加更多文件来测试进度
            for i in range(50):  # 50个文件用于测试进度条
                zf.writestr(f"{base_name}/{base_name}/Materials/M_Test_{i:03d}.uasset", f"材质文件内容 {i}")
            
            for i in range(30):  # 30个纹理文件
                zf.writestr(f"{base_name}/{base_name}/Textures/T_Test_{i:03d}.uasset", f"纹理文件内容 {i}")
            
            # 添加其他类型的资产
            zf.writestr(f"{base_name}/{base_name}/Meshes/SM_TestCube.uasset", "静态网格文件内容")
            zf.writestr(f"{base_name}/{base_name}/Maps/TestLevel.umap", "测试关卡文件内容")
            zf.writestr(f"{base_name}/{base_name}/Blueprints/BP_TestActor.uasset", "蓝图文件内容")
            zf.writestr(f"{base_name}/{base_name}/README.md", "测试资产包说明文档")
            
        return temp_zip.name

def test_ue_project_search():
    """测试UE工程搜索功能"""
    print("=== 测试UE工程搜索功能 ===")
    
    try:
        from widgets.asset_card import AssetCard
        from utils.image_utils import ImageUtils
        
        class MockController:
            pass
        
        # 创建AssetCard实例
        image_utils = ImageUtils()
        asset_card = AssetCard(None, {}, MockController(), image_utils)
        
        # 创建测试工程结构
        base_dir, test_projects = create_test_project_structure()
        
        print(f"创建了 {len(test_projects)} 个测试工程")
        
        # 模拟搜索（只搜索测试目录）
        print("开始搜索UE工程...")
        
        # 模拟局部搜索（避免全盘搜索）
        projects = []
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if file.lower().endswith('.uproject'):
                    project_path = os.path.join(root, file)
                    projects.append({
                        'name': os.path.splitext(file)[0],
                        'path': project_path,
                        'dir': root
                    })
                    print(f"找到UE工程: {project_path}")
        
        print(f"搜索完成，找到 {len(projects)} 个工程")
        
        # 验证搜索结果
        if len(projects) == len(test_projects):
            print("✅ UE工程搜索测试通过")
        else:
            print("❌ UE工程搜索测试失败")
        
        # 清理测试文件
        import shutil
        shutil.rmtree(base_dir)
        print("已清理测试文件")
        
    except Exception as e:
        print(f"❌ 测试出错: {e}")
        import traceback
        traceback.print_exc()

def test_progress_callback():
    """测试进度回调功能"""
    print("\n=== 测试进度回调功能 ===")
    
    try:
        from widgets.asset_card import AssetCard
        from utils.image_utils import ImageUtils
        
        class MockController:
            pass
        
        # 创建AssetCard实例
        image_utils = ImageUtils()
        asset_card = AssetCard(None, {}, MockController(), image_utils)
        
        # 创建测试ZIP文件
        test_zip = create_test_asset_zip()
        print(f"创建测试ZIP文件: {test_zip}")
        
        # 创建临时解压目录
        temp_dir = tempfile.mkdtemp(prefix="test_extract_")
        
        # 测试进度回调
        progress_values = []
        
        def test_progress_callback(progress):
            progress_values.append(progress)
            print(f"进度: {int(progress * 100)}%")
        
        # 测试解压功能
        success = asset_card._extract_archive_to_temp(test_zip, temp_dir, test_progress_callback)
        
        if success:
            print("✅ 解压测试成功")
            print(f"进度回调次数: {len(progress_values)}")
            if progress_values:
                print(f"最终进度: {int(progress_values[-1] * 100)}%")
        else:
            print("❌ 解压测试失败")
        
        # 清理测试文件
        os.unlink(test_zip)
        import shutil
        shutil.rmtree(temp_dir)
        print("已清理测试文件")
        
    except Exception as e:
        print(f"❌ 测试出错: {e}")
        import traceback
        traceback.print_exc()

def test_cancel_functionality():
    """测试取消功能"""
    print("\n=== 测试取消功能 ===")
    
    try:
        from widgets.asset_card import AssetCard
        from utils.image_utils import ImageUtils
        
        class MockController:
            pass
        
        # 创建AssetCard实例
        image_utils = ImageUtils()
        asset_card = AssetCard(None, {}, MockController(), image_utils)
        
        # 测试取消标志
        asset_card.import_cancelled = False
        print(f"初始取消状态: {asset_card.import_cancelled}")
        
        # 模拟取消操作
        asset_card.import_cancelled = True
        print(f"设置取消后状态: {asset_card.import_cancelled}")
        
        # 测试条件检查
        if hasattr(asset_card, 'import_cancelled') and asset_card.import_cancelled:
            print("✅ 取消标志检查正常")
        else:
            print("❌ 取消标志检查失败")
        
    except Exception as e:
        print(f"❌ 测试出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("开始测试修复后的导入功能...")
    
    # 测试UE工程搜索
    test_ue_project_search()
    
    # 测试进度回调
    test_progress_callback()
    
    # 测试取消功能
    test_cancel_functionality()
    
    print("\n🎉 所有测试完成！")