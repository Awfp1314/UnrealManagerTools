#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安装psutil库的脚本
"""

import subprocess
import sys

def install_psutil():
    """安装psutil库（添加国内镜像源作为备用）"""
    print("正在安装psutil库...")
    
    # 首先尝试使用默认源安装
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', 'psutil'], 
                               capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ psutil库安装成功！")
            print("现在可以正常使用UE工程搜索功能了。")
            return
        else:
            print("❌ 使用默认源安装psutil库失败")
            print("错误信息:", result.stderr)
    except Exception as e:
        print(f"❌ 使用默认源安装过程中出错: {e}")
    
    # 失败后尝试使用国内镜像源
    print("尝试使用国内镜像源安装...")
    mirrors = [
        "https://pypi.tuna.tsinghua.edu.cn/simple/",  # 清华大学镜像源
        "https://mirrors.aliyun.com/pypi/simple/",     # 阿里云镜像源
        "https://pypi.douban.com/simple/",             # 豆瓣镜像源
        "https://mirrors.ustc.edu.cn/pypi/web/simple/" # 中科大镜像源
    ]
    
    for mirror in mirrors:
        try:
            print(f"  尝试使用镜像源: {mirror}")
            result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-i', mirror, 'psutil'], 
                                   capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ 使用镜像源成功安装psutil库！")
                print("现在可以正常使用UE工程搜索功能了。")
                return
            else:
                print(f"  使用 {mirror} 安装失败")
                print("  错误信息:", result.stderr)
        except Exception as e:
            print(f"  使用 {mirror} 安装过程中出错: {e}")
            continue
    
    print("❌ 所有镜像源都未能成功安装psutil库")
    print("\n备选方案：程序会自动使用备用搜索方法，功能仍可正常使用。")

if __name__ == "__main__":
    install_psutil()
    input("按回车键退出...")