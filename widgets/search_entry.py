import customtkinter as ctk

class SearchEntry(ctk.CTkFrame):
    def __init__(self, parent, placeholder_text="", height=35, command=None):
        super().__init__(parent, fg_color="transparent")
        self.command = command
        
        # 创建搜索框
        self.entry = ctk.CTkEntry(self, 
                                 placeholder_text=placeholder_text,
                                 height=height,
                                 font=ctk.CTkFont(size=13))
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind('<KeyRelease>', self.on_key_release)
        
        # 搜索图标按钮
        self.search_btn = ctk.CTkButton(self, 
                                       text="🔍",
                                       width=40,
                                       height=height,
                                       command=self.on_search_click,
                                       font=ctk.CTkFont(size=12))
        self.search_btn.pack(side="right", padx=(5, 0))

    def on_key_release(self, event=None):
        """处理键盘释放事件"""
        if self.command:
            self.command(self.entry.get())

    def on_search_click(self):
        """处理搜索按钮点击"""
        if self.command:
            self.command(self.entry.get())

    def get(self):
        """获取搜索内容"""
        return self.entry.get()

    def clear(self):
        """清空搜索框"""
        self.entry.delete(0, 'end')