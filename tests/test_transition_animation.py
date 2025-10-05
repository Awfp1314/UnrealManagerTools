#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
界面切换动画测试脚本
用于测试和展示不同的动画效果
"""

import customtkinter as ctk
import time

class AnimationTestWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("界面切换动画测试")
        self.geometry("800x600")
        
        # 动画参数
        self.transition_duration = 200
        self.transition_steps = 10
        self.is_transitioning = False
        
        self.create_widgets()
    
    def create_widgets(self):
        """创建测试界面"""
        # 标题
        title_label = ctk.CTkLabel(self, text="界面切换动画测试", 
                                  font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=20)
        
        # 控制面板
        control_frame = ctk.CTkFrame(self)
        control_frame.pack(pady=10, padx=20, fill="x")
        
        # 速度控制
        speed_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        speed_frame.pack(side="left", padx=10, pady=10)
        
        ctk.CTkLabel(speed_frame, text="动画速度:").pack(side="left", padx=5)
        
        speed_buttons = [
            ("快速", "fast"),
            ("正常", "normal"), 
            ("慢速", "slow")
        ]
        
        for text, speed in speed_buttons:
            btn = ctk.CTkButton(speed_frame, text=text, width=60,
                               command=lambda s=speed: self.set_speed(s))
            btn.pack(side="left", padx=2)
        
        # 切换按钮
        switch_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        switch_frame.pack(side="right", padx=10, pady=10)
        
        ctk.CTkButton(switch_frame, text="切换到页面A", 
                     command=lambda: self.switch_to_page("A")).pack(side="left", padx=5)
        ctk.CTkButton(switch_frame, text="切换到页面B", 
                     command=lambda: self.switch_to_page("B")).pack(side="left", padx=5)
        
        # 内容区域
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 创建两个测试页面
        self.page_a = self.create_page_a()
        self.page_b = self.create_page_b()
        
        # 当前显示的页面
        self.current_page = None
        self.switch_to_page("A")  # 默认显示页面A
    
    def create_page_a(self):
        """创建测试页面A"""
        page = ctk.CTkFrame(self.content_frame, fg_color=("#e8f4fd", "#2d3748"))
        
        ctk.CTkLabel(page, text="📄 页面 A", 
                    font=ctk.CTkFont(size=24, weight="bold")).pack(pady=50)
        
        ctk.CTkLabel(page, text="这是第一个测试页面\n包含一些示例内容", 
                    font=ctk.CTkFont(size=14)).pack(pady=20)
        
        # 添加一些装饰性内容
        for i in range(3):
            item_frame = ctk.CTkFrame(page)
            item_frame.pack(fill="x", padx=50, pady=5)
            ctk.CTkLabel(item_frame, text=f"测试项目 {i+1}").pack(pady=10)
        
        return page
    
    def create_page_b(self):
        """创建测试页面B"""
        page = ctk.CTkFrame(self.content_frame, fg_color=("#f0fff0", "#2d4a32"))
        
        ctk.CTkLabel(page, text="📊 页面 B", 
                    font=ctk.CTkFont(size=24, weight="bold")).pack(pady=50)
        
        ctk.CTkLabel(page, text="这是第二个测试页面\n具有不同的样式和内容", 
                    font=ctk.CTkFont(size=14)).pack(pady=20)
        
        # 添加一些不同的内容
        progress_frame = ctk.CTkFrame(page)
        progress_frame.pack(fill="x", padx=50, pady=20)
        
        ctk.CTkLabel(progress_frame, text="进度条示例:").pack(pady=5)
        progress_bar = ctk.CTkProgressBar(progress_frame, width=300)
        progress_bar.pack(pady=10)
        progress_bar.set(0.7)
        
        return page
    
    def set_speed(self, speed):
        """设置动画速度"""
        speed_settings = {
            "fast": {"duration": 100, "steps": 6},
            "normal": {"duration": 200, "steps": 10},
            "slow": {"duration": 300, "steps": 15}
        }
        
        if speed in speed_settings:
            settings = speed_settings[speed]
            self.transition_duration = settings["duration"]
            self.transition_steps = settings["steps"]
            print(f"🎨 动画速度设置为: {speed} ({self.transition_duration}ms, {self.transition_steps}步)")
    
    def switch_to_page(self, page_name):
        """切换页面"""
        if self.is_transitioning:
            print("⚠️ 正在切换中，忽略请求")
            return
        
        new_page = self.page_a if page_name == "A" else self.page_b
        
        if self.current_page == new_page:
            print(f"ℹ️ 当前已在页面 {page_name}")
            return
        
        print(f"🎬 开始切换到页面 {page_name}")
        
        if self.current_page:
            self.start_transition(self.current_page, new_page, page_name)
        else:
            self.show_page_directly(new_page, page_name)
    
    def start_transition(self, old_page, new_page, page_name):
        """开始切换动画"""
        self.is_transitioning = True
        
        # 淡出旧页面
        self.fade_out_page(old_page, lambda: self.fade_in_page(new_page, page_name))
    
    def fade_out_page(self, page, callback):
        """淡出页面"""
        self.animate_alpha(page, 1.0, 0.0, callback)
    
    def fade_in_page(self, page, page_name):
        """淡入页面"""
        # 切换页面
        if self.current_page:
            self.current_page.pack_forget()
        
        self.current_page = page
        self.current_page.pack(fill="both", expand=True)
        
        # 淡入新页面
        self.animate_alpha(page, 0.0, 1.0, lambda: self.finish_transition(page_name))
    
    def animate_alpha(self, page, start_alpha, end_alpha, callback):
        """透明度动画"""
        step_size = (end_alpha - start_alpha) / self.transition_steps
        current_alpha = start_alpha
        
        def animate_step(step=0):
            nonlocal current_alpha
            
            if step < self.transition_steps:
                current_alpha += step_size
                alpha = max(0.0, min(1.0, current_alpha))
                
                # 应用透明度效果
                self.apply_alpha_effect(page, alpha)
                
                # 继续动画
                delay = self.transition_duration // (self.transition_steps * 2)
                self.after(delay, lambda: animate_step(step + 1))
            else:
                # 动画完成
                self.apply_alpha_effect(page, end_alpha)
                if callback:
                    callback()
        
        animate_step()
    
    def apply_alpha_effect(self, page, alpha):
        """应用透明度效果"""
        try:
            if alpha <= 0.1:
                page.configure(fg_color="transparent")
            elif alpha >= 0.9:
                # 恢复原始颜色
                if page == self.page_a:
                    page.configure(fg_color=("#e8f4fd", "#2d3748"))
                else:
                    page.configure(fg_color=("#f0fff0", "#2d4a32"))
            else:
                # 中间状态
                if page == self.page_a:
                    light_base, dark_base = 180, 45
                else:
                    light_base, dark_base = 190, 50
                
                light_intensity = int(light_base + (255 - light_base) * alpha)
                dark_intensity = int(dark_base * alpha)
                
                light_intensity = max(0, min(255, light_intensity))
                dark_intensity = max(0, min(255, dark_intensity))
                
                light_color = f"#{light_intensity:02x}{light_intensity:02x}{light_intensity:02x}"
                dark_color = f"#{dark_intensity:02x}{dark_intensity:02x}{dark_intensity:02x}"
                
                page.configure(fg_color=(light_color, dark_color))
        except Exception as e:
            print(f"应用透明度效果出错: {e}")
    
    def show_page_directly(self, page, page_name):
        """直接显示页面（无动画）"""
        self.current_page = page
        self.current_page.pack(fill="both", expand=True)
        self.finish_transition(page_name)
    
    def finish_transition(self, page_name):
        """完成切换"""
        self.is_transitioning = False
        print(f"✨ 切换到页面 {page_name} 完成")

def main():
    """主函数"""
    print("🚀 启动界面切换动画测试")
    
    # 设置外观
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
    
    # 创建并运行应用
    app = AnimationTestWindow()
    
    print("📖 使用说明：")
    print("1. 点击'切换到页面A'或'切换到页面B'测试切换动画")
    print("2. 使用'快速'、'正常'、'慢速'按钮调整动画速度")
    print("3. 尝试快速点击按钮，测试冲突防护机制")
    
    app.mainloop()
    print("👋 测试完成")

if __name__ == "__main__":
    main()