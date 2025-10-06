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
    # 设置CustomTkinter主题
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    
    # 初始化数据管理器和应用状态
    asset_manager = AssetManager()
    app_state = AppState()
    
    # 创建主窗口
    root = ctk.CTk()
    
    # 设置窗口标题
    root.title("虚幻引擎工具箱")
    
    # 设置固定窗口大小
    window_width = 1085
    window_height = 800
    
    # 获取屏幕尺寸
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # 计算居中位置，增加小偏移量使窗口更居中
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    
    # 在Windows系统上，x轴增加偏移量使窗口更居中显示
    x += 150  # 增加更大的偏移量，进一步调整x轴位置使其更居中
    
    # 直接设置窗口尺寸和位置
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # 禁用自由调整大小
    root.resizable(False, False)
    
    # 创建主界面
    app = MainWindow(root, asset_manager, app_state)
    
    # 启动主循环
    root.mainloop()

if __name__ == "__main__":
    main()