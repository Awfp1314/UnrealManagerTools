import customtkinter as ctk
import os
from utils.dialog_utils import DialogUtils

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
        
        # 添加分类路径配置区域
        category_path_frame = ctk.CTkFrame(content_frame, corner_radius=10)
        category_path_frame.pack(fill="x", pady=(0, 20), ipady=10)
        
        # 分类路径配置标题
        category_path_title = ctk.CTkLabel(category_path_frame, text="分类路径配置",
                                          font=ctk.CTkFont(size=16, weight="bold"))
        category_path_title.pack(anchor="w", padx=20, pady=(15, 10))
        
        # 配置按钮
        config_button = ctk.CTkButton(
            category_path_frame,
            text="配置分类路径",
            command=self.show_category_path_config_dialog,
            width=150,
            height=35
        )
        config_button.pack(pady=20)
        
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
        
    def show_category_path_config_dialog(self):
        """显示分类路径配置对话框"""
        # 创建选择分类对话框
        dialog = ctk.CTkToplevel(self.controller.root)
        dialog.title("选择分类")
        dialog.geometry("400x350")  # 增加高度以确保按钮可见
        dialog.resizable(False, False)
        dialog.transient(self.controller.root)
        dialog.grab_set()
        
        # 居中显示
        DialogUtils.center_window(dialog, self.controller.root)
        
        # 创建主框架
        main_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 标题
        title_label = ctk.CTkLabel(main_frame, text="选择要配置路径的分类",
                                  font=ctk.CTkFont(size=16, weight="bold"))
        title_label.pack(pady=(0, 20))
        
        # 分类列表
        categories_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        categories_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # 获取可用分类（排除"全部"）
        available_categories = [cat for cat in self.controller.asset_manager.categories if cat != "全部"]
        
        if not available_categories:
            no_categories_label = ctk.CTkLabel(categories_frame, 
                                              text="暂无可用分类\n请先添加分类",
                                              font=ctk.CTkFont(size=12),
                                              text_color=("gray50", "gray50"))
            no_categories_label.pack(pady=50)
        else:
            # 创建可滚动的分类列表
            categories_scrollable = ctk.CTkScrollableFrame(categories_frame, height=180)  # 增加高度以确保内容完整显示
            categories_scrollable.pack(fill="both", expand=True)
            
            # 显示每个分类
            for category in available_categories:
                category_frame = ctk.CTkFrame(categories_scrollable, fg_color="transparent")
                category_frame.pack(fill="x", pady=5)
                
                category_label = ctk.CTkLabel(category_frame, text=category,
                                             font=ctk.CTkFont(size=13))
                category_label.pack(side="left", fill="x", expand=True)
                
                select_button = ctk.CTkButton(category_frame, text="配置路径",
                                             width=80, height=28,
                                             command=lambda c=category: self.select_category_for_path_config(dialog, c))
                select_button.pack(side="right")
        
        # 关闭按钮
        close_button = ctk.CTkButton(main_frame, text="关闭",
                                    command=dialog.destroy,
                                    width=80, height=35)
        close_button.pack()

    def select_category_for_path_config(self, dialog, category):
        """选择分类进行路径配置"""
        dialog.destroy()
        self.show_path_config_dialog(category)

    def show_path_config_dialog(self, category):
        """显示路径配置对话框"""
        # 创建路径配置对话框
        dialog = ctk.CTkToplevel(self.controller.root)
        dialog.title(f"配置分类 '{category}' 的路径")
        dialog.geometry("600x550")  # 增加高度以确保按钮可见
        dialog.resizable(False, False)
        dialog.transient(self.controller.root)
        dialog.grab_set()
        
        # 居中显示
        DialogUtils.center_window(dialog, self.controller.root)
        
        # 创建主框架
        main_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 标题
        title_label = ctk.CTkLabel(main_frame, text=f"配置分类 '{category}' 的路径",
                                  font=ctk.CTkFont(size=16, weight="bold"))
        title_label.pack(anchor="w", pady=(0, 20))
        
        # 当前路径列表
        paths_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        paths_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # 路径列表标题
        paths_title = ctk.CTkLabel(paths_frame, text="已配置的路径:",
                                  font=ctk.CTkFont(size=14, weight="bold"))
        paths_title.pack(anchor="w", pady=(0, 10))
        
        # 创建可滚动的路径列表
        self.paths_scrollable = ctk.CTkScrollableFrame(paths_frame, height=230)  # 增加高度以确保内容完整显示
        self.paths_scrollable.pack(fill="both", expand=True)
        
        # 加载当前路径
        self.load_category_paths(category)
        
        # 错误提示标签（默认隐藏）
        self.path_error_label = ctk.CTkLabel(main_frame, text="", 
                                            font=ctk.CTkFont(size=12),
                                            text_color=("red", "red"))
        self.path_error_label.pack(anchor="w", pady=(0, 10))
        
        # 添加路径框架
        add_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        add_frame.pack(fill="x", pady=(0, 20))
        
        add_label = ctk.CTkLabel(add_frame, text="添加新路径:",
                                font=ctk.CTkFont(size=14, weight="bold"))
        add_label.pack(anchor="w", pady=(0, 10))
        
        path_var = ctk.StringVar()
        path_frame = ctk.CTkFrame(add_frame, fg_color="transparent")
        path_frame.pack(fill="x")
        
        path_entry = ctk.CTkEntry(path_frame, textvariable=path_var,
                                 placeholder_text="选择或输入文件夹路径",
                                 height=35, font=ctk.CTkFont(size=13))
        path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        browse_button = ctk.CTkButton(path_frame, text="浏览",
                                     width=80, height=35,
                                     command=lambda: self.browse_folder(path_var))
        browse_button.pack(side="right")
        
        add_button = ctk.CTkButton(add_frame, text="添加路径",
                                  command=lambda: self.add_category_path(category, path_var),
                                  height=35, width=100)
        add_button.pack(pady=(15, 0))
        
        # 按钮框架
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x")
        
        close_button = ctk.CTkButton(button_frame, text="关闭",
                                    command=dialog.destroy,
                                    height=35, width=80)
        close_button.pack(side="right")

    def load_category_paths(self, category):
        """加载分类路径到界面"""
        # 清空现有显示
        for widget in self.paths_scrollable.winfo_children():
            widget.destroy()
        
        # 获取分类路径
        paths = self.controller.asset_manager.get_category_paths(category)
        
        if not paths:
            no_paths_label = ctk.CTkLabel(self.paths_scrollable, 
                                         text="暂无配置路径",
                                         font=ctk.CTkFont(size=12),
                                         text_color=("gray50", "gray50"))
            no_paths_label.pack(pady=20)
            return
        
        # 显示每个路径
        for path in paths:
            path_frame = ctk.CTkFrame(self.paths_scrollable, fg_color="transparent")
            path_frame.pack(fill="x", pady=5)
            
            path_label = ctk.CTkLabel(path_frame, text=path,
                                     font=ctk.CTkFont(size=12),
                                     anchor="w")
            path_label.pack(side="left", fill="x", expand=True)
            
            remove_button = ctk.CTkButton(path_frame, text="移除",
                                         width=60, height=28,
                                         fg_color="#d9534f",
                                         hover_color="#c9302c",
                                         command=lambda p=path, c=category: self.remove_category_path(c, p))
            remove_button.pack(side="right")

    def browse_folder(self, path_var):
        """浏览文件夹"""
        folder = DialogUtils.browse_folder("选择文件夹")
        if folder:
            path_var.set(folder)

    def add_category_path(self, category, path_var):
        """添加分类路径"""
        path = path_var.get().strip()
        if not path:
            self.path_error_label.configure(text="请输入或选择路径")
            return
            
        if not os.path.exists(path):
            self.path_error_label.configure(text="路径不存在")
            return
            
        # 检查路径冲突
        if self.controller.asset_manager.is_path_conflict(category, path):
            self.path_error_label.configure(text="路径已在其他分类中配置")
            return
            
        # 添加路径
        if self.controller.asset_manager.add_category_path(category, path):
            path_var.set("")  # 清空输入框
            self.path_error_label.configure(text="")  # 清除错误信息
            self.load_category_paths(category)  # 刷新显示
        else:
            self.path_error_label.configure(text="添加路径失败")

    def remove_category_path(self, category, path):
        """移除分类路径"""
        if self.controller.asset_manager.remove_category_path(category, path):
            self.load_category_paths(category)  # 刷新显示
        else:
            self.path_error_label.configure(text="移除路径失败")
