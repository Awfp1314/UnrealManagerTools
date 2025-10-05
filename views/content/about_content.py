import customtkinter as ctk

class AboutContent(ctk.CTkFrame):
    """关于页面内容类"""
    
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=10)
        self.controller = controller
        
        # 创建界面组件
        self.create_widgets()
        
    def create_widgets(self):
        """创建关于页面的界面组件"""
        # 页面标题
        title_frame = ctk.CTkFrame(self, height=60, corner_radius=10)
        title_frame.pack(fill="x", padx=10, pady=(10, 0))
        title_frame.pack_propagate(False)
        
        title_label = ctk.CTkLabel(title_frame, text="关于",
                                 font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(side="left", padx=20, pady=15)
        
        # 内容区域
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 关于信息卡片
        about_frame = ctk.CTkFrame(content_frame, corner_radius=10)
        about_frame.pack(fill="both", expand=True, pady=20, padx=40)
        
        # 程序图标
        icon_label = ctk.CTkLabel(about_frame, 
                                text="🚀", 
                                font=ctk.CTkFont(size=48))
        icon_label.pack(pady=(40, 20))
        
        # 程序名称
        app_name_label = ctk.CTkLabel(about_frame, 
                                    text="虚幻引擎资产管理器", 
                                    font=ctk.CTkFont(size=20, weight="bold"))
        app_name_label.pack(pady=(0, 10))
        
        # 版本信息
        version_label = ctk.CTkLabel(about_frame, 
                                   text="版本 1.0", 
                                   font=ctk.CTkFont(size=14))
        version_label.pack(pady=(0, 20))
        
        # 作者信息
        author_label = ctk.CTkLabel(about_frame, 
                                  text="作者：HUTAO", 
                                  font=ctk.CTkFont(size=14, weight="bold"))
        author_label.pack(pady=(0, 10))
        
        # 版权信息
        copyright_label = ctk.CTkLabel(about_frame, 
                                     text="© 2025 版权所有", 
                                     font=ctk.CTkFont(size=12),
                                     text_color=("gray60", "gray40"))
        copyright_label.pack(pady=(20, 40))
        
    def refresh_content(self):
        """刷新页面内容"""
        # 关于页面通常不需要刷新
        pass