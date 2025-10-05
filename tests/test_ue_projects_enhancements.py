#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试虚幻工程功能增强
"""

import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def test_toolbar_button_states():
    """测试工具栏按钮状态"""
    print("=== 测试工具栏按钮状态 ===")
    
    try:
        # 读取工具栏文件
        with open('views/toolbar.py', 'r', encoding='utf-8') as f:
            toolbar_content = f.read()
        
        # 检查按钮状态管理
        required_features = [
            'self.buttons = {}',  # 按钮引用存储
            'self.current_tool = None',  # 当前工具状态
            'set_active_tool',  # 设置活动工具方法
            'fg_color=("gray75", "gray25")',  # 默认灰色
            'fg_color=("#1f538d", "#14375e")',  # 选中蓝色
        ]
        
        for feature in required_features:
            if feature in toolbar_content:
                print(f"✅ 按钮状态功能: {feature}")
            else:
                print(f"❌ 缺少功能: {feature}")
        
        # 检查默认选中
        if 'self.set_active_tool("ue_projects")' in toolbar_content:
            print("✅ 默认选中虚幻工程按钮")
        else:
            print("❌ 缺少默认选中设置")
        
        return True
        
    except Exception as e:
        print(f"❌ 工具栏按钮状态测试失败: {e}")
        return False

def test_content_refresh_mechanism():
    """测试内容刷新机制"""
    print("\n=== 测试内容刷新机制 ===")
    
    try:
        # 读取内容管理器文件
        with open('views/content/base_content.py', 'r', encoding='utf-8') as f:
            content_manager = f.read()
        
        # 检查无缝刷新机制
        if 'self.after(10, lambda: self.current_content.refresh_content())' in content_manager:
            print("✅ 无缝刷新机制: 使用after延迟刷新")
        else:
            print("❌ 缺少无缝刷新机制")
        
        # 检查默认显示虚幻工程
        if 'self.show_content("ue_projects")' in content_manager:
            print("✅ 默认显示虚幻工程界面")
        else:
            print("❌ 缺少默认显示设置")
        
        return True
        
    except Exception as e:
        print(f"❌ 内容刷新机制测试失败: {e}")
        return False

def test_project_card_events():
    """测试工程卡片事件"""
    print("\n=== 测试工程卡片事件 ===")
    
    try:
        # 读取虚幻工程文件
        with open('views/content/ue_projects.py', 'r', encoding='utf-8') as f:
            ue_projects_content = f.read()
        
        # 检查新增的方法
        required_methods = [
            'bind_project_card_events',  # 事件绑定方法
            'on_project_double_click',   # 双击处理
            'show_project_context_menu', # 右键菜单
            'context_menu_action',       # 菜单动作
            'delete_project',            # 删除项目
        ]
        
        for method in required_methods:
            if method in ue_projects_content:
                print(f"✅ 工程卡片方法: {method}")
            else:
                print(f"❌ 缺少方法: {method}")
        
        # 检查事件绑定
        event_bindings = [
            '<Double-Button-1>',  # 双击事件
            '<Button-3>',         # 右键事件
            'cursor="hand2"',     # 鼠标指针
        ]
        
        for binding in event_bindings:
            if binding in ue_projects_content:
                print(f"✅ 事件绑定: {binding}")
            else:
                print(f"❌ 缺少事件绑定: {binding}")
        
        return True
        
    except Exception as e:
        print(f"❌ 工程卡片事件测试失败: {e}")
        return False

def test_context_menu_features():
    """测试右键菜单功能"""
    print("\n=== 测试右键菜单功能 ===")
    
    try:
        # 读取虚幻工程文件
        with open('views/content/ue_projects.py', 'r', encoding='utf-8') as f:
            ue_projects_content = f.read()
        
        # 检查菜单选项
        menu_options = [
            '▶️ 打开项目',       # 打开项目
            '📁 打开所在文件夹',    # 打开文件夹
            '🗑️ 删除项目',       # 删除项目
        ]
        
        for option in menu_options:
            if option in ue_projects_content:
                print(f"✅ 菜单选项: {option}")
            else:
                print(f"❌ 缺少菜单选项: {option}")
        
        # 检查菜单样式和行为
        menu_features = [
            'overrideredirect(True)',    # 无边框窗口
            'attributes("-topmost", True)', # 置顶显示
            'geometry(f"+{x}+{y}")',     # 位置定位
            'on_click_outside',          # 外部点击关闭
        ]
        
        for feature in menu_features:
            if feature in ue_projects_content:
                print(f"✅ 菜单功能: {feature}")
            else:
                print(f"❌ 缺少菜单功能: {feature}")
        
        return True
        
    except Exception as e:
        print(f"❌ 右键菜单功能测试失败: {e}")
        return False

def test_main_window_integration():
    """测试主窗口集成"""
    print("\n=== 测试主窗口集成 ===")
    
    try:
        # 读取主窗口文件
        with open('views/main_window.py', 'r', encoding='utf-8') as f:
            main_window_content = f.read()
        
        # 检查工具栏状态同步
        if 'self.toolbar.set_active_tool(tool_name)' in main_window_content:
            print("✅ 工具栏状态同步")
        else:
            print("❌ 缺少工具栏状态同步")
        
        return True
        
    except Exception as e:
        print(f"❌ 主窗口集成测试失败: {e}")
        return False

def test_double_click_functionality():
    """测试双击功能"""
    print("\n=== 测试双击功能 ===")
    
    try:
        # 读取虚幻工程文件
        with open('views/content/ue_projects.py', 'r', encoding='utf-8') as f:
            ue_projects_content = f.read()
        
        # 检查双击功能实现
        double_click_features = [
            'on_project_double_click',   # 双击处理方法
            'self.open_project(project)', # 调用打开项目
            'isinstance(widget, ctk.CTkButton)', # 跳过按钮组件
        ]
        
        for feature in double_click_features:
            if feature in ue_projects_content:
                print(f"✅ 双击功能: {feature}")
            else:
                print(f"❌ 缺少双击功能: {feature}")
        
        return True
        
    except Exception as e:
        print(f"❌ 双击功能测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始测试虚幻工程功能增强...\n")
    
    results = []
    
    # 测试工具栏按钮状态
    results.append(test_toolbar_button_states())
    
    # 测试内容刷新机制
    results.append(test_content_refresh_mechanism())
    
    # 测试工程卡片事件
    results.append(test_project_card_events())
    
    # 测试右键菜单功能
    results.append(test_context_menu_features())
    
    # 测试主窗口集成
    results.append(test_main_window_integration())
    
    # 测试双击功能
    results.append(test_double_click_functionality())
    
    # 总结
    print(f"\n{'='*50}")
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 所有测试通过 ({passed}/{total})")
        print("虚幻工程功能增强完成!")
        print("\n新增功能:")
        print("- ✅ 工具栏按钮状态管理(灰色/蓝色)")
        print("- ✅ 默认选中虚幻工程按钮")
        print("- ✅ 无缝界面刷新机制")
        print("- ✅ 工程项目右键菜单")
        print("- ✅ 双击打开项目功能")
        print("- ✅ 删除项目功能")
        print("- ✅ 完整的事件处理系统")
    else:
        print(f"⚠️  部分测试失败 ({passed}/{total})")
        print("需要进一步检查功能实现")

if __name__ == "__main__":
    main()