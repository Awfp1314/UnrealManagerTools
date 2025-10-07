import customtkinter as ctk
from tkinter import filedialog, messagebox

class DialogUtils:
    """对话框工具类 - 统一管理常用对话框操作"""
    
    @staticmethod
    def center_window(window, parent=None):
        """居中显示窗口 - 增强版，确保窗口正确居中
        如果提供了parent参数，则相对于父窗口居中，否则相对于屏幕居中"""
        # 强制更新窗口信息
        window.update_idletasks()
        
        # 获取窗口尺寸
        window_width = window.winfo_width()
        window_height = window.winfo_height()
        
        if parent and parent.winfo_exists():
            # 相对于父窗口居中
            parent_x = parent.winfo_x()
            parent_y = parent.winfo_y()
            parent_width = parent.winfo_width()
            parent_height = parent.winfo_height()
            
            # 计算居中位置
            x = parent_x + (parent_width - window_width) // 2
            y = parent_y + (parent_height - window_height) // 2
        else:
            # 相对于屏幕居中
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            
            # 计算居中位置
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
        
        # 设置窗口位置
        window.geometry(f"+{x}+{y}")
        
        # 再次更新以确保应用新位置
        window.update_idletasks()
    
    @staticmethod
    def browse_folder(title="选择文件夹"):
        """浏览文件夹"""
        return filedialog.askdirectory(title=title)
    
    @staticmethod
    def browse_file(title="选择文件", filetypes=None):
        """浏览文件"""
        if filetypes is None:
            filetypes = [("所有文件", "*.*")]
        return filedialog.askopenfilename(title=title, filetypes=filetypes)
    
    @staticmethod
    def create_form_field(parent, label_text, var, entry_type="entry", **kwargs):
        """创建表单字段"""
        # 标签
        label = ctk.CTkLabel(parent, text=label_text, 
                            font=ctk.CTkFont(size=13, weight="bold"))
        label.pack(anchor="w", pady=(0, 5))
        
        # 初始化widget变量
        widget = None
        
        # 输入框
        if entry_type == "entry":
            widget = ctk.CTkEntry(parent, textvariable=var, 
                                 height=35, font=ctk.CTkFont(size=13), **kwargs)
        elif entry_type == "combobox":
            widget = ctk.CTkComboBox(parent, variable=var, 
                                   height=35, font=ctk.CTkFont(size=13), **kwargs)
        elif entry_type == "checkbox":
            widget = ctk.CTkCheckBox(parent, text=label_text, 
                                   variable=var, font=ctk.CTkFont(size=13), **kwargs)
            label.destroy()  # 复选框不需要单独的标签
        
        # 确保widget存在再调用pack
        if widget is not None:
            if entry_type != "checkbox":
                widget.pack(fill="x", pady=(0, 15))
            else:
                widget.pack(anchor="w", pady=15)
        
        return widget
    
    @staticmethod
    def create_file_picker_frame(parent, var, title="选择文件", filetypes=None):
        """创建文件选择框架"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=(0, 15))
        
        entry = ctk.CTkEntry(frame, textvariable=var, font=ctk.CTkFont(size=13))
        entry.pack(side="left", fill="x", expand=True)
        
        button = ctk.CTkButton(frame, text="浏览", width=80,
                              command=lambda: DialogUtils._set_file_path(var, title, filetypes))
        button.pack(side="right", padx=(5, 0))
        
        return frame
    
    @staticmethod
    def _set_file_path(var, title, filetypes):
        """设置文件路径"""
        if filetypes and filetypes[0][1].startswith("*."):
            # 文件选择
            file_path = DialogUtils.browse_file(title, filetypes)
            if file_path:
                var.set(file_path)
        else:
            # 文件夹选择
            folder_path = DialogUtils.browse_folder(title)
            if folder_path:
                var.set(folder_path)
    
    @staticmethod
    def create_button_frame(parent, buttons):
        """创建按钮框架"""
        btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
        btn_frame.pack(fill="x", pady=10)
        
        for button_config in buttons:
            if len(button_config) >= 3:
                text, command, side = button_config[:3]
                kwargs = button_config[3] if len(button_config) > 3 else {}
            else:
                continue
                
            btn = ctk.CTkButton(btn_frame, text=text, command=command, 
                               width=80, **kwargs)
            btn.pack(side=side, padx=5)
        
        return btn_frame
    
    @staticmethod
    def show_error(controller, message):
        """显示错误消息"""
        if hasattr(controller, 'show_status'):
            controller.show_status(message, "error")
        else:
            messagebox.showerror("错误", message)
    
    @staticmethod
    def show_success(controller, message):
        """显示成功消息"""
        if hasattr(controller, 'show_status'):
            controller.show_status(message, "success")
        else:
            messagebox.showinfo("成功", message)
    
    @staticmethod
    def create_category_selector(parent, var, categories, on_change=None):
        """创建分类选择器（支持自定义分类）"""
        category_list = [cat for cat in categories if cat != "全部"] + ["自定义..."]
        if not category_list:
            category_list = ["未分类", "自定义..."]
            
        combo = ctk.CTkComboBox(parent, variable=var, values=category_list,
                               height=35, font=ctk.CTkFont(size=13))
        combo.pack(fill="x", pady=(0, 15))
        
        # 自定义分类输入框
        custom_frame = ctk.CTkFrame(parent, fg_color="transparent")
        custom_var = ctk.StringVar()
        custom_entry = ctk.CTkEntry(custom_frame, textvariable=custom_var,
                                   placeholder_text="输入新分类名称",
                                   height=35, font=ctk.CTkFont(size=13),
                                   state="readonly")
        
        def handle_category_change(choice):
            if choice == "自定义...":
                custom_frame.pack(fill="x", pady=(5, 15))
                custom_entry.pack(fill="x")
                custom_entry.configure(state="normal")
            else:
                custom_frame.pack_forget()
                custom_entry.configure(state="readonly")
            
            if on_change:
                on_change(choice)
        
        combo.configure(command=handle_category_change)
        
        return combo, custom_var, custom_frame