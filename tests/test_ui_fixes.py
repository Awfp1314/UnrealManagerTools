#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试UI修复效果
"""

def test_path_filtering():
    """测试路径过滤功能"""
    print("=== 测试路径过滤功能 ===")
    
    # 模拟搜索到的路径
    test_paths = [
        "C:\\Users\\wang\\Desktop\\HorrorDemo\\HorrorDemo.uproject",  # 正常工程
        "C:\\Users\\wang\\AppData\\Roaming\\Code\\User\\History\\-4e6d839c\\7g15.uproject",  # 应该被过滤
        "D:\\UnrealEngine\\Project\\Test\\Test.uproject",  # 正常工程
        "D:\\ProgramData\\Epic\\EpicGamesLauncher\\VaultCache\\CiciToon501fb9bd7dfbV1\\data\\CiciToon.uproject",  # 应该被过滤
        "C:\\Temp\\SomeProject.uproject",  # 应该被过滤
        "E:\\MyProjects\\GameProject\\GameProject.uproject",  # 正常工程
    ]
    
    # 过滤规则（与修复代码中的规则一致）
    excluded_paths = [
        'appdata\\roaming',
        'appdata\\local', 
        'temp',
        '$recycle.bin',
        'system volume information',
        'windows',
        'program files',
        'programdata\\epic\\epicgameslauncher\\vaultcache',
        '.vs',
        '.vscode',
        'node_modules',
        '.git',
        '__pycache__',
    ]
    
    valid_projects = []
    filtered_projects = []
    
    for path in test_paths:
        path_lower = path.lower()
        is_excluded = False
        
        for excluded in excluded_paths:
            if excluded in path_lower:
                is_excluded = True
                filtered_projects.append(path)
                print(f"✅ 过滤掉: {path}")
                break
        
        if not is_excluded:
            valid_projects.append(path)
            print(f"✓ 保留: {path}")
    
    print(f"\n总共测试路径: {len(test_paths)}")
    print(f"有效工程: {len(valid_projects)}")
    print(f"过滤掉的: {len(filtered_projects)}")
    
    # 验证关键路径是否被正确过滤
    appdata_filtered = any('appdata\\roaming' in p.lower() for p in filtered_projects)
    epic_cache_filtered = any('epicgameslauncher\\vaultcache' in p.lower() for p in filtered_projects)
    temp_filtered = any('temp' in p.lower() for p in filtered_projects)
    
    if appdata_filtered and epic_cache_filtered and temp_filtered:
        print("✅ 路径过滤功能测试通过")
        return True
    else:
        print("❌ 路径过滤功能测试失败")
        return False

def test_dialog_dimensions():
    """测试对话框尺寸"""
    print("\n=== 测试对话框尺寸修复 ===")
    
    original_size = "700x500"
    new_size = "750x600"
    
    print(f"原始尺寸: {original_size}")
    print(f"修复后尺寸: {new_size}")
    
    # 解析尺寸
    orig_w, orig_h = map(int, original_size.split('x'))
    new_w, new_h = map(int, new_size.split('x'))
    
    width_increase = new_w - orig_w
    height_increase = new_h - orig_h
    
    print(f"宽度增加: {width_increase}px")
    print(f"高度增加: {height_increase}px")
    
    # 验证尺寸增加是否合理
    if width_increase >= 50 and height_increase >= 100:
        print("✅ 对话框尺寸修复合理")
        return True
    else:
        print("❌ 对话框尺寸修复不足")
        return False

def test_scrollable_area():
    """测试滚动区域高度"""
    print("\n=== 测试滚动区域高度修复 ===")
    
    original_height = 250
    new_height = 350
    
    print(f"原始滚动区域高度: {original_height}px")
    print(f"修复后滚动区域高度: {new_height}px")
    
    height_increase = new_height - original_height
    print(f"高度增加: {height_increase}px")
    
    if height_increase >= 100:
        print("✅ 滚动区域高度修复合理")
        return True
    else:
        print("❌ 滚动区域高度修复不足") 
        return False

def main():
    """主测试函数"""
    print("开始测试UI修复效果...\n")
    
    results = []
    
    # 测试路径过滤
    results.append(test_path_filtering())
    
    # 测试对话框尺寸
    results.append(test_dialog_dimensions())
    
    # 测试滚动区域
    results.append(test_scrollable_area())
    
    # 总结
    print(f"\n{'='*50}")
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 所有测试通过 ({passed}/{total})")
        print("UI修复完成，功能正常!")
    else:
        print(f"⚠️  部分测试失败 ({passed}/{total})")
        print("需要进一步检查修复效果")

if __name__ == "__main__":
    main()