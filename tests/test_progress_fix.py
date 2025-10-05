#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试解压功能的进度条更新
"""

import os
import sys
import zipfile
import tempfile
import tkinter as tk
import customtkinter as ctk

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_test_zip():
    """创建一个测试用的ZIP文件"""
    with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_zip:
        with zipfile.ZipFile(temp_zip.name, 'w') as zf:
            # 创建一些测试文件
            for i in range(20):
                filename = f"test_file_{i:02d}.txt"
                content = f"这是测试文件 {i}\n" * 100  # 每个文件约200字节
                zf.writestr(filename, content)
        return temp_zip.name

def test_progress_update():
    """测试进度条更新"""
    print("创建测试ZIP文件...")
    test_zip = create_test_zip()
    
    # 设置customtkinter
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # 创建根窗口
    root = ctk.CTk()
    root.title("进度条测试")
    root.geometry("400x200")
    root.withdraw()  # 隐藏主窗口
    
    # 创建进度对话框
    progress_dialog = ctk.CTkToplevel(root)
    progress_dialog.title("解压进度测试")
    progress_dialog.geometry("400x150")
    progress_dialog.resizable(False, False)
    progress_dialog.transient(root)
    progress_dialog.grab_set()
    
    # 居中显示
    progress_dialog.update_idletasks()
    x = (progress_dialog.winfo_screenwidth() // 2) - (400 // 2)
    y = (progress_dialog.winfo_screenheight() // 2) - (150 // 2)
    progress_dialog.geometry(f"400x150+{x}+{y}")
    
    # 主框架
    main_frame = ctk.CTkFrame(progress_dialog, fg_color="transparent")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # 标题
    title_label = ctk.CTkLabel(main_frame, text="正在测试进度条更新...",
                              font=ctk.CTkFont(size=14, weight="bold"))
    title_label.pack(pady=(0, 10))
    
    # 当前文件
    current_file_label = ctk.CTkLabel(main_frame, text="正在解压: test.zip",
                                     font=ctk.CTkFont(size=12))
    current_file_label.pack(pady=(0, 10))
    
    # 进度条框架
    progress_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    progress_frame.pack(fill="x", pady=(0, 10))
    
    # 进度条
    progress_bar = ctk.CTkProgressBar(progress_frame, width=300)
    progress_bar.pack(side="left", fill="x", expand=True)
    progress_bar.set(0)
    
    # 百分比标签
    progress_label = ctk.CTkLabel(progress_frame, text="0%",
                                 font=ctk.CTkFont(size=12, weight="bold"),
                                 width=50)
    progress_label.pack(side="right", padx=(10, 0))
    
    # 取消按钮
    def on_cancel():
        progress_dialog.destroy()
        root.quit()
    
    cancel_button = ctk.CTkButton(main_frame, text="取消", width=100,
                                 command=on_cancel)
    cancel_button.pack()
    
    # 模拟解压进度
    import threading
    import time
    
    def simulate_extraction():
        """模拟解压过程"""
        try:
            with zipfile.ZipFile(test_zip, 'r') as zf:
                file_list = zf.namelist()
                total_files = len(file_list)
                
                for i, filename in enumerate(file_list):
                    # 更新当前文件名
                    def update_current_file(f):
                        def update():
                            current_file_label.configure(text=f"正在解压: {f}")
                        return update
                    
                    progress_dialog.after(0, update_current_file(filename))
                    
                    # 更新进度
                    progress = (i + 1) / total_files
                    def update_progress(p):
                        def update():
                            progress_bar.set(p)
                            progress_label.configure(text=f"{int(p * 100)}%")
                            progress_dialog.update_idletasks()
                        return update
                    
                    progress_dialog.after(0, update_progress(progress))
                    
                    # 模拟解压延迟
                    time.sleep(0.2)  # 每个文件200ms
                
                # 完成
                def on_complete():
                    progress_dialog.after(500, lambda: [
                        progress_dialog.destroy(),
                        root.quit()
                    ])
                    print("测试完成！进度条更新正常。")
                
                progress_dialog.after(0, on_complete)
                
        except Exception as e:
            print(f"测试出错: {e}")
            progress_dialog.after(0, lambda: [
                progress_dialog.destroy(),
                root.quit()
            ])
    
    # 启动模拟线程
    thread = threading.Thread(target=simulate_extraction, daemon=True)
    thread.start()
    
    # 运行GUI
    root.mainloop()
    
    # 清理
    try:
        os.unlink(test_zip)
        print("清理测试文件完成")
    except:
        pass

if __name__ == "__main__":
    print("开始测试进度条更新功能...")
    test_progress_update()
    print("测试结束")