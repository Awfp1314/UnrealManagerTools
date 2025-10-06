import customtkinter as ctk
from views.toolbar import Toolbar
from views.content.base_content import ContentManager
from utils.dialog_utils import DialogUtils

class MainWindow:
    def __init__(self, root, asset_manager, app_state):
        self.root = root
        self.asset_manager = asset_manager
        self.app_state = app_state
        
        # 初始化UI
        self.setup_window()
        self.create_ui()
        
        # 初始加载
        self.refresh_content()
    
    def show_status(self, message, status_type="info"):
        """显示状态信息"""
        if hasattr(self, 'content_manager') and hasattr(self.content_manager, 'current_content'):
            self.content_manager.current_content.show_status(message, status_type)
    
    def setup_window(self):
        """设置窗口属性 - 现代化设计"""
        # 配置网格布局
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # 设置窗口标题和图标
        self.root.title("🚀 虚幻引擎工具箱")
        
        # 设置窗口圆角（如果支持）
        try:
            self.root.configure(corner_radius=15)
        except:
            pass

    def create_ui(self):
        """创建用户界面 - 现代化设计"""
        # 左侧工具栏（现代化设计）
        self.toolbar = Toolbar(self.root, self, self.app_state)
        self.toolbar.grid(row=0, column=0, sticky="nsew", padx=(15, 7), pady=15)
        
        # 中间内容区域（现代化设计）
        self.content_manager = ContentManager(self.root, self)
        self.content_manager.grid(row=0, column=1, sticky="nsew", padx=7, pady=15)

    def set_current_tool(self, tool_name):
        """设置当前工具"""
        self.app_state.set_current_tool(tool_name)
        self.content_manager.show_content(tool_name)
        # 同步工具栏按钮状态
        if hasattr(self.toolbar, 'set_active_tool'):
            self.toolbar.set_active_tool(tool_name)

    def set_current_category(self, category):
        """设置当前分类"""
        self.app_state.set_current_category(category)
        self.refresh_content()

    def set_search_term(self, search_term):
        """设置搜索词"""
        self.app_state.set_search_term(search_term)
        self.refresh_content()

    def set_current_resource(self, resource):
        """设置当前选中的资源"""
        self.app_state.set_current_resource(resource)

    def refresh_content(self):
        """刷新内容显示"""
        self.content_manager.refresh_content()