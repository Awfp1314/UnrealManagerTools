import customtkinter as ctk
from views.toolbar import Toolbar
from views.content.base_content import ContentManager
from utils.dialog_utils import DialogUtils

class MainWindow:
    def __init__(self, root, asset_manager, app_state):
        self.root = root
        self.asset_manager = asset_manager
        self.app_state = app_state
        
        # Initialize UI
        self.setup_window()
        self.create_ui()
        
        # Initial loading
        self.refresh_content()
    
    def show_status(self, message, status_type="info"):
        """Show status message"""
        if hasattr(self, 'content_manager') and self.content_manager:
            # Check if content_manager has current_page attribute and corresponding page
            if hasattr(self.content_manager, 'current_page') and self.content_manager.current_page:
                current_page_name = self.content_manager.current_page
                if current_page_name in self.content_manager.pages:
                    current_page = self.content_manager.pages[current_page_name]
                    # Check if current page has show_status method
                    if hasattr(current_page, 'show_status'):
                        current_page.show_status(message, status_type)
    
    def setup_window(self):
        """Set window properties - modern design"""
        # Configure grid layout
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # Set window title and icon
        self.root.title("🚀 Unreal Engine Toolbox")
        
        # Set window rounded corners (if supported)
        try:
            self.root.configure(corner_radius=15)
        except:
            pass
        
        # 启用双缓冲支持
        try:
            # 对于Tkinter的底层Canvas启用双缓冲
            self.root.attributes('-alpha', 1.0)
            # 对于支持的平台启用窗口级别双缓冲
            if hasattr(self.root, 'tk'):
                self.root.tk.call('tk', 'scaling', 1.0)
        except:
            pass
        
        # 解决最小化时窗口无法打开的问题
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind("<Map>", self.on_window_mapped)  # 窗口恢复事件
        self.root.bind("<Unmap>", self.on_window_unmapped)  # 窗口最小化事件
        
        # 确保窗口在最前面
        self.root.lift()
        self.root.focus_force()

    def on_closing(self):
        """处理窗口关闭事件"""
        self.root.destroy()

    def on_window_mapped(self, event=None):
        """窗口恢复事件处理"""
        # 确保窗口正确显示
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def on_window_unmapped(self, event=None):
        """窗口最小化事件处理"""
        # 可以在这里添加最小化时的特殊处理
        pass

    def create_ui(self):
        """Create user interface - modern design"""
        # Left toolbar (modern design)
        self.toolbar = Toolbar(self.root, self, self.app_state)
        self.toolbar.grid(row=0, column=0, sticky="nsew", padx=(15, 7), pady=15)
        
        # Middle content area (modern design)
        self.content_manager = ContentManager(self.root, self)
        self.content_manager.grid(row=0, column=1, sticky="nsew", padx=7, pady=15)

    def set_current_tool(self, tool_name):
        """Set current tool"""
        self.app_state.set_current_tool(tool_name)
        self.content_manager.show_content(tool_name)
        # Sync toolbar button status
        if hasattr(self.toolbar, 'set_active_tool'):
            self.toolbar.set_active_tool(tool_name)

    def set_current_category(self, category):
        """Set current category"""
        self.app_state.set_current_category(category)
        self.refresh_content()

    def set_search_term(self, search_term):
        """Set search term"""
        self.app_state.set_search_term(search_term)
        self.refresh_content()

    def set_current_resource(self, resource):
        """Set current selected resource"""
        self.app_state.set_current_resource(resource)

    def refresh_content(self):
        """Refresh content display"""
        self.content_manager.refresh_content()