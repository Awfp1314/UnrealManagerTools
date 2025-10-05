#!/usr/bin/env python3
"""
安装项目依赖脚本
"""
import subprocess
import sys

def install_package(package):
    """安装Python包（添加国内镜像源作为备用）"""
    # 首先尝试使用默认源安装
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ 成功安装 {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"✗ 使用默认源安装 {package} 失败，尝试使用国内镜像源...")
        
    # 失败后尝试使用国内镜像源
    mirrors = [
        "https://pypi.tuna.tsinghua.edu.cn/simple/",  # 清华大学镜像源
        "https://mirrors.aliyun.com/pypi/simple/",     # 阿里云镜像源
        "https://pypi.douban.com/simple/",             # 豆瓣镜像源
        "https://mirrors.ustc.edu.cn/pypi/web/simple/" # 中科大镜像源
    ]
    
    for mirror in mirrors:
        try:
            print(f"  尝试使用镜像源: {mirror}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-i", mirror, package])
            print(f"✓ 使用镜像源成功安装 {package}")
            return True
        except subprocess.CalledProcessError:
            print(f"  使用 {mirror} 安装失败")
            continue
    
    print(f"✗ 所有镜像源都未能成功安装 {package}")
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
        print("请尝试以下方法手动安装失败的包：")
        print("1. 使用默认源：pip install py7zr customtkinter pillow")
        print("2. 使用清华镜像源：pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ py7zr customtkinter pillow")
        print("3. 使用阿里云镜像源：pip install -i https://mirrors.aliyun.com/pypi/simple/ py7zr customtkinter pillow")
        print("4. 使用豆瓣镜像源：pip install -i https://pypi.douban.com/simple/ py7zr customtkinter pillow")
        print("5. 使用中科大镜像源：pip install -i https://mirrors.ustc.edu.cn/pypi/web/simple/ py7zr customtkinter pillow")

if __name__ == "__main__":
    main()