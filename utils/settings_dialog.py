import customtkinter as ctk
from utils.dialog_utils import DialogUtils

class SettingsDialog:
    def __init__(self, root, app_state, on_settings_changed=None):
        self.root = root
        self.app_state = app_state
        self.on_settings_changed = on_settings_changed
        self.dialog = None
        
    def show(self):
        """显示设置对话框"""
        # 创建对话框窗口
        self.dialog = ctk.CTkToplevel(self.root)
        self.dialog.title("设置")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        
        # 居中显示对话框
        DialogUtils.center_window(self.dialog, self.root)
        
        # 使对话框模态
        self.dialog.grab_set()
        
        # 创建设置选项
        self.create_settings_ui()
    
    def create_settings_ui(self):
        """创建设置界面"""
        if not self.dialog:
            return
            
        # 设置标题
        title_label = ctk.CTkLabel(
            self.dialog,
            text="设置选项",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(20, 20))
        
        # 主题设置
        theme_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        theme_frame.pack(fill="x", padx=30, pady=10)
        
        theme_label = ctk.CTkLabel(theme_frame, text="主题")
        theme_label.pack(side="left", padx=(0, 10))
        
        current_theme = self.app_state.theme
        theme_var = ctk.StringVar(value=current_theme)
        
        theme_optionmenu = ctk.CTkOptionMenu(
            theme_frame,
            variable=theme_var,
            values=["Dark", "Light"],
            command=self.on_theme_change
        )
        theme_optionmenu.pack(side="left", fill="x", expand=True)
        
        # 关闭按钮
        close_button = ctk.CTkButton(
            self.dialog,
            text="关闭",
            command=self.close_dialog,
            width=100
        )
        close_button.pack(pady=30)
    
    def on_theme_change(self, theme):
        """处理主题变更"""
        self.app_state.set_theme(theme)
        ctk.set_appearance_mode(theme)
        if self.on_settings_changed:
            self.on_settings_changed("theme", theme)
    

            
    def close_dialog(self):
        """关闭对话框"""
        if self.dialog:
            self.dialog.destroy()
            self.dialog = None
    
    def destroy(self):
        """销毁对话框"""
        if self.dialog:
            self.dialog.destroy()
            self.dialog = None