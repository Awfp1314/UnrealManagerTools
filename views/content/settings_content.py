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
        
        # 主题选项
        theme_options_frame = ctk.CTkFrame(theme_frame, fg_color="transparent")
        theme_options_frame.pack(fill="x", padx=20)
        
        ctk.CTkLabel(theme_options_frame, text="选择主题:").pack(anchor="w", pady=(0, 5))
        
        self.theme_var = ctk.StringVar(value=self.app_state.theme)
        theme_combo = ctk.CTkComboBox(theme_options_frame, 
                                 variable=self.theme_var,
                                 values=["System", "Dark", "Light"],
                                 command=self.change_theme,
                                 width=200)
        theme_combo.pack(anchor="w")
        
        # 资产库设置区域
        asset_frame = ctk.CTkFrame(content_frame, corner_radius=10)
        asset_frame.pack(fill="x", pady=(0, 20), ipady=10)
        
        # 资产库设置标题
        asset_title = ctk.CTkLabel(asset_frame, text="资产库设置",
                              font=ctk.CTkFont(size=16, weight="bold"))
        asset_title.pack(anchor="w", padx=20, pady=(15, 10))
        
        # 自动刷新选项
        auto_refresh_frame = ctk.CTkFrame(asset_frame, fg_color="transparent")
        auto_refresh_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        self.auto_refresh_var = ctk.BooleanVar(value=self.controller.asset_manager.config.get("settings", {}).get("auto_refresh", True))
        auto_refresh_check = ctk.CTkCheckBox(auto_refresh_frame, 
                                        text="自动刷新资产库",
                                        variable=self.auto_refresh_var,
                                        command=self.toggle_auto_refresh)
        auto_refresh_check.pack(anchor="w")
        
        # 分类管理区域
        category_frame = ctk.CTkFrame(content_frame, corner_radius=10)
        category_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # 分类管理标题
        category_title = ctk.CTkLabel(category_frame, text="分类管理",
                                 font=ctk.CTkFont(size=16, weight="bold"))
        category_title.pack(anchor="w", padx=20, pady=(15, 10))
        
        # 分类列表框架
        categories_frame = ctk.CTkFrame(category_frame, fg_color="transparent")
        categories_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        # 分类列表标题
        ctk.CTkLabel(categories_frame, text="现有分类:", 
                font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0, 5))
        
        # 分类滚动区域
        categories_scrollable = ctk.CTkScrollableFrame(categories_frame, height=180)  # 增加高度以确保内容完整显示
        categories_scrollable.pack(fill="both", expand=True)
        
        # 增加滚动速度 - 绑定鼠标滚轮事件
        categories_scrollable.bind("<MouseWheel>", self.on_categories_mouse_wheel)
        
        # 为所有子组件也绑定滚轮事件
        self.bind_children_mousewheel(categories_scrollable)
        
        # 加载分类列表
        self.load_categories(categories_scrollable)
        
        # 添加分类框架
        add_frame = ctk.CTkFrame(category_frame, fg_color="transparent")
        add_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(add_frame, text="添加新分类:", 
                font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0, 10))
        
        add_input_frame = ctk.CTkFrame(add_frame, fg_color="transparent")
        add_input_frame.pack(fill="x")
        
        self.new_category_var = ctk.StringVar()
        new_category_entry = ctk.CTkEntry(add_input_frame, 
                                     textvariable=self.new_category_var,
                                     placeholder_text="输入新分类名称",
                                     height=35,
                                     font=ctk.CTkFont(size=13))
        new_category_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        add_btn = ctk.CTkButton(add_input_frame, 
                           text="添加",
                           command=self.add_category,
                           height=35,
                           width=80,
                           font=ctk.CTkFont(size=13))
        add_btn.pack(side="right")
        
        # 路径配置区域
        path_frame = ctk.CTkFrame(content_frame, corner_radius=10)
        path_frame.pack(fill="both", expand=True)
        
        # 路径配置标题
        path_title = ctk.CTkLabel(path_frame, text="分类路径配置",
                             font=ctk.CTkFont(size=16, weight="bold"))
        path_title.pack(anchor="w", padx=20, pady=(15, 10))
        
        # 路径配置内容
        path_content = ctk.CTkFrame(path_frame, fg_color="transparent")
        path_content.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        # 分类选择
        ctk.CTkLabel(path_content, text="选择分类:", 
                font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0, 5))
        
        # 获取现有分类（排除"全部"）
        categories = [cat for cat in self.controller.asset_manager.categories if cat != "全部"]
        if not categories:
            categories = ["默认"]
        
        self.category_path_var = ctk.StringVar(value=categories[0] if categories else "")
        category_path_combo = ctk.CTkComboBox(path_content, 
                                         variable=self.category_path_var,
                                         values=categories,
                                         command=self.on_category_path_change,
                                         width=200)
        category_path_combo.pack(anchor="w", pady=(0, 15))
        
        # 路径列表标题
        ctk.CTkLabel(path_content, text="配置路径:", 
                font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0, 5))
        
        # 路径列表框架
        paths_frame = ctk.CTkFrame(path_content, fg_color="transparent")
        paths_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # 路径滚动区域
        self.paths_scrollable = ctk.CTkScrollableFrame(paths_frame, height=230)  # 增加高度以确保内容完整显示
        self.paths_scrollable.pack(fill="both", expand=True)
        
        # 增加滚动速度 - 绑定鼠标滚轮事件
        self.paths_scrollable.bind("<MouseWheel>", self.on_paths_mouse_wheel)
        
        # 为所有子组件也绑定滚轮事件
        self.bind_children_mousewheel(self.paths_scrollable)
        
        # 添加路径输入框
        self.path_var = ctk.StringVar()
        path_input_frame = ctk.CTkFrame(path_content, fg_color="transparent")
        path_input_frame.pack(fill="x", pady=(0, 10))
        
        path_entry = ctk.CTkEntry(path_input_frame, textvariable=self.path_var,
                                 placeholder_text="输入或选择文件夹路径",
                                 height=35, font=ctk.CTkFont(size=13))
        path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        browse_button = ctk.CTkButton(path_input_frame, text="浏览",
                                     width=80, height=35,
                                     command=lambda: self.browse_folder(self.path_var))
        browse_button.pack(side="right")
        
        # 错误提示标签（默认隐藏）
        self.path_error_label = ctk.CTkLabel(path_content, text="", 
                                            font=ctk.CTkFont(size=12),
                                            text_color=("red", "red"))
        self.path_error_label.pack(anchor="w", pady=(0, 10))
        
        # 添加路径按钮
        add_path_btn = ctk.CTkButton(path_content, 
                                text="添加路径",
                                command=self.add_category_path,
                                height=35,
                                font=ctk.CTkFont(size=13))
        add_path_btn.pack(anchor="w")

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

    def bind_children_mousewheel(self, widget):
        """递归绑定所有子组件的鼠标滚轮事件"""
        widget.bind("<MouseWheel>", self.on_categories_mouse_wheel)
        for child in widget.winfo_children():
            self.bind_children_mousewheel(child)

    def on_categories_mouse_wheel(self, event):
        """处理分类列表鼠标滚轮事件，增加滚动速度"""
        # 增加滚动速度（默认速度的10倍，让用户感觉更明显）
        categories_scrollable = None
        # 查找正确的滚动框
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkScrollableFrame) and hasattr(widget, '_parent_canvas'):
                categories_scrollable = widget
                break
        if categories_scrollable:
            categories_scrollable._parent_canvas.yview_scroll(-10 * int(event.delta / 120), "units")
        
        # 阻止事件继续传播，避免其他组件处理
        return "break"

    def on_paths_mouse_wheel(self, event):
        """处理路径列表鼠标滚轮事件，增加滚动速度"""
        # 增加滚动速度（默认速度的10倍，让用户感觉更明显）
        self.paths_scrollable._parent_canvas.yview_scroll(-10 * int(event.delta / 120), "units")
        
        # 阻止事件继续传播，避免其他组件处理
        return "break"

    def load_categories(self, categories_scrollable):
        """加载分类列表"""
        # 清空现有显示
        for widget in categories_scrollable.winfo_children():
            widget.destroy()
        
        # 获取分类列表
        categories = [cat for cat in self.controller.asset_manager.categories if cat != "全部"]
        if not categories:
            no_categories_label = ctk.CTkLabel(categories_scrollable, 
                                              text="暂无可用分类\n请先添加分类",
                                              font=ctk.CTkFont(size=12),
                                              text_color=("gray50", "gray50"))
            no_categories_label.pack(pady=50)
            return
        
        # 显示每个分类
        for category in categories:
            category_frame = ctk.CTkFrame(categories_scrollable, fg_color="transparent")
            category_frame.pack(fill="x", pady=5)
            
            category_label = ctk.CTkLabel(category_frame, text=category,
                                             font=ctk.CTkFont(size=13))
            category_label.pack(side="left", fill="x", expand=True)
            
            remove_button = ctk.CTkButton(category_frame, text="删除",
                                             width=80, height=28,
                                             fg_color="#d9534f",
                                             hover_color="#c9302c",
                                             command=lambda c=category: self.remove_category(c))
            remove_button.pack(side="right")

    def add_category(self):
        """添加新分类"""
        category_name = self.new_category_var.get().strip()
        if not category_name:
            return
        
        if self.controller.asset_manager.add_category(category_name):
            self.new_category_var.set("")  # 清空输入框
            self.load_categories(self.paths_scrollable)  # 刷新显示
        else:
            self.path_error_label.configure(text="添加分类失败")

    def remove_category(self, category):
        """删除分类"""
        if self.controller.asset_manager.remove_category(category):
            self.load_categories(self.paths_scrollable)  # 刷新显示
        else:
            self.path_error_label.configure(text="删除分类失败")

    def on_category_path_change(self, category):
        """处理分类选择变化"""
        self.load_category_paths(category)



    def browse_folder(self, path_var):
        """浏览文件夹"""
        folder = DialogUtils.browse_folder("选择文件夹")
        if folder:
            path_var.set(folder)

    def add_category_path(self):
        """添加分类路径"""
        category = self.category_path_var.get()
        path = self.path_var.get().strip()
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
            self.path_var.set("")  # 清空输入框
            self.path_error_label.configure(text="")  # 清除错误信息
            self.load_category_paths(category)  # 刷新显示
        else:
            self.path_error_label.configure(text="添加路径失败")

    def add_category_path_dialog(self, category, path_var):
        """在对话框中添加分类路径"""
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

    def change_theme(self, theme):
        """处理主题变更"""
        self.app_state.set_theme(theme)
        ctk.set_appearance_mode(theme)
        
    def toggle_auto_refresh(self):
        """切换自动刷新设置"""
        auto_refresh = self.auto_refresh_var.get()
        self.controller.asset_manager.config.set("settings", "auto_refresh", auto_refresh)
        self.controller.asset_manager.config.save()
        
    def refresh_content(self):
        """刷新页面内容"""
        # 更新主题选择器的值以匹配当前状态
        self.theme_var.set(self.app_state.theme)
        self.auto_refresh_var.set(self.controller.asset_manager.config.get("settings", {}).get("auto_refresh", True))

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
                                  command=lambda: self.add_category_path_dialog(category, path_var),
                                  height=35, width=100)
        add_button.pack(pady=(15, 0))
        
        # 按钮框架
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x")
        
        close_button = ctk.CTkButton(button_frame, text="关闭",
                                    command=dialog.destroy,
                                    height=35, width=80)
        close_button.pack(side="right")


