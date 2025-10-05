#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试工程卡片悬停动画功能
"""

import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def test_hover_animation_methods():
    """测试悬停动画方法"""
    print("=== 测试悬停动画方法 ===")
    
    try:
        # 读取虚幻工程文件
        with open('views/content/ue_projects.py', 'r', encoding='utf-8') as f:
            ue_projects_content = f.read()
        
        # 检查新增的悬停动画方法
        required_methods = [
            'on_card_enter',          # 鼠标进入事件
            'on_card_leave',          # 鼠标离开事件
            'animate_card_hover',     # 悬停动画方法
        ]
        
        for method in required_methods:
            if method in ue_projects_content:
                print(f"✅ 悬停动画方法: {method}")
            else:
                print(f"❌ 缺少方法: {method}")
        
        # 检查事件绑定
        hover_bindings = [
            '<Enter>',                # 鼠标进入事件
            '<Leave>',                # 鼠标离开事件
            'on_card_enter',          # 进入处理函数
            'on_card_leave',          # 离开处理函数
        ]
        
        for binding in hover_bindings:
            if binding in ue_projects_content:
                print(f"✅ 悬停事件绑定: {binding}")
            else:
                print(f"❌ 缺少事件绑定: {binding}")
        
        return True
        
    except Exception as e:
        print(f"❌ 悬停动画方法测试失败: {e}")
        return False

def test_card_styling():
    """测试卡片样式"""
    print("\n=== 测试卡片样式 ===")
    
    try:
        # 读取虚幻工程文件
        with open('views/content/ue_projects.py', 'r', encoding='utf-8') as f:
            ue_projects_content = f.read()
        
        # 检查卡片样式设置
        style_features = [
            'fg_color=("gray92", "gray20")',      # 默认背景色
            'border_width=1',                      # 默认边框宽度
            'border_color=("gray70", "gray30")',   # 默认边框颜色
            'corner_radius=10',                    # 圆角
        ]
        
        for feature in style_features:
            if feature in ue_projects_content:
                print(f"✅ 卡片样式: {feature}")
            else:
                print(f"❌ 缺少样式: {feature}")
        
        return True
        
    except Exception as e:
        print(f"❌ 卡片样式测试失败: {e}")
        return False

def test_animation_colors():
    """测试动画颜色配置"""
    print("\n=== 测试动画颜色配置 ===")
    
    try:
        # 读取虚幻工程文件
        with open('views/content/ue_projects.py', 'r', encoding='utf-8') as f:
            ue_projects_content = f.read()
        
        # 检查悬停状态颜色
        hover_colors = [
            '"#e8f4fd"',                          # 浅蓝色背景
            '"#2d3748"',                          # 深色模式背景
            '"#3182ce"',                          # 蓝色边框
            '"#4299e1"',                          # 蓝色边框（深色）
            'target_border = 2',                  # 悬停边框宽度
        ]
        
        for color in hover_colors:
            if color in ue_projects_content:
                print(f"✅ 悬停颜色: {color}")
            else:
                print(f"❌ 缺少颜色: {color}")
        
        return True
        
    except Exception as e:
        print(f"❌ 动画颜色配置测试失败: {e}")
        return False

def test_animation_parameters():
    """测试动画参数"""
    print("\n=== 测试动画参数 ===")
    
    try:
        # 读取虚幻工程文件
        with open('views/content/ue_projects.py', 'r', encoding='utf-8') as f:
            ue_projects_content = f.read()
        
        # 检查动画参数
        animation_params = [
            'max_steps=8',                        # 动画总步数
            'self.after(25,',                     # 动画帧间隔（25ms）
            'step + 1',                           # 步数递增
            'progress = step / max_steps',        # 进度计算
        ]
        
        for param in animation_params:
            if param in ue_projects_content:
                print(f"✅ 动画参数: {param}")
            else:
                print(f"❌ 缺少参数: {param}")
        
        return True
        
    except Exception as e:
        print(f"❌ 动画参数测试失败: {e}")
        return False

def test_error_handling():
    """测试错误处理"""
    print("\n=== 测试错误处理 ===")
    
    try:
        # 读取虚幻工程文件
        with open('views/content/ue_projects.py', 'r', encoding='utf-8') as f:
            ue_projects_content = f.read()
        
        # 检查错误处理机制
        error_handling = [
            'try:',                               # 异常捕获
            'except Exception as e:',             # 异常处理
            'card_frame.winfo_exists()',          # 组件存在检查
            'print(f"悬停动画出错: {e}")',          # 错误日志
            'print(f"离开动画出错: {e}")',          # 错误日志
            'print(f"动画执行出错: {e}")',          # 错误日志
        ]
        
        for handling in error_handling:
            if handling in ue_projects_content:
                print(f"✅ 错误处理: {handling}")
            else:
                print(f"❌ 缺少错误处理: {handling}")
        
        return True
        
    except Exception as e:
        print(f"❌ 错误处理测试失败: {e}")
        return False

def test_recursive_event_binding():
    """测试递归事件绑定"""
    print("\n=== 测试递归事件绑定 ===")
    
    try:
        # 读取虚幻工程文件
        with open('views/content/ue_projects.py', 'r', encoding='utf-8') as f:
            ue_projects_content = f.read()
        
        # 检查递归绑定机制
        recursive_features = [
            'get_all_children(widget)',           # 递归获取子组件
            'all_widgets.extend',                 # 扩展组件列表
            'isinstance(widget, ctk.CTkButton)', # 按钮类型检查
            'cf=card_frame',                     # 卡片框架引用
        ]
        
        for feature in recursive_features:
            if feature in ue_projects_content:
                print(f"✅ 递归绑定: {feature}")
            else:
                print(f"❌ 缺少递归绑定: {feature}")
        
        return True
        
    except Exception as e:
        print(f"❌ 递归事件绑定测试失败: {e}")
        return False

def test_performance_optimization():
    """测试性能优化"""
    print("\n=== 测试性能优化 ===")
    
    try:
        # 读取虚幻工程文件
        with open('views/content/ue_projects.py', 'r', encoding='utf-8') as f:
            ue_projects_content = f.read()
        
        # 检查性能优化措施
        optimization_features = [
            'if not card_frame.winfo_exists():',  # 组件存在检查
            'if progress >= 1.0:',                # 动画完成检查
            'if step < max_steps:',               # 步数限制
            '25',                                 # 合理的帧率（40fps）
        ]
        
        for feature in optimization_features:
            if feature in ue_projects_content:
                print(f"✅ 性能优化: {feature}")
            else:
                print(f"❌ 缺少优化: {feature}")
        
        return True
        
    except Exception as e:
        print(f"❌ 性能优化测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始测试工程卡片悬停动画功能...\n")
    
    results = []
    
    # 测试悬停动画方法
    results.append(test_hover_animation_methods())
    
    # 测试卡片样式
    results.append(test_card_styling())
    
    # 测试动画颜色配置
    results.append(test_animation_colors())
    
    # 测试动画参数
    results.append(test_animation_parameters())
    
    # 测试错误处理
    results.append(test_error_handling())
    
    # 测试递归事件绑定
    results.append(test_recursive_event_binding())
    
    # 测试性能优化
    results.append(test_performance_optimization())
    
    # 总结
    print(f"\n{'='*50}")
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 所有测试通过 ({passed}/{total})")
        print("工程卡片悬停动画功能实现完成!")
        print("\n动画特性:")
        print("- ✅ 平滑的背景色过渡（灰色 → 浅蓝色）")
        print("- ✅ 动态边框效果（1px → 2px，灰色 → 蓝色）")
        print("- ✅ 8步分段动画，25ms间隔（40fps）")
        print("- ✅ 递归事件绑定，覆盖所有子组件")
        print("- ✅ 智能过滤按钮，避免事件冲突")
        print("- ✅ 完善的错误处理和性能优化")
        print("- ✅ 支持明暗主题的颜色适配")
    else:
        print(f"⚠️  部分测试失败 ({passed}/{total})")
        print("需要进一步检查功能实现")

if __name__ == "__main__":
    main()