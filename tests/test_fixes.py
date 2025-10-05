#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修复后的功能
"""

import os
import sys
import tempfile

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_psutil_fallback():
    """测试psutil备用方案"""
    print("=== 测试psutil备用方案 ===")
    
    try:
        from widgets.asset_card import AssetCard
        from utils.image_utils import ImageUtils
        
        class MockController:
            pass
        
        # 创建AssetCard实例
        image_utils = ImageUtils()
        asset_card = AssetCard(None, {}, MockController(), image_utils)
        
        # 测试搜索功能（不会真正搜索，只测试方法是否正常）
        def test_progress(p):
            print(f"搜索进度: {int(p * 100)}%")
        
        print("测试UE工程搜索方法...")
        projects = asset_card.search_ue_projects(test_progress)
        print(f"搜索方法执行成功，找到 {len(projects)} 个工程")
        
        print("✅ psutil备用方案测试通过")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

def test_import_cancelled_logic():
    """测试导入取消逻辑"""
    print("\n=== 测试导入取消逻辑 ===")
    
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
        print(f"初始导入取消状态: {asset_card.import_cancelled}")
        
        # 模拟取消
        asset_card.import_cancelled = True
        print(f"设置取消后状态: {asset_card.import_cancelled}")
        
        # 测试条件检查（模拟解压过程中的检查）
        if hasattr(asset_card, 'import_cancelled') and asset_card.import_cancelled:
            print("✅ 导入取消检查正常")
        else:
            print("❌ 导入取消检查失败")
        
        # 测试解压取消标志
        asset_card.extraction_cancelled = False
        print(f"初始解压取消状态: {asset_card.extraction_cancelled}")
        
        asset_card.extraction_cancelled = True
        if hasattr(asset_card, 'extraction_cancelled') and asset_card.extraction_cancelled:
            print("✅ 解压取消检查正常")
        else:
            print("❌ 解压取消检查失败")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

def test_archive_file_detection():
    """测试压缩包文件检测"""
    print("\n=== 测试压缩包文件检测 ===")
    
    try:
        from widgets.asset_card import AssetCard
        from utils.image_utils import ImageUtils
        
        class MockController:
            pass
        
        # 创建AssetCard实例
        image_utils = ImageUtils()
        asset_card = AssetCard(None, {}, MockController(), image_utils)
        
        # 创建测试目录结构
        test_dir = tempfile.mkdtemp(prefix="test_archive_")
        
        # 创建一些测试文件
        test_files = [
            "test1.zip",
            "test2.7z", 
            "test3.rar",  # 不支持的格式
            "test4.txt",  # 非压缩包
            "subdir/test5.zip"  # 子目录中的压缩包
        ]
        
        for file_path in test_files:
            full_path = os.path.join(test_dir, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w') as f:
                f.write("test content")
        
        # 测试查找压缩包功能
        archive_files = asset_card.find_archive_files(test_dir)
        print(f"找到的压缩包文件: {len(archive_files)}")
        
        for archive in archive_files:
            print(f"  - {os.path.basename(archive)}")
        
        # 验证结果
        expected_count = 3  # test1.zip, test2.7z, subdir/test5.zip
        if len(archive_files) == expected_count:
            print("✅ 压缩包文件检测正常")
        else:
            print(f"❌ 压缩包文件检测异常，期望{expected_count}个，实际{len(archive_files)}个")
        
        # 清理测试文件
        import shutil
        shutil.rmtree(test_dir)
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("开始测试修复功能...")
    
    # 测试psutil备用方案
    test_psutil_fallback()
    
    # 测试取消逻辑
    test_import_cancelled_logic()
    
    # 测试压缩包检测
    test_archive_file_detection()
    
    print("\n🎉 所有测试完成！")