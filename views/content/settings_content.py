import customtkinter as ctk

class SettingsContent(ctk.CTkFrame):
    """设置页面内容类"""
    
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=10)
        self.controller = controller
        self.app_state = controller.app_state
        
        # 创建界面组件
        self.create_widgets()
        
    def create_widgets(self):
        """创建设置页面的界面组件"""
        # 页面标题
        title_frame = ctk.CTkFrame(self, height=60, corner_radius=10)
        title_frame.pack(fill="x", padx=10, pady=(10, 0))
        title_frame.pack_propagate(False)
        
        title_label = ctk.CTkLabel(title_frame, text="应用设置",
                                 font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(side="left", padx=20, pady=15)
        
        # 内容区域
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 主题设置区域
        theme_frame = ctk.CTkFrame(content_frame, corner_radius=10)
        theme_frame.pack(fill="x", pady=(0, 20), ipady=10)
        
        # 主题设置标题
        theme_title = ctk.CTkLabel(theme_frame, text="界面主题",
                                  font=ctk.CTkFont(size=16, weight="bold"))
        theme_title.pack(anchor="w", padx=20, pady=(15, 10))
        
        # 主题选择
        theme_option_frame = ctk.CTkFrame(theme_frame, fg_color="transparent")
        theme_option_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        theme_label = ctk.CTkLabel(theme_option_frame, text="主题风格:", width=100)
        theme_label.pack(side="left", padx=(0, 10), pady=5)
        
        current_theme = self.app_state.theme
        self.theme_var = ctk.StringVar(value=current_theme)
        
        self.theme_optionmenu = ctk.CTkOptionMenu(
            theme_option_frame,
            variable=self.theme_var,
            values=["Dark", "Light"],
            command=self.on_theme_change,
            width=150
        )
        self.theme_optionmenu.pack(side="left", fill="x", expand=False, pady=5)
        
        # 使用延迟自动关闭下拉菜单，同时保留悬浮动画
        self.theme_optionmenu.bind("<<ComboboxSelected>>", self._start_close_timer)
        self.close_timer = None
        
        # 提示信息
        hint_label = ctk.CTkLabel(
            content_frame,
            text="💡 提示: 其他设置选项将在后续版本中添加",
            font=ctk.CTkFont(size=12),
            text_color=(("gray60", "gray40"))
        )
        hint_label.pack(anchor="w", padx=20, pady=(20, 0))
        
    def on_theme_change(self, theme):
        """处理主题变更"""
        self.app_state.set_theme(theme)
        ctk.set_appearance_mode(theme)
        
    def _start_close_timer(self, event=None):
        """开始下拉菜单自动关闭计时器"""
        # 取消之前的计时器
        if self.close_timer is not None:
            self.after_cancel(self.close_timer)
        
        # 2秒后自动关闭下拉菜单
        self.close_timer = self.after(2000, self._auto_close_dropdown)
        
        # 监听下拉菜单的离开事件
        if hasattr(self.theme_optionmenu, '_dropdown_menu') and self.theme_optionmenu._dropdown_menu is not None:
            self.theme_optionmenu._dropdown_menu.bind("<Leave>", lambda e: self.after(500, self._auto_close_dropdown))
            
    def _auto_close_dropdown(self):
        """自动关闭下拉菜单的方法"""
        if hasattr(self.theme_optionmenu, '_dropdown_menu') and self.theme_optionmenu._dropdown_menu is not None:
            self.theme_optionmenu._dropdown_menu.place_forget()
            self.close_timer = None
        
    def refresh_content(self):
        """刷新页面内容"""
        # 更新主题选择器的值以匹配当前状态
        self.theme_var.set(self.app_state.theme)