#!/usr/bin/env python3
"""
安装项目依赖脚本
"""
import subprocess
import sys

def install_package(package):
    """安装Python包"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ 成功安装 {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"✗ 安装 {package} 失败")
        return False

def main():
    """主函数"""
    print("正在安装项目依赖...")
    
    # 需要安装的包
    packages = [
        "py7zr",  # 用于7z文件解压
        "customtkinter",  # GUI框架
        "pillow",  # 图像处理
    ]
    
    success_count = 0
    for package in packages:
        if install_package(package):
            success_count += 1
    
    print(f"\n安装完成：{success_count}/{len(packages)} 个包安装成功")
    
    if success_count == len(packages):
        print("✓ 所有依赖安装完成，可以正常运行程序")
    else:
        print("⚠ 部分依赖安装失败，程序可能无法正常运行")
        print("请手动安装失败的包：")
        print("pip install py7zr customtkinter pillow")

if __name__ == "__main__":
    main()