import customtkinter as ctk
from tkinter import filedialog
import os

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
        
        # 分类路径设置区域
        paths_frame = ctk.CTkFrame(content_frame, corner_radius=10)
        paths_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # 分类路径设置标题
        paths_title = ctk.CTkLabel(paths_frame, text="分类路径配置",
                                  font=ctk.CTkFont(size=16, weight="bold"))
        paths_title.pack(anchor="w", padx=20, pady=(15, 10))
        
        # 分类路径设置说明
        paths_hint = ctk.CTkLabel(paths_frame, 
                                 text="为每个分类配置扫描路径，刷新时将自动发现新资源",
                                 font=ctk.CTkFont(size=12),
                                 text_color=("gray60", "gray40"))
        paths_hint.pack(anchor="w", padx=20, pady=(0, 15))
        
        # 配置路径按钮
        config_btn = ctk.CTkButton(paths_frame,
                                  text="⚙️ 配置分类路径",
                                  font=ctk.CTkFont(size=14, weight="bold"),
                                  height=40,
                                  fg_color=("#2196F3", "#14375e"),
                                  hover_color=("#1976D2", "#1e5a8a"),
                                  text_color=("white", "white"),
                                  command=self.show_category_selection_dialog)
        config_btn.pack(fill="x", padx=20, pady=(0, 20))
        
        # 提示信息
        hint_label = ctk.CTkLabel(
            content_frame,
            text="💡 提示: 其他设置选项将在后续版本中添加",
            font=ctk.CTkFont(size=12),
            text_color=(("gray60", "gray40"))
        )
        hint_label.pack(anchor="w", padx=20, pady=(20, 0))
    
    def show_category_selection_dialog(self):
        """显示分类选择对话框"""
        # 创建对话框
        dialog = ctk.CTkToplevel(self)
        dialog.title("选择分类")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        
        # 居中显示
        self._center_dialog(dialog)
        
        # 创建主框架
        main_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 标题
        title_label = ctk.CTkLabel(main_frame, text="选择要配置路径的分类",
                                  font=ctk.CTkFont(size=16, weight="bold"))
        title_label.pack(pady=(0, 20))
        
        # 分类列表滚动区域
        scrollable_frame = ctk.CTkScrollableFrame(main_frame, height=150)
        scrollable_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # 获取所有非"全部"的分类
        categories = [cat for cat in self.controller.asset_manager.categories if cat != "全部"]
        
        # 创建分类按钮
        for category in categories:
            btn = ctk.CTkButton(scrollable_frame,
                               text=category,
                               font=ctk.CTkFont(size=13),
                               height=35,
                               fg_color="transparent",
                               hover_color=("#e0e0e0", "#3d3d3d"),
                               text_color=("#333333", "#ffffff"),
                               border_width=2,
                               border_color=("#2196F3", "#4299e1"),
                               command=lambda c=category: [dialog.destroy(), self.show_path_config_dialog(c)])
            btn.pack(fill="x", pady=5)
    
    def show_path_config_dialog(self, category):
        """显示路径配置对话框"""
        # 创建对话框
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"配置 {category} 分类路径")
        dialog.geometry("500x400")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        
        # 居中显示
        self._center_dialog(dialog)
        
        # 创建主框架
        main_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 标题
        title_label = ctk.CTkLabel(main_frame, text=f"配置 {category} 分类路径",
                                  font=ctk.CTkFont(size=16, weight="bold"))
        title_label.pack(pady=(0, 20))
        
        # 路径列表滚动区域
        scrollable_frame = ctk.CTkScrollableFrame(main_frame, height=200)
        scrollable_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # 获取该分类的路径列表
        paths = self.controller.asset_manager.get_category_paths(category)
        
        # 创建路径项
        path_frames = []
        for path in paths:
            path_frame = self._create_path_item_dialog(scrollable_frame, category, path, dialog)
            path_frames.append(path_frame)
        
        # 按钮框架
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=10)
        
        # 添加路径按钮
        add_btn = ctk.CTkButton(btn_frame,
                               text="+ 添加路径",
                               font=ctk.CTkFont(size=13, weight="bold"),
                               height=35,
                               fg_color=("#4CAF50", "#2E7D32"),
                               hover_color=("#388E3C", "#1B5E20"),
                               text_color=("white", "white"),
                               command=lambda: self._add_category_path_dialog(category, scrollable_frame, dialog))
        add_btn.pack(side="left", padx=5)
        
        # 关闭按钮
        close_btn = ctk.CTkButton(btn_frame,
                                 text="关闭",
                                 font=ctk.CTkFont(size=13, weight="bold"),
                                 height=35,
                                 fg_color=("#f44336", "#d32f2f"),
                                 hover_color=("#d32f2f", "#b71c1c"),
                                 text_color=("white", "white"),
                                 command=dialog.destroy)
        close_btn.pack(side="right", padx=5)
        
        # 保存引用以便更新
        dialog.path_frames = path_frames
        dialog.scrollable_frame = scrollable_frame
    
    def _create_path_item_dialog(self, parent, category, path, dialog):
        """创建路径项（对话框版本）"""
        path_frame = ctk.CTkFrame(parent, fg_color="transparent")
        path_frame.pack(fill="x", pady=(0, 5))
        
        # 路径显示
        path_label = ctk.CTkLabel(path_frame, 
                                 text=path,
                                 font=ctk.CTkFont(size=12),
                                 anchor="w")
        path_label.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # 删除按钮
        remove_btn = ctk.CTkButton(path_frame,
                                  text="删除",
                                  width=60,
                                  height=28,
                                  font=ctk.CTkFont(size=12),
                                  fg_color=("#f44336", "#d32f2f"),
                                  hover_color=("#d32f2f", "#b71c1c"),
                                  text_color=("white", "white"),
                                  command=lambda: self._remove_category_path_dialog(category, path, dialog))
        remove_btn.pack(side="right")
        
        return path_frame
    
    def _add_category_path_dialog(self, category, scrollable_frame, dialog):
        """为分类添加路径（对话框版本）"""
        # 打开文件夹选择对话框
        path = filedialog.askdirectory(title=f"选择{category}分类的扫描路径")
        if path:
            # 检查该路径是否已在其他分类中配置
            all_categories = [cat for cat in self.controller.asset_manager.categories if cat != "全部"]
            path_already_exists = False
            existing_category = ""
            
            for cat in all_categories:
                cat_paths = self.controller.asset_manager.get_category_paths(cat)
                if path in cat_paths and cat != category:
                    path_already_exists = True
                    existing_category = cat
                    break
            
            if path_already_exists:
                # 显示错误提示
                error_dialog = ctk.CTkToplevel(dialog)
                error_dialog.title("路径冲突")
                error_dialog.geometry("400x200")
                error_dialog.resizable(False, False)
                error_dialog.transient(dialog)
                error_dialog.grab_set()
                
                # 居中显示
                self._center_dialog(error_dialog)
                
                # 创建错误提示内容
                error_frame = ctk.CTkFrame(error_dialog, fg_color="transparent")
                error_frame.pack(fill="both", expand=True, padx=20, pady=20)
                
                error_label = ctk.CTkLabel(error_frame, 
                                          text="❌ 路径冲突",
                                          font=ctk.CTkFont(size=16, weight="bold"),
                                          text_color="red")
                error_label.pack(pady=(0, 10))
                
                error_msg = ctk.CTkLabel(error_frame,
                                        text=f"路径 '{path}' 已在分类 '{existing_category}' 中配置\n请先移除后再添加到当前分类",
                                        font=ctk.CTkFont(size=12),
                                        wraplength=350)
                error_msg.pack(pady=(0, 20))
                
                close_btn = ctk.CTkButton(error_frame,
                                         text="确定",
                                         font=ctk.CTkFont(size=13, weight="bold"),
                                         height=35,
                                         fg_color=("#f44336", "#d32f2f"),
                                         hover_color=("#d32f2f", "#b71c1c"),
                                         text_color=("white", "white"),
                                         command=error_dialog.destroy)
                close_btn.pack()
                return
            
            # 获取当前路径列表
            current_paths = self.controller.asset_manager.get_category_paths(category)
            # 添加新路径
            if path not in current_paths:
                current_paths.append(path)
                # 保存到资产管理器
                self.controller.asset_manager.set_category_paths(category, current_paths)
                # 更新UI
                self._update_path_config_dialog(category, scrollable_frame, dialog)
    
    def _remove_category_path_dialog(self, category, path, dialog):
        """为分类移除路径（对话框版本）"""
        # 获取当前路径列表
        current_paths = self.controller.asset_manager.get_category_paths(category)
        # 移除路径
        if path in current_paths:
            current_paths.remove(path)
            # 保存到资产管理器
            self.controller.asset_manager.set_category_paths(category, current_paths)
            # 更新UI
            self._update_path_config_dialog(category, dialog.scrollable_frame, dialog)
    
    def _update_path_config_dialog(self, category, scrollable_frame, dialog):
        """更新路径配置对话框显示"""
        # 清空现有路径项
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        
        # 获取该分类的路径列表
        paths = self.controller.asset_manager.get_category_paths(category)
        
        # 创建新的路径项
        path_frames = []
        for path in paths:
            path_frame = self._create_path_item_dialog(scrollable_frame, category, path, dialog)
            path_frames.append(path_frame)
        
        # 更新引用
        dialog.path_frames = path_frames
    
    def _center_dialog(self, dialog):
        """居中显示对话框"""
        # 等待窗口更新
        dialog.update_idletasks()
        
        # 获取父窗口的位置和尺寸
        parent_window = self.winfo_toplevel()
        parent_window.update_idletasks()
        
        parent_x = parent_window.winfo_x()
        parent_y = parent_window.winfo_y()
        parent_width = parent_window.winfo_width()
        parent_height = parent_window.winfo_height()
        
        # 获取对话框的尺寸
        dialog_width = dialog.winfo_width()
        dialog_height = dialog.winfo_height()
        
        # 计算对话框应该出现的位置（父窗口的视觉中心）
        dialog_x = parent_x + (parent_width - dialog_width) // 2
        dialog_y = parent_y + (parent_height - dialog_height) // 2
        
        # 设置对话框位置
        dialog.geometry(f"+{dialog_x}+{dialog_y}")
    
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