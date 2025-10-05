#!/usr/bin/env python3
"""
解压功能测试脚本
"""
import os
import sys
import zipfile
import py7zr
from pathlib import Path

def test_extraction():
    """测试解压功能"""
    print("=== 解压功能测试 ===")
    
    # 测试目录
    test_dir = r"E:\UE_Asset\Backroom"  # 根据您之前提到的路径
    
    if not os.path.exists(test_dir):
        print(f"测试目录不存在: {test_dir}")
        print("请修改 test_dir 变量为实际的资源目录")
        return
    
    print(f"扫描目录: {test_dir}")
    
    # 查找压缩包
    archive_files = []
    for root, dirs, files in os.walk(test_dir):
        for file in files:
            if file.lower().endswith(('.zip', '.7z')):
                archive_path = os.path.join(root, file)
                archive_files.append(archive_path)
                print(f"找到压缩包: {archive_path}")
                
                # 检查文件大小
                try:
                    size = os.path.getsize(archive_path)
                    print(f"  文件大小: {size / (1024*1024):.2f} MB")
                except:
                    print(f"  无法获取文件大小")
    
    if not archive_files:
        print("未找到任何压缩包")
        return
    
    # 测试解压第一个文件
    test_archive = archive_files[0]
    print(f"\n=== 测试解压: {test_archive} ===")
    
    # 创建测试解压目录
    test_extract_dir = os.path.join(os.path.dirname(test_archive), "test_extract")
    os.makedirs(test_extract_dir, exist_ok=True)
    
    filename = os.path.basename(test_archive)
    name_without_ext = os.path.splitext(filename)[0]
    extract_path = os.path.join(test_extract_dir, name_without_ext)
    
    try:
        if test_archive.lower().endswith('.zip'):
            print("使用 zipfile 解压...")
            with zipfile.ZipFile(test_archive, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                print(f"压缩包包含 {len(file_list)} 个文件")
                if len(file_list) > 0:
                    print("前5个文件:")
                    for f in file_list[:5]:
                        print(f"  {f}")
                
                os.makedirs(extract_path, exist_ok=True)
                zip_ref.extractall(extract_path)
                print(f"解压到: {extract_path}")
                
        elif test_archive.lower().endswith('.7z'):
            print("使用 py7zr 解压...")
            archive = py7zr.SevenZipFile(test_archive, mode='r')
            try:
                file_list = archive.getnames()
                print(f"压缩包包含 {len(file_list)} 个文件")
                if len(file_list) > 0:
                    print("前5个文件:")
                    for f in file_list[:5]:
                        print(f"  {f}")
                
                os.makedirs(extract_path, exist_ok=True)
                archive.extractall(path=extract_path)
                print(f"解压到: {extract_path}")
            finally:
                archive.close()
        
        # 检查解压结果
        if os.path.exists(extract_path):
            extracted_files = list(Path(extract_path).rglob("*"))
            print(f"解压成功！解压出 {len(extracted_files)} 个文件/文件夹")
            
            if len(extracted_files) > 0:
                print("解压出的前5个项目:")
                for f in extracted_files[:5]:
                    if f.is_file():
                        print(f"  文件: {f.relative_to(extract_path)}")
                    else:
                        print(f"  目录: {f.relative_to(extract_path)}")
        else:
            print("错误: 解压目录不存在")
            
    except Exception as e:
        print(f"解压失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_extraction()