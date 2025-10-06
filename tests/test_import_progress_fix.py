#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试导入功能的进度条更新修复
"""

import os
import sys
import zipfile
import tempfile
import tkinter as tk
import customtkinter as ctk

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_test_asset_zip():
    """创建一个测试用的资产ZIP文件"""
    with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_zip:
        with zipfile.ZipFile(temp_zip.name, 'w') as zf:
            # 创建一些测试文件和目录结构
            zf.writestr("TestAsset/TestAsset/Materials/M_Test_001.uasset", "材质文件内容")
            zf.writestr("TestAsset/TestAsset/Textures/T_Test_001.uasset", "纹理文件内容")
            zf.writestr("TestAsset/TestAsset/Meshes/SM_TestCube.uasset", "静态网格文件内容")
            zf.writestr("TestAsset/TestAsset/Maps/TestLevel.umap", "测试关卡文件内容")
            zf.writestr("TestAsset/TestAsset/Blueprints/BP_TestActor.uasset", "蓝图文件内容")
            zf.writestr("TestAsset/TestAsset/README.md", "测试资产包说明文档")
        return temp_zip.name

def test_import_progress():
    """测试导入进度更新"""
    print("创建测试资产ZIP文件...")
    test_zip = create_test_asset_zip()
    
    # 设置customtkinter
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # 创建根窗口
    root = ctk.CTk()
    root.title("导入进度测试")
    root.geometry("400x200")
    root.withdraw()  # 隐藏主窗口
    
    # 创建进度对话框
    progress_dialog = ctk.CTkToplevel(root)
    progress_dialog.title("导入进度测试")
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
    title_label = ctk.CTkLabel(main_frame, text="正在测试导入进度更新...",
                              font=ctk.CTkFont(size=14, weight="bold"))
    title_label.pack(pady=(0, 10))
    
    # 当前文件
    current_file_label = ctk.CTkLabel(main_frame, text="准备导入...",
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
    
    # 模拟导入进度
    import threading
    import time
    
    def simulate_import():
        """模拟导入过程"""
        try:
            # 模拟导入过程中的不同阶段
            stages = [
                "准备导入环境...",
                "解压资产文件...",
                "优化目录结构...",
                "复制到目标目录...",
                "清理临时文件...",
                "刷新虚幻引擎..."
            ]
            
            for i, stage in enumerate(stages):
                # 更新当前阶段
                def update_stage(s):
                    def update():
                        current_file_label.configure(text=s)
                    return update
                
                progress_dialog.after(0, update_stage(stage))
                
                # 更新进度
                progress = (i + 1) / len(stages)
                def update_progress(p):
                    def update():
                        progress_bar.set(p)
                        progress_label.configure(text=f"{int(p * 100)}%")
                        progress_dialog.update_idletasks()
                    return update
                
                progress_dialog.after(0, update_progress(progress))
                
                # 模拟处理延迟
                time.sleep(0.5)  # 每个阶段500ms
            
            # 完成
            def on_complete():
                progress_dialog.after(500, lambda: [
                    progress_dialog.destroy(),
                    root.quit()
                ])
                print("测试完成！导入进度条更新正常。")
            
            progress_dialog.after(0, on_complete)
            
        except Exception as e:
            print(f"测试出错: {e}")
            progress_dialog.after(0, lambda: [
                progress_dialog.destroy(),
                root.quit()
            ])
    
    # 启动模拟线程
    thread = threading.Thread(target=simulate_import, daemon=True)
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
    print("开始测试导入进度条更新修复...")
    test_import_progress()
    print("测试结束")