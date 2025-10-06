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
        self.dialog.geometry("400x250")  # 调整高度以保持界面美观
        self.dialog.resizable(False, False)  # 设置为不可由用户自由调整大小
        
        # 确保对话框始终位于主窗口的视觉中心
        self._center_dialog_on_main_window()
        
        # 使对话框模态
        self.dialog.grab_set()
        
        # 创建设置选项
        self.create_settings_ui()
    
    def create_settings_ui(self):
        """创建设置界面"""
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
            command=self.dialog.destroy,
            width=100
        )
        close_button.pack(pady=30)
    
    def on_theme_change(self, theme):
        """处理主题变更"""
        self.app_state.set_theme(theme)
        ctk.set_appearance_mode(theme)
        if self.on_settings_changed:
            self.on_settings_changed("theme", theme)
    
    def _center_dialog_on_main_window(self):
        """将对话框居中显示在主窗口上"""
        # 等待窗口更新
        self.dialog.update_idletasks()
        
        # 获取主窗口的位置和尺寸
        main_window = self.root
        main_window.update_idletasks()
        
        main_x = main_window.winfo_x()
        main_y = main_window.winfo_y()
        main_width = main_window.winfo_width()
        main_height = main_window.winfo_height()
        
        # 获取对话框的尺寸
        dialog_width = self.dialog.winfo_width()
        dialog_height = self.dialog.winfo_height()
        
        # 计算对话框应该出现的位置（主窗口的视觉中心）
        dialog_x = main_x + (main_width - dialog_width) // 2
        dialog_y = main_y + (main_height - dialog_height) // 2
        
        # 设置对话框位置
        self.dialog.geometry(f"+{dialog_x}+{dialog_y}")
    
    def destroy(self):
        """销毁对话框"""
        if self.dialog:
            self.dialog.destroy()