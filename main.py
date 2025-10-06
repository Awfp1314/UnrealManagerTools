import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import customtkinter as ctk
from models.asset_manager import AssetManager
from models.app_state import AppState
from views.main_window import MainWindow
from utils.dialog_utils import DialogUtils

def main():
    # 设置CustomTkinter主题（现代化设计）
    ctk.set_appearance_mode("Dark")  # 默认深色主题
    ctk.set_default_color_theme("blue")  # 蓝色主题
    
    # 创建主窗口
    root = ctk.CTk()
    
    # 设置窗口标题（现代化设计）
    root.title("🚀 虚幻引擎工具箱 - 现代版")
    
    # 设置窗口大小（现代化设计）
    window_width = 1200  # 增加窗口宽度
    window_height = 850  # 增加窗口高度
    
    # 获取屏幕尺寸
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # 计算居中位置
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    
    # 设置窗口尺寸和位置
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # 禁用自由调整大小
    root.resizable(False, False)
    
    # 设置窗口圆角（如果支持）
    try:
        root.configure(corner_radius=15)
    except:
        pass
    
    # 强制更新窗口信息
    root.update_idletasks()
    
    # 初始化数据管理器和应用状态
    asset_manager = AssetManager()
    app_state = AppState()
    
    # 创建主界面
    app = MainWindow(root, asset_manager, app_state)
    
    # 启动主循环
    root.mainloop()

if __name__ == "__main__":
    main()