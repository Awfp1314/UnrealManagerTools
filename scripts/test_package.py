#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试打包脚本功能的简单工具
此脚本用于验证package.py的基本功能是否正常工作
"""

import os
import sys
import subprocess
import time

# 获取项目根目录
sCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(sCRIPT_DIR)

def check_package_script():
    """检查打包脚本是否存在并能正常运行基本功能"""
    print("=== UE资源管理器打包脚本测试 ===")
    
    # 检查package.py是否存在
    package_path = os.path.join(PROJECT_ROOT, "package.py")
    if not os.path.exists(package_path):
        print(f"错误: 未找到package.py文件，路径: {package_path}")
        return False
    
    print("✓ 找到了package.py文件")
    
    # 检查requirements.txt是否存在且包含必要依赖
    req_path = os.path.join(PROJECT_ROOT, "requirements.txt")
    if not os.path.exists(req_path):
        print(f"错误: 未找到requirements.txt文件，路径: {req_path}")
        return False
    
    with open(req_path, "r") as f:
        content = f.read()
        required_deps = ["py7zr", "customtkinter", "pillow", "pyinstaller", "psutil"]
        missing_deps = []
        
        for dep in required_deps:
            if dep not in content:
                missing_deps.append(dep)
        
        if missing_deps:
            print(f"错误: requirements.txt缺少必要依赖: {', '.join(missing_deps)}")
            return False
    
    print("✓ requirements.txt包含所有必要依赖")
    
    # 尝试运行package.py的依赖检查部分（不实际打包）
    print("\n开始测试package.py...")
    try:
        # 运行package.py的简化版本，仅检查依赖
        result = subprocess.run([sys.executable, package_path, "--check"], 
                               capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✓ package.py依赖检查通过")
        else:
            print(f"错误: package.py依赖检查失败\n{result.stderr}")
            return False
    except Exception as e:
        print(f"错误: 运行package.py时出现异常: {str(e)}")
        return False
    
    print("\n=== 测试完成 ===")
    print("提示: 要完整测试打包功能，请直接运行 'python ../package.py'")
    return True

if __name__ == "__main__":
    # 添加--check参数支持到package.py的逻辑（如果需要）
    # 这里我们先简单检查文件结构和基本依赖
    success = check_package_script()
    sys.exit(0 if success else 1)