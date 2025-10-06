import customtkinter as ctk


class Toolbar(ctk.CTkFrame):
    def __init__(self, parent, controller, app_state):
        super().__init__(parent, width=220, corner_radius=15)  # 增加宽度和圆角
        self.controller = controller
        self.app_state = app_state
        self.grid_propagate(False)
        self.buttons = {}  # 存储按钮引用
        self.current_tool = None  # 当前选中的工具
        self.create_widgets()
        # 默认选中虚幻资产库
        self.set_active_tool("ue_asset_library")
        
    
    def create_widgets(self):
        """创建工具栏组件 - 现代化设计"""
        # 工具栏标题（现代化设计）
        self.title_label = ctk.CTkLabel(self, text="🚀 工具栏", 
                                      font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=(20, 25))
        
        # 工具列表（现代化设计）
        tools_frame = ctk.CTkFrame(self, fg_color="transparent")
        tools_frame.pack(fill="both", expand=True, padx=15)
        
        # 定义工具（调整顺序：虚幻资产库在上方，虚幻工程在下方）
        tools = [
            ("📚 虚幻资产库", "ue_asset_library"),
            ("🎮 虚幻工程", "ue_projects"),
        ]
        
        for tool_name, tool_id in tools:
            btn = ctk.CTkButton(tools_frame, text=tool_name,
                               command=lambda tid=tool_id: self.on_tool_click(tid),
                               height=45,  # 增加按钮高度
                               font=ctk.CTkFont(size=14, weight="bold"),  # 增加字体大小和加粗
                               anchor="w",
                               fg_color=("#e5e7eb", "#374151"),  # 现代化颜色
                               hover_color=("#d1d5db", "#4b5563"),  # 现代化悬停颜色
                               text_color=("#1f2937", "#f9fafb"),
                               corner_radius=8)  # 增加圆角
            btn.pack(fill="x", pady=8)  # 增加间距
            self.buttons[tool_id] = btn
        

        
        # 设置和关于按钮（现代化设计）
        bottom_buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_buttons_frame.pack(fill="x", padx=15, pady=15)
        
        # 设置按钮（现代化设计）
        self.settings_btn = ctk.CTkButton(bottom_buttons_frame, text="⚙️ 设置",
                                       command=lambda: self.on_tool_click("settings"),
                                       height=45,  # 增加按钮高度
                                       font=ctk.CTkFont(size=14, weight="bold"),  # 增加字体大小和加粗
                                       anchor="w",
                                       fg_color=("#8b5cf6", "#a78bfa"),  # 紫色主题
                                       hover_color=("#7c3aed", "#8b5cf6"),  # 紫色悬停
                                       text_color=("#f9fafb", "#f9fafb"),
                                       corner_radius=8)  # 增加圆角
        self.settings_btn.pack(fill="x", pady=8)
        self.buttons["settings"] = self.settings_btn
        
        # 关于按钮（现代化设计）
        self.about_btn = ctk.CTkButton(bottom_buttons_frame, text="ℹ️ 关于",
                                     command=lambda: self.on_tool_click("about"),
                                     height=45,  # 增加按钮高度
                                     font=ctk.CTkFont(size=14, weight="bold"),  # 增加字体大小和加粗
                                     anchor="w",
                                     fg_color=("#10b981", "#34d399"),  # 绿色主题
                                     hover_color=("#059669", "#10b981"),  # 绿色悬停
                                     text_color=("#f9fafb", "#f9fafb"),
                                     corner_radius=8)  # 增加圆角
        self.about_btn.pack(fill="x", pady=8)
        self.buttons["about"] = self.about_btn
        
        # 底部信息（现代化设计）
        info_frame = ctk.CTkFrame(self, height=70, corner_radius=10)
        info_frame.pack(fill="x", padx=15, pady=15)
        info_frame.pack_propagate(False)
        
        self.info_label = ctk.CTkLabel(info_frame, text="版本 1.0", 
                                     font=ctk.CTkFont(size=13, weight="bold"),
                                     text_color=("gray70", "gray70"))
        self.info_label.pack(expand=True)
    
    def on_tool_click(self, tool_id):
        """处理工具按钮点击 - 即时切换"""
        # 如果点击的是当前已选中的工具，忽略
        if self.current_tool == tool_id:
            print(f"ℹ️ Currently selected: {tool_id}")
            return
        
        print(f"👆 用户点击工具: {tool_id}")
        
        # 添加按钮点击反馈动画
        self._animate_button_click(tool_id)
        
        # 设置活动工具
        self.set_active_tool(tool_id)
        
        # 通知控制器切换工具
        self.controller.set_current_tool(tool_id)
    

    
    def _animate_button_click(self, tool_id):
        """按钮点击反馈动画"""
        if tool_id in self.buttons:
            btn = self.buttons[tool_id]
            
            # 短暂的点击效果
            original_color = btn.cget("fg_color")
            
            # 点击时的颜色（更深的蓝色）
            btn.configure(fg_color=("#0d2d52", "#0a1f3a"))
            
            # 100ms后恢复正常颜色
            self.after(100, lambda: btn.configure(fg_color=original_color))
    
    def set_active_tool(self, tool_id):
        """设置活动工具按钮 - 带平滑过渡动画"""
        print(f"🎨 切换工具按钮状态: {tool_id}")
        
        # 重置所有按钮为默认状态
        for btn_id, btn in self.buttons.items():
            if btn_id == tool_id:
                # 设置为选中状态（蓝色）
                self._animate_to_active_state(btn)
            else:
                # 设置为未选中状态（灰色）
                self._animate_to_inactive_state(btn)
        
        self.current_tool = tool_id
    

    
    def _animate_to_active_state(self, button):
        """动画切换到活动状态 - 现代化设计"""
        # 蓝色高亮状态
        button.configure(
            fg_color=("#3b82f6", "#60a5fa"),  # 更鲜明的蓝色用于亮色主题
            hover_color=("#2563eb", "#3b82f6"),
            border_width=2,
            border_color=("#1d4ed8", "#2563eb"),
            text_color=("#ffffff", "#ffffff"),
            font=ctk.CTkFont(size=14, weight="bold")  # 加粗字体
        )
    
    def _animate_to_inactive_state(self, button):
        """动画切换到非活动状态 - 现代化设计"""
        # 灰色默认状态
        button.configure(
            fg_color=("#e5e7eb", "#374151"),
            hover_color=("#d1d5db", "#4b5563"),
            border_width=1,
            border_color=("#d1d5db", "#4b5563"),
            text_color=("#1f2937", "#f9fafb"),
            font=ctk.CTkFont(size=14, weight="bold")  # 加粗字体
        )