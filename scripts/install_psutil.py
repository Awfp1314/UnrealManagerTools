#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安装psutil库的脚本
"""

import subprocess
import sys

def install_psutil():
    """安装psutil库"""
    try:
        print("正在安装psutil库...")
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', 'psutil'], 
                               capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ psutil库安装成功！")
            print("现在可以正常使用UE工程搜索功能了。")
        else:
            print("❌ psutil库安装失败")
            print("错误信息:", result.stderr)
            print("\n备选方案：程序会自动使用备用搜索方法，功能仍可正常使用。")
            
    except Exception as e:
        print(f"❌ 安装过程中出错: {e}")
        print("\n备选方案：程序会自动使用备用搜索方法，功能仍可正常使用。")

if __name__ == "__main__":
    install_psutil()
    input("按回车键退出...")