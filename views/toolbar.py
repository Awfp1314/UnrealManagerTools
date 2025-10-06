import customtkinter as ctk


class Toolbar(ctk.CTkFrame):
    def __init__(self, parent, controller, app_state):
        super().__init__(parent, width=200, corner_radius=10)
        self.controller = controller
        self.app_state = app_state
        self.grid_propagate(False)
        self.buttons = {}  # 存储按钮引用
        self.current_tool = None  # 当前选中的工具
        self.create_widgets()
        # 默认选中虚幻资产库
        self.set_active_tool("ue_asset_library")
        
    

    def create_widgets(self):
        """创建工具栏组件"""
        # 工具栏标题
        self.title_label = ctk.CTkLabel(self, text="工具栏", 
                                      font=ctk.CTkFont(size=16, weight="bold"))
        self.title_label.pack(pady=(15, 20))
        
        # 工具列表
        tools_frame = ctk.CTkFrame(self, fg_color="transparent")
        tools_frame.pack(fill="both", expand=True, padx=10)
        
        # 定义工具
        tools = [
            ("虚幻资产库", "ue_asset_library"),
            ("虚幻工程", "ue_projects"),
        ]
        
        for tool_name, tool_id in tools:
            # 使用默认参数修复lambda闭包问题
            btn = ctk.CTkButton(tools_frame, text=tool_name,
                               command=lambda tid=tool_id: self.on_tool_click(tid),
                               height=45,
                               font=ctk.CTkFont(size=14, weight="bold"),
                               anchor="w",
                               fg_color="transparent",
                               hover_color=("#e0e0e0", "#3d3d3d"),
                               text_color=("#333333", "#ffffff"),
                               border_width=2,
                               border_color=("#e0e0e0", "#444444"),
                               corner_radius=8)
            btn.pack(fill="x", pady=5)
            self.buttons[tool_id] = btn
        

        
        # 设置和关于按钮
        bottom_buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_buttons_frame.pack(fill="x", padx=10, pady=10)
        
        # 设置按钮
        self.settings_btn = ctk.CTkButton(bottom_buttons_frame, text="设置",
                                       command=lambda s=self: s.on_tool_click("settings"),
                                       height=45,
                                       font=ctk.CTkFont(size=14, weight="bold"),
                                       anchor="w",
                                       fg_color="transparent",
                                       hover_color=("#e0e0e0", "#3d3d3d"),
                                       text_color=("#333333", "#ffffff"),
                                       border_width=2,
                                       border_color=("#e0e0e0", "#444444"),
                                       corner_radius=8)
        self.settings_btn.pack(fill="x", pady=5)
        self.buttons["settings"] = self.settings_btn
        
        # 关于按钮
        self.about_btn = ctk.CTkButton(bottom_buttons_frame, text="关于",
                                     command=lambda s=self: s.on_tool_click("about"),
                                     height=45,
                                     font=ctk.CTkFont(size=14, weight="bold"),
                                     anchor="w",
                                     fg_color="transparent",
                                     hover_color=("#e0e0e0", "#3d3d3d"),
                                     text_color=("#333333", "#ffffff"),
                                     border_width=2,
                                     border_color=("#e0e0e0", "#444444"),
                                     corner_radius=8)
        self.about_btn.pack(fill="x", pady=5)
        self.buttons["about"] = self.about_btn
        
        # 底部信息
        info_frame = ctk.CTkFrame(self, height=60, corner_radius=8)
        info_frame.pack(fill="x", padx=10, pady=10)
        info_frame.pack_propagate(False)
        
        self.info_label = ctk.CTkLabel(info_frame, text="版本 1.0", 
                                     font=ctk.CTkFont(size=12),
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
        """动画切换到活动状态"""
        # 蓝色高亮状态
        button.configure(
            fg_color=("#2196F3", "#14375e"),  # 更鲜明的蓝色用于亮色主题
            hover_color=("#1976D2", "#1e5a8a"),
            border_width=2,
            border_color=("#1976D2", "#4299e1"),
            text_color=("#ffffff", "#ffffff")
        )
    
    def _animate_to_inactive_state(self, button):
        """动画切换到非活动状态"""
        # 灰色默认状态
        button.configure(
            fg_color=("#d0d0d0", "#2d2d2d"),
            hover_color=("#b0b0b0", "#3d3d3d"),
            border_width=1,
            border_color=("#b0b0b0", "#505050"),
            text_color=("#333333", "#ffffff")
        )