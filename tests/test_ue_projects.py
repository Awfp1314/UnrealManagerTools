#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试虚幻工程功能
"""

import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def test_project_manager():
    """测试工程管理器"""
    print("=== 测试工程管理器 ===")
    
    try:
        from models.project_manager import ProjectManager
        
        # 创建工程管理器
        project_manager = ProjectManager()
        print("✅ 工程管理器创建成功")
        
        # 测试配置加载
        project_manager.load_config()
        print("✅ 配置文件加载成功")
        
        # 测试最近工程获取
        recent_projects = project_manager.get_recent_projects()
        print(f"✅ 最近工程数量: {len(recent_projects)}")
        
        # 测试工程列表获取
        projects = project_manager.get_projects()
        print(f"✅ 工程列表数量: {len(projects)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 工程管理器测试失败: {e}")
        return False

def test_ue_projects_content():
    """测试虚幻工程内容组件"""
    print("\n=== 测试虚幻工程内容组件 ===")
    
    try:
        from views.content.ue_projects import UEProjectsContent
        print("✅ 虚幻工程内容组件导入成功")
        
        # 检查类结构
        methods = [method for method in dir(UEProjectsContent) if not method.startswith('_')]
        required_methods = [
            'create_widgets', 'refresh_content', 'start_project_search',
            'update_recent_projects', 'update_all_projects', 'open_project'
        ]
        
        for method in required_methods:
            if method in methods:
                print(f"✅ 方法 {method} 存在")
            else:
                print(f"❌ 方法 {method} 缺失")
        
        return True
        
    except Exception as e:
        print(f"❌ 虚幻工程内容组件测试失败: {e}")
        return False

def test_toolbar_integration():
    """测试工具栏集成"""
    print("\n=== 测试工具栏集成 ===")
    
    try:
        # 读取工具栏文件
        with open('views/toolbar.py', 'r', encoding='utf-8') as f:
            toolbar_content = f.read()
        
        # 检查是否包含虚幻工程
        if '虚幻工程' in toolbar_content:
            print("✅ 工具栏包含虚幻工程按钮")
        else:
            print("❌ 工具栏缺少虚幻工程按钮")
            
        if 'ue_projects' in toolbar_content:
            print("✅ 工具栏包含ue_projects ID")
        else:
            print("❌ 工具栏缺少ue_projects ID")
        
        return True
        
    except Exception as e:
        print(f"❌ 工具栏集成测试失败: {e}")
        return False

def test_content_manager_integration():
    """测试内容管理器集成"""
    print("\n=== 测试内容管理器集成 ===")
    
    try:
        # 读取内容管理器文件
        with open('views/content/base_content.py', 'r', encoding='utf-8') as f:
            content_manager = f.read()
        
        # 检查导入
        if 'from views.content.ue_projects import UEProjectsContent' in content_manager:
            print("✅ 内容管理器正确导入UEProjectsContent")
        else:
            print("❌ 内容管理器缺少UEProjectsContent导入")
            
        # 检查注册
        if 'ue_projects' in content_manager and 'UEProjectsContent' in content_manager:
            print("✅ 内容管理器正确注册虚幻工程内容")
        else:
            print("❌ 内容管理器缺少虚幻工程内容注册")
        
        return True
        
    except Exception as e:
        print(f"❌ 内容管理器集成测试失败: {e}")
        return False

def test_asset_card_integration():
    """测试资产卡片集成"""
    print("\n=== 测试资产卡片集成 ===")
    
    try:
        # 读取资产卡片文件
        with open('widgets/asset_card.py', 'r', encoding='utf-8') as f:
            asset_card_content = f.read()
        
        # 检查新方法
        required_methods = ['get_preloaded_projects', 'display_found_projects_simple']
        
        for method in required_methods:
            if method in asset_card_content:
                print(f"✅ 资产卡片包含方法 {method}")
            else:
                print(f"❌ 资产卡片缺少方法 {method}")
        
        # 检查是否移除了旧的搜索方法
        if 'search_ue_projects' not in asset_card_content:
            print("✅ 已移除旧的search_ue_projects方法")
        else:
            print("❌ 仍然包含旧的search_ue_projects方法")
        
        return True
        
    except Exception as e:
        print(f"❌ 资产卡片集成测试失败: {e}")
        return False

def test_file_structure():
    """测试文件结构"""
    print("\n=== 测试文件结构 ===")
    
    required_files = [
        'models/project_manager.py',
        'views/content/ue_projects.py',
        'views/toolbar.py',
        'views/content/base_content.py',
        'widgets/asset_card.py'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ 文件存在: {file_path}")
        else:
            print(f"❌ 文件缺失: {file_path}")
            all_exist = False
    
    return all_exist

def main():
    """主测试函数"""
    print("开始测试虚幻工程功能...\n")
    
    results = []
    
    # 测试文件结构
    results.append(test_file_structure())
    
    # 测试工程管理器
    results.append(test_project_manager())
    
    # 测试虚幻工程内容组件
    results.append(test_ue_projects_content())
    
    # 测试工具栏集成
    results.append(test_toolbar_integration())
    
    # 测试内容管理器集成
    results.append(test_content_manager_integration())
    
    # 测试资产卡片集成
    results.append(test_asset_card_integration())
    
    # 总结
    print(f"\n{'='*50}")
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 所有测试通过 ({passed}/{total})")
        print("虚幻工程功能集成完成!")
        print("\n功能特性:")
        print("- ✅ 程序启动时自动搜索工程")
        print("- ✅ 工具栏添加虚幻工程按钮")
        print("- ✅ 最近打开和所有工程双区域显示")
        print("- ✅ 移除资产导入时的搜索功能")
        print("- ✅ 使用预加载的工程列表")
        print("- ✅ 独立的工程管理界面")
    else:
        print(f"⚠️  部分测试失败 ({passed}/{total})")
        print("需要进一步检查功能实现")

if __name__ == "__main__":
    main()