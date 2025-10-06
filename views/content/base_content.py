import customtkinter as ctk
import customtkinter as ctk
from views.content.ue_asset_library import UEAssetLibraryContent
from views.content.ue_projects import UEProjectsContent
from views.content.settings_content import SettingsContent
from views.content.about_content import AboutContent

class ContentManager(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=10)
        self.controller = controller
        self.current_page = None
        self.pages = {}  # 存储独立页面
        self.loaded_pages = set()  # 跟踪已加载的页面
        self.loading_frame = None  # 加载界面
        self.app_state = controller.app_state if hasattr(controller, 'app_state') else None  # 获取app_state
        
        # 配置网格布局，让页面占满整个容器
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # 显示加载界面
        self.show_loading_screen()
        
        # 预创建所有独立页面并预加载数据
        self.after(100, self.create_all_pages)  # 稍微延迟，让加载界面先显示

    def show_loading_screen(self):
        """显示加载界面，提供更好的启动体验"""
        print("💾 显示加载界面...")
        
        # 创建加载界面
        self.loading_frame = ctk.CTkFrame(self, fg_color=("gray95", "gray15"), corner_radius=10)
        self.loading_frame.grid(row=0, column=0, sticky="nsew")
        
        # 配置加载界面布局
        self.loading_frame.grid_rowconfigure(0, weight=1)
        self.loading_frame.grid_rowconfigure(1, weight=0)
        self.loading_frame.grid_rowconfigure(2, weight=1)
        self.loading_frame.grid_columnconfigure(0, weight=1)
        
        # 主内容区域
        content_frame = ctk.CTkFrame(self.loading_frame, fg_color="transparent")
        content_frame.grid(row=1, column=0, padx=40, pady=40)
        
        # 加载图标（使用文字代替）
        icon_label = ctk.CTkLabel(content_frame, 
                                 text="🚀", 
                                 font=ctk.CTkFont(size=48))
        icon_label.pack(pady=(0, 20))
        
        # 加载标题
        title_label = ctk.CTkLabel(content_frame, 
                                  text="虚幻引擎资产管理器", 
                                  font=ctk.CTkFont(size=24, weight="bold"),
                                  text_color=(("gray20", "gray90")))
        title_label.pack(pady=(0, 10))
        
        # 加载提示
        self.loading_label = ctk.CTkLabel(content_frame, 
                                         text="正在初始化界面...", 
                                         font=ctk.CTkFont(size=14),
                                         text_color=(("gray50", "gray60")))
        self.loading_label.pack(pady=(0, 20))
        
        # 进度条
        self.progress_bar = ctk.CTkProgressBar(content_frame, width=300, height=8)
        self.progress_bar.pack(pady=(0, 10))
        self.progress_bar.set(0.1)  # 初始进度
    
    def update_loading_progress(self, progress, message):
        """更新加载进度"""
        if self.loading_label and self.progress_bar:
            try:
                self.loading_label.configure(text=message)
                self.progress_bar.set(progress)
                self.update_idletasks()  # 强制更新界面
            except:
                pass
                
    def hide_loading_screen(self):
        """隐藏加载界面"""
        if self.loading_frame:
            self.loading_frame.grid_remove()
            self.loading_frame = None
            print("✨ 加载界面已隐藏")

    def create_all_pages(self):
        """创建所有独立页面并预加载数据"""
        print("🚀 创建独立页面...")
        message = "正在创建界面组件..."
        self.update_loading_progress(0.2, message)
        
        # 创建虚幻工程页面
        self.pages["ue_projects"] = UEProjectsContent(self, self.controller)
        message = "工程管理界面创建完成..."
        self.update_loading_progress(0.4, message)
        
        # 创建虚幻资产库页面
        self.pages["ue_asset_library"] = UEAssetLibraryContent(self, self.controller)
        message = "资产库界面创建完成..."
        self.update_loading_progress(0.6, message)
        
        # 创建设置页面
        self.pages["settings"] = SettingsContent(self, self.controller)
        message = "设置界面创建完成..."
        self.update_loading_progress(0.8, message)
        
        # 创建关于页面
        self.pages["about"] = AboutContent(self, self.controller)
        message = "关于界面创建完成..."
        self.update_loading_progress(0.9, message)
        
        # 关键优化：所有页面都放在同一个grid位置，通过层级控制显示
        for page_name, page in self.pages.items():
            page.grid(row=0, column=0, sticky="nsew")
            # 初始时隐藏所有页面（但保持在grid中）
            page.grid_remove()
        
        print("✅ 所有独立页面创建完成！")
        
        # 预加载所有页面数据，避免首次切换卡顿
        self.after(100, self._preload_all_pages)  # 稍微延迟，让界面先显示

    def _preload_all_pages(self):
        """预加载所有页面数据，防止首次切换卡顿"""
        print("🚀 开始预加载所有页面数据...")
        message = "正在加载数据..."
        self.update_loading_progress(0.7, message)
        
        total_pages = len(self.pages)
        loaded_count = 0
        
        for page_name, page in self.pages.items():
            try:
                # 如果页面有refresh_content方法，预加载数据
                if hasattr(page, 'refresh_content'):
                    print(f"💾 预加载页面: {page_name}")
                    page.refresh_content()
                    self.loaded_pages.add(page_name)  # 标记为已加载
                    loaded_count += 1
                    
                    # 更新进度
                    progress = 0.7 + (loaded_count / total_pages) * 0.2
                    message = f"已加载 {page_name}..."
                    self.update_loading_progress(progress, message)
            except Exception as e:
                print(f"⚠️ 预加载页面 {page_name} 失败: {e}")
        
        print("✨ 所有页面数据预加载完成！")
        
        # 预加载完成，显示默认页面
        message = "初始化完成，正在进入..."
        self.update_loading_progress(0.95, message)
        self.after(500, self._finish_loading)  # 稍微延迟，显示完成状态
    
    def _finish_loading(self):
        """完成加载，显示默认页面"""
        message = "加载完成！"
        self.update_loading_progress(1.0, message)
        self.after(300, lambda: [
            self.hide_loading_screen(),
            self.show_page("ue_asset_library")  # 显示默认页面（虚幻资产库）
        ])

    def show_page(self, page_name):
        """显示指定页面 - 真正的原子切换，无闪烁无绘制痕迹"""
        # 如果是相同页面，无需切换
        if self.current_page == page_name:
            print(f"ℹ️ 当前已在页面: {page_name}")
            return
        
        if page_name in self.pages:
            print(f"⚡ 原子切换到页面: {page_name}")
            
            # 关键优化：使用单一原子操作实现真正的标签页切换
            new_page = self.pages[page_name]
            
            # 步骤1：直接显示新页面（在最上层）
            new_page.grid(row=0, column=0, sticky="nsew")
            new_page.tkraise()  # 立即提升到最高层级
            
            # 步骤2：同时隐藏旧页面（在新页面已经显示后）
            if self.current_page and self.current_page in self.pages:
                old_page = self.pages[self.current_page]
                # 使用lower而不是grid_remove，保持在grid中但在底层
                old_page.lower()
            
            # 更新当前页面记录
            self.current_page = page_name
            
            # 数据状态检查
            if page_name in self.loaded_pages:
                print(f"💾 页面 {page_name} 使用预加载数据，无缝显示")
            else:
                print(f"⚡ 页面 {page_name} 数据未预加载，进行快速刷新...")
                self.after(1, lambda: self._safe_refresh_page(page_name))
                self.loaded_pages.add(page_name)
        else:
            print(f"❌ 页面不存在: {page_name}")



    def _safe_refresh_page(self, page_name):
        """安全刷新页面，避免错误"""
        try:
            if page_name in self.pages:
                page = self.pages[page_name]
                if hasattr(page, 'refresh_content'):
                    page.refresh_content()
        except Exception as e:
            print(f"刷新页面内容出错: {e}")

    def force_refresh_content(self):
        """强制刷新当前页面 - 用于手动刷新按钮"""
        if self.current_page and self.current_page in self.pages:
            page = self.pages[self.current_page]
            if hasattr(page, 'refresh_content'):
                print(f"🔄 强制刷新当前页面: {self.current_page}")
                page.refresh_content()

    def refresh_content(self):
        """刷新当前页面 - 保持向后兼容"""
        # 这个方法保持不变，以保证向后兼容
        self.force_refresh_content()
    
    # 为了向后兼容，保留旧的方法名
    def show_content(self, content_type):
        """兼容旧的show_content方法"""
        self.show_page(content_type)