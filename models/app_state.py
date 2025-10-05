class AppState:
    def __init__(self):
        self.current_tool = "ue_asset_library"  # 默认工具
        self.current_category = "全部"
        self.search_term = ""
        self.current_resource = None
        self.theme = "Dark"  # 默认深色主题
    
    def set_theme(self, theme):
        """设置主题"""
        self.theme = theme
    

        
    def set_current_tool(self, tool_name):
        """设置当前工具"""
        self.current_tool = tool_name
        
    def set_current_category(self, category):
        """设置当前分类"""
        self.current_category = category
        
    def set_search_term(self, search_term):
        """设置搜索词"""
        self.search_term = search_term.lower()
        
    def set_current_resource(self, resource):
        """设置当前选中的资源"""
        self.current_resource = resource