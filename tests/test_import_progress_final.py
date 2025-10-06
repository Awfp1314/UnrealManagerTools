#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终测试导入过程中的进度条更新
"""

import os
import sys
import tempfile
import zipfile
import shutil
import threading
import time

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
    return project_dir, uproject_path, content_dir

def create_test_asset_zip():
    """创建一个测试用的资产ZIP文件"""
    with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_zip:
        with zipfile.ZipFile(temp_zip.name, 'w') as zf:
            # 创建包含多层嵌套的资产包
            base_name = "TestAsset"
            
            # 添加更多文件来测试进度
            for i in range(30):  # 30个文件用于测试进度条
                zf.writestr(f"{base_name}/{base_name}/Materials/M_Test_{i:03d}.uasset", f"材质文件内容 {i}")
            
            for i in range(20):  # 20个纹理文件
                zf.writestr(f"{base_name}/{base_name}/Textures/T_Test_{i:03d}.uasset", f"纹理文件内容 {i}")
            
            # 添加其他类型的资产
            zf.writestr(f"{base_name}/{base_name}/Meshes/SM_TestCube.uasset", "静态网格文件内容")
            zf.writestr(f"{base_name}/{base_name}/Maps/TestLevel.umap", "测试关卡文件内容")
            zf.writestr(f"{base_name}/{base_name}/Blueprints/BP_TestActor.uasset", "蓝图文件内容")
            zf.writestr(f"{base_name}/{base_name}/README.md", "测试资产包说明文档")
            
        return temp_zip.name

def test_import_with_progress():
    """测试导入过程中的进度条更新"""
    print("=== 测试导入过程中的进度条更新 ===")
    
    try:
        # 创建测试项目和资产
        project_dir, uproject_path, content_dir = create_test_project()
        test_zip = create_test_asset_zip()
        
        print(f"创建测试ZIP文件: {test_zip}")
        
        # 导入必要的模块
        from widgets.asset_card import AssetCard
        from utils.image_utils import ImageUtils
        import customtkinter as ctk
        
        # 设置customtkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # 创建模拟控制器
        class MockController:
            def show_status(self, message, status_type="info"):
                print(f"[状态] {message}")
        
        # 创建AssetCard实例
        image_utils = ImageUtils()
        asset_card = AssetCard(None, {}, MockController(), image_utils)
        
        # 记录进度更新
        progress_updates = []
        
        # 创建进度回调函数
        def progress_callback(progress):
            progress_updates.append(progress)
            print(f"进度更新: {int(progress * 100)}%")
        
        # 在新线程中执行导入，避免阻塞GUI
        def run_import():
            try:
                # 测试导入功能
                asset_card.import_cancelled = False  # 确保没有取消标志
                success = asset_card.import_single_archive_to_content(test_zip, content_dir, progress_callback)
                
                if success:
                    print("✅ 导入测试成功")
                    # 检查导入的文件
                    imported_path = os.path.join(content_dir, "TestAsset")
                    if os.path.exists(imported_path):
                        print(f"✅ 资产已成功导入到: {imported_path}")
                    else:
                        print("❌ 资产未正确导入")
                else:
                    print("❌ 导入测试失败")
                
                # 输出进度更新统计
                print(f"总共进度更新次数: {len(progress_updates)}")
                if progress_updates:
                    print(f"最终进度: {int(progress_updates[-1] * 100)}%")
                    print(f"进度更新详情: {[int(p * 100) for p in progress_updates]}")
                
            except Exception as e:
                print(f"导入过程中出错: {e}")
                import traceback
                traceback.print_exc()
            finally:
                # 清理测试文件
                try:
                    os.unlink(test_zip)
                    shutil.rmtree(project_dir)
                    print("已清理测试文件")
                except:
                    pass
        
        # 启动导入线程
        import_thread = threading.Thread(target=run_import, daemon=True)
        import_thread.start()
        
        # 等待导入完成
        import_thread.join(timeout=30)  # 最多等待30秒
        
        if import_thread.is_alive():
            print("⚠️  导入超时")
            return False
        else:
            print("✅ 导入线程已完成")
            return True
        
    except Exception as e:
        print(f"❌ 测试出错: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("开始测试导入过程中的进度条更新...")
    success = test_import_with_progress()
    if success:
        print("\n🎉 导入进度条更新测试完成！")
    else:
        print("\n❌ 导入进度条更新测试失败！")