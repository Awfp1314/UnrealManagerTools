import customtkinter as ctk
import os
import threading
from datetime import datetime
from tkinter import messagebox
import customtkinter as ctk
from models.project_manager import ProjectManager
from utils.dialog_utils import DialogUtils

class UEProjectsContent(ctk.CTkFrame):
    """虚幻引擎工程内容界面"""
    
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=10)
        self.controller = controller
        self.project_manager = ProjectManager()
        self.is_data_loaded = False  # 数据加载状态
        self.last_refresh_time = None  # 上次刷新时间
        
        self.create_widgets()
        
        # 启动时边滇搜索工程（后台进行）
        self.start_initial_search()
    
    def start_initial_search(self):
        """启动初始搜索 - 后台进行，不阻塞界面"""
        def initial_search_thread():
            try:
                print(f"🔍 后台搜索UE工程...")
                projects = self.project_manager.refresh_projects()
                print(f"✅ 后台搜索完成，找到 {len(projects)} 个工程")
                
                # 标记数据已加载
                self.is_data_loaded = True
                self.last_refresh_time = datetime.now()
                
                # 在主线程中更新UI
                self.after(0, self._update_display_only)
                
            except Exception as e:
                print(f"后台搜索出错: {e}")
        
        # 在后台线程中执行搜索，不影响界面加载速度
        threading.Thread(target=initial_search_thread, daemon=True).start()
    
    def create_widgets(self):
        """创建界面组件"""
        # 主标题
        title_frame = ctk.CTkFrame(self, height=60, corner_radius=10)
        title_frame.pack(fill="x", padx=10, pady=(10, 0))
        title_frame.pack_propagate(False)
        
        title_label = ctk.CTkLabel(title_frame, text="虚幻引擎工程管理",
                                  font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(side="left", padx=20, pady=15)
        
        # 刷新按钮
        refresh_btn = ctk.CTkButton(title_frame, text="🔄 刷新工程",
                                   width=100, height=30,
                                   command=self.refresh_projects)
        refresh_btn.pack(side="right", padx=20, pady=15)
        
        # 搜索状态标签
        self.status_label = ctk.CTkLabel(title_frame, text="",
                                        font=ctk.CTkFont(size=12),
                                        text_color=("orange", "orange"))
        self.status_label.pack(side="right", padx=(0, 10), pady=15)
        
        # 内容区域
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 最近打开区域
        recent_frame = ctk.CTkFrame(content_frame)
        recent_frame.pack(fill="both", expand=True, pady=(0, 5))
        
        recent_title = ctk.CTkLabel(recent_frame, text="📂 最近打开",
                                   font=ctk.CTkFont(size=14, weight="bold"))
        recent_title.pack(anchor="w", padx=15, pady=(15, 5))
        
        # 最近打开的工程滚动区域
        self.recent_scroll = ctk.CTkScrollableFrame(recent_frame, height=150)
        self.recent_scroll.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # 所有工程区域
        projects_frame = ctk.CTkFrame(content_frame)
        projects_frame.pack(fill="both", expand=True, pady=(5, 0))
        
        projects_title = ctk.CTkLabel(projects_frame, text="🎮 所有工程",
                                     font=ctk.CTkFont(size=14, weight="bold"))
        projects_title.pack(anchor="w", padx=15, pady=(15, 5))
        
        # 搜索栏
        search_frame = ctk.CTkFrame(projects_frame, fg_color="transparent")
        search_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        self.search_var = ctk.StringVar()
        self.search_var.trace("w", self.on_search_change)
        search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var,
                                   placeholder_text="搜索工程名称...",
                                   height=32)
        search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # 排序选项
        sort_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
        sort_frame.pack(side="right")
        
        ctk.CTkLabel(sort_frame, text="排序:").pack(side="left", padx=(0, 5))
        self.sort_var = ctk.StringVar(value="修改时间")
        sort_combo = ctk.CTkComboBox(sort_frame, variable=self.sort_var,
                                    values=["修改时间", "名称", "创建时间"],
                                    width=100, command=self.on_sort_change)
        sort_combo.pack(side="left")
        
        # 所有工程的滚动区域
        self.projects_scroll = ctk.CTkScrollableFrame(projects_frame, height=300)
        self.projects_scroll.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # 增加滚动速度 - 绑定鼠标滚轮事件
        self.projects_scroll.bind("<MouseWheel>", self.on_projects_mouse_wheel)
        self.recent_scroll.bind("<MouseWheel>", self.on_recent_mouse_wheel)
        
        # 为所有子组件也绑定滚轮事件
        self.bind_children_mousewheel(self.projects_scroll)
        self.bind_children_mousewheel(self.recent_scroll)
        
        # 初始状态显示
        self.show_loading_state()

    def bind_children_mousewheel(self, widget):
        """递归绑定所有子组件的鼠标滚轮事件"""
        widget.bind("<MouseWheel>", self.on_projects_mouse_wheel)
        for child in widget.winfo_children():
            self.bind_children_mousewheel(child)

    def on_projects_mouse_wheel(self, event):
        """处理工程列表鼠标滚轮事件，增加滚动速度"""
        # 增加滚动速度（默认速度的10倍，让用户感觉更明显）
        self.projects_scroll._parent_canvas.yview_scroll(-10 * int(event.delta / 120), "units")
        
        # 阻止事件继续传播，避免其他组件处理
        return "break"

    def on_recent_mouse_wheel(self, event):
        """处理最近工程列表鼠标滚轮事件，增加滚动速度"""
        # 增加滚动速度（默认速度的10倍，让用户感觉更明显）
        self.recent_scroll._parent_canvas.yview_scroll(-10 * int(event.delta / 120), "units")
        
        # 阻止事件继续传播，避免其他组件处理
        return "break"

    def show_loading_state(self):
        """显示加载状态"""
        self.status_label.configure(text="正在搜索工程...")
        
        # 清空现有内容
        for widget in self.recent_scroll.winfo_children():
            widget.destroy()
        for widget in self.projects_scroll.winfo_children():
            widget.destroy()
        
        # 显示加载提示
        loading_label = ctk.CTkLabel(self.projects_scroll, text="🔍 正在搜索系统中的虚幻引擎工程...",
                                    font=ctk.CTkFont(size=12),
                                    text_color=("gray50", "gray50"))
        loading_label.pack(pady=50)
    
    def start_project_search(self):
        """启动工程搜索"""
        def search_thread():
            try:
                # 搜索工程
                projects = self.project_manager.search_ue_projects()
                
                # 在主线程中更新UI
                self.after(0, lambda: self.on_search_complete(projects))
                
            except Exception as e:
                self.after(0, lambda: self.on_search_error(str(e)))
        
        # 在后台线程中执行搜索
        threading.Thread(target=search_thread, daemon=True).start()
    
    def on_search_complete(self, projects):
        """搜索完成回调"""
        self.status_label.configure(text=f"找到 {len(projects)} 个工程")
        
        # 标记数据已加载
        self.is_data_loaded = True
        self.last_refresh_time = datetime.now()
        
        # 更新显示
        self._update_display_only()
    
    def on_search_error(self, error_msg):
        """搜索错误回调"""
        self.status_label.configure(text=f"搜索出错: {error_msg}")
        
        # 显示错误信息
        error_label = ctk.CTkLabel(self.projects_scroll, text=f"❌ 搜索失败: {error_msg}",
                                  font=ctk.CTkFont(size=12),
                                  text_color=("red", "red"))
        error_label.pack(pady=50)
    
    def refresh_projects(self):
        """刷新工程列表 - 强制刷新"""
        print(f"🔄 用户手动刷新工程列表")
        self.show_loading_state()
        self.is_data_loaded = False  # 重置加载状态
        self.start_project_search()
    
    def refresh_content(self, force=False):
        """刷新内容显示 - 智能刷新机制"""
        # 智能刷新判断
        if not force and self.is_data_loaded:
            # 数据已加载且非强制刷新，直接显示现有数据
            print(f"⚡ 快速显示已加载的UE工程数据")
            self._update_display_only()
            return
        
        # 需要刷新数据
        if not self.is_data_loaded:
            print(f"🔄 首次加载，进行数据刷新")
            self.show_loading_state()
            self.start_project_search()
        else:
            print(f"🔄 刷新UE工程数据")
            self.start_project_search()  # 强制重新搜索工程
            self.last_refresh_time = datetime.now()
    
    def _update_display_only(self):
        """仅更新显示，不重新加载数据"""
        try:
            # 更新状态显示
            projects_count = len(self.project_manager.get_projects())
            self.status_label.configure(text=f"找到 {projects_count} 个工程")
            
            # 更新界面显示
            self.update_recent_projects()
            self.update_all_projects()
        except Exception as e:
            print(f"更新显示出错: {e}")
            # 出错时回退到完整刷新
            self.refresh_content(force=True)
    
    def update_recent_projects(self):
        """更新最近打开的工程"""
        # 清空现有内容
        for widget in self.recent_scroll.winfo_children():
            widget.destroy()
        
        recent_projects = self.project_manager.get_recent_projects()
        
        if not recent_projects:
            no_recent_label = ctk.CTkLabel(self.recent_scroll, text="暂无最近打开的工程",
                                          font=ctk.CTkFont(size=12),
                                          text_color=("gray50", "gray50"))
            no_recent_label.pack(pady=20)
            return
        
        # 显示最近工程
        for project in recent_projects[:5]:  # 最多显示5个
            self.create_project_card(self.recent_scroll, project, is_recent=True)
    
    def update_all_projects(self):
        """更新所有工程"""
        # 清空现有内容
        for widget in self.projects_scroll.winfo_children():
            widget.destroy()
        
        projects = self.get_filtered_and_sorted_projects()
        
        if not projects:
            no_projects_label = ctk.CTkLabel(self.projects_scroll, text="未找到工程文件",
                                           font=ctk.CTkFont(size=12),
                                           text_color=("gray50", "gray50"))
            no_projects_label.pack(pady=50)
            return
        
        # 显示工程
        for project in projects:
            self.create_project_card(self.projects_scroll, project, is_recent=False)
    
    def get_filtered_and_sorted_projects(self):
        """获取过滤和排序后的工程列表"""
        projects = self.project_manager.get_projects()
        
        # 搜索过滤
        search_term = self.search_var.get().lower()
        if search_term:
            projects = [p for p in projects if search_term in p['name'].lower()]
        
        # 排序
        sort_by = self.sort_var.get()
        if sort_by == "名称":
            projects.sort(key=lambda x: x['name'].lower())
        elif sort_by == "创建时间":
            projects.sort(key=lambda x: x['created'], reverse=True)
        else:  # 修改时间
            projects.sort(key=lambda x: x['modified'], reverse=True)
        
        return projects
    
    def create_project_card(self, parent, project, is_recent=False):
        """创建工程卡片"""
        # 项目卡片框架（添加初始样式支持悬停动画）
        card_frame = ctk.CTkFrame(parent, 
                                height=80 if is_recent else 100,
                                fg_color=("gray92", "gray20"),  # 默认背景色
                                border_width=1,                  # 默认边框宽度
                                border_color=("gray70", "gray30"), # 默认边框颜色
                                corner_radius=10)                # 圆角
        card_frame.pack(fill="x", padx=5, pady=3)
        card_frame.pack_propagate(False)
        
        # 主要信息区域
        info_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        info_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        # 项目名称和状态
        header_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        header_frame.pack(fill="x")
        
        # 项目名称
        name_label = ctk.CTkLabel(header_frame, text=project['name'],
                                 font=ctk.CTkFont(size=14, weight="bold"))
        name_label.pack(side="left", anchor="w")
        
        # 最近打开标识
        if is_recent and 'last_opened' in project:
            try:
                last_opened = datetime.fromisoformat(project['last_opened'])
                time_str = last_opened.strftime("%m-%d %H:%M")
                recent_label = ctk.CTkLabel(header_frame, text=f"最近打开: {time_str}",
                                          font=ctk.CTkFont(size=10),
                                          text_color=("orange", "orange"))
                recent_label.pack(side="right")
            except:
                pass
        
        # 项目路径
        path_label = ctk.CTkLabel(info_frame, text=project['path'],
                                 font=ctk.CTkFont(size=10),
                                 text_color=("gray50", "gray50"))
        path_label.pack(anchor="w", pady=(2, 5))
        
        # 如果不是最近项目，显示更多信息
        if not is_recent:
            # 修改时间
            try:
                modified_time = datetime.fromisoformat(project['modified'])
                time_str = modified_time.strftime("%Y-%m-%d %H:%M")
                time_label = ctk.CTkLabel(info_frame, text=f"修改时间: {time_str}",
                                        font=ctk.CTkFont(size=9),
                                        text_color=("gray60", "gray60"))
                time_label.pack(anchor="w")
            except:
                pass
        
        # 操作按钮
        button_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(5, 0))
        
        # 打开工程按钮
        open_btn = ctk.CTkButton(button_frame, text="▶️ 打开工程",
                                width=100, height=28,
                                command=lambda p=project: self.open_project(p))
        open_btn.pack(side="left", padx=(0, 10))
        
        # 打开文件夹按钮
        folder_btn = ctk.CTkButton(button_frame, text="📁 打开文件夹",
                                  width=100, height=28,
                                  fg_color="transparent", border_width=1,
                                  command=lambda p=project: self.open_project_folder(p))
        folder_btn.pack(side="left", padx=(0, 10))
        
        # 项目信息按钮
        info_btn = ctk.CTkButton(button_frame, text="ℹ️ 详情",
                                width=80, height=28,
                                fg_color="transparent", border_width=1,
                                command=lambda p=project: self.show_project_info(p))
        info_btn.pack(side="right")
        
        # 绑定事件：双击、右键菜单和悬停动画
        self.bind_project_card_events(card_frame, project)
    
    def bind_project_card_events(self, card_frame, project):
        """绑定工程卡片事件"""
        # 获取所有子组件
        all_widgets = [card_frame]
        
        def get_all_children(widget):
            children = []
            for child in widget.winfo_children():
                children.append(child)
                children.extend(get_all_children(child))
            return children
        
        all_widgets.extend(get_all_children(card_frame))
        
        # 为所有组件绑定事件（除了按钮）
        for widget in all_widgets:
            # 跳过按钮组件，避免干扰按钮功能
            if not isinstance(widget, ctk.CTkButton):
                # 双击事件：直接打开项目
                widget.bind('<Double-Button-1>', lambda e, p=project: self.on_project_double_click(p))
                # 右键事件：显示菜单
                widget.bind('<Button-3>', lambda e, p=project: self.show_project_context_menu(e, p))
                # 悬停事件：动画效果
                widget.bind('<Enter>', lambda e, cf=card_frame: self.on_card_enter(cf))
                widget.bind('<Leave>', lambda e, cf=card_frame: self.on_card_leave(cf))
                # 鼠标指针样式
                widget.configure(cursor="hand2")
    
    def on_card_enter(self, card_frame):
        """鼠标进入卡片事件（悬停动画）"""
        try:
            # 平滑过渡到悬停状态
            self.animate_card_hover(card_frame, True)
        except Exception as e:
            print(f"悬停动画出错: {e}")
    
    def on_card_leave(self, card_frame):
        """鼠标离开卡片事件（悬停动画）"""
        try:
            # 平滑过渡到默认状态
            self.animate_card_hover(card_frame, False)
        except Exception as e:
            print(f"离开动画出错: {e}")
    
    def animate_card_hover(self, card_frame, is_hover, step=0, max_steps=1):
        """卡片悬停动画效果 - 优化版本，即时响应"""
        try:
            if not card_frame.winfo_exists():
                return
            
            # 即时设置最终状态，无延迟
            if is_hover:
                # 悬停状态：淡蓝色背景，蓝色边框
                card_frame.configure(
                    fg_color=("#e8f4fd", "#2d3748"),
                    border_width=2,
                    border_color=("#3182ce", "#4299e1")
                )
            else:
                # 默认状态：灰色背景，细边框
                card_frame.configure(
                    fg_color=("gray92", "gray20"),
                    border_width=1,
                    border_color=("gray70", "gray30")
                )
        
        except Exception as e:
            print(f"动画执行出错: {e}")
            # 发生错误时直接设置最终状态
            try:
                if is_hover:
                    card_frame.configure(
                        fg_color=("#e8f4fd", "#2d3748"),
                        border_width=2,
                        border_color=("#3182ce", "#4299e1")
                    )
                else:
                    card_frame.configure(
                        fg_color=("gray92", "gray20"),
                        border_width=1,
                        border_color=("gray70", "gray30")
                    )
            except:
                pass
    
    def on_project_double_click(self, project):
        """处理项目双击事件"""
        print(f"双击打开项目: {project['name']}")
        self.open_project(project)
    
    def show_project_context_menu(self, event, project):
        """显示项目右键菜单 - 优化版本，支持鼠标移出自动关闭"""
        # 关闭任何已存在的右键菜单
        self._close_all_context_menus()
        
        # 创建新的右键菜单
        self.current_context_menu = ctk.CTkToplevel(self.controller.root)
        self.current_context_menu.title("")
        self.current_context_menu.geometry("180x150")
        self.current_context_menu.overrideredirect(True)
        self.current_context_menu.attributes("-topmost", True)
        
        # 定位菜单位置
        x = event.x_root
        y = event.y_root
        self.current_context_menu.geometry(f"+{x}+{y}")
        
        # 设置菜单样式 - 优化亮色主题显示
        self.current_context_menu.configure(fg_color=("#f0f0f0", "gray20"))
        
        # 菜单选项
        menu_frame = ctk.CTkFrame(self.current_context_menu, fg_color="transparent")
        menu_frame.pack(fill="both", expand=True, padx=1, pady=1)
        
        # 菜单按钮
        buttons = [
            ('▶️ 打开项目', lambda: self.context_menu_action(self.current_context_menu, lambda: self.open_project(project))),
            ('📂 打开所在文件夹', lambda: self.context_menu_action(self.current_context_menu, lambda: self.open_project_folder(project))),
            ('🗑️ 删除项目', lambda: self.context_menu_action(self.current_context_menu, lambda: self.delete_project(project)))
        ]
        
        for text, command in buttons:
            btn = ctk.CTkButton(menu_frame, text=text, 
                               command=command,
                               height=30,
                               font=ctk.CTkFont(size=12),
                               anchor="w",
                               fg_color="transparent",
                               hover_color=("#e0e0e0", "gray30"),
                               text_color=("#333333", "#ffffff"))
            btn.pack(fill="x", padx=2, pady=1)
        
        # 获取当前项目卡片的区域信息
        project_widget = event.widget
        # 向上查找项目卡片的根容器
        while project_widget and hasattr(project_widget, 'winfo_class') and project_widget.winfo_class() != 'CTkFrame':
            project_widget = project_widget.master
        
        # 如果没有找到合适的容器，使用原始的事件widget
        if not project_widget:
            project_widget = event.widget
        
        # 绑定鼠标移出事件 - 智能关闭机制
        self._bind_smart_close_events(project_widget, project)
    
    def _close_all_context_menus(self):
        """关闭所有已存在的右键菜单"""
        # 关闭当前的右键菜单
        if hasattr(self, 'current_context_menu') and self.current_context_menu:
            try:
                if self.current_context_menu.winfo_exists():
                    self.current_context_menu.destroy()
            except Exception:
                pass
            finally:
                self.current_context_menu = None
    
    def _bind_smart_close_events(self, project_widget, project):
        """绑定智能关闭事件"""
        if not self.current_context_menu:
            return
            
        # 获取项目区域的边界
        try:
            project_x = project_widget.winfo_rootx()
            project_y = project_widget.winfo_rooty()
            project_width = project_widget.winfo_width()
            project_height = project_widget.winfo_height()
        except Exception:
            # 如果获取失败，使用默认的点击外部关闭
            self._bind_click_outside_close()
            return
        
        # 鼠标移动事件处理
        def on_mouse_move(event):
            try:
                if not self.current_context_menu or not self.current_context_menu.winfo_exists():
                    return
                
                mouse_x = event.x_root
                mouse_y = event.y_root
                
                # 检查鼠标是否在项目区域内
                in_project_area = (project_x <= mouse_x <= project_x + project_width and 
                                 project_y <= mouse_y <= project_y + project_height)
                
                # 检查鼠标是否在菜单区域内
                try:
                    menu_x = self.current_context_menu.winfo_rootx()
                    menu_y = self.current_context_menu.winfo_rooty()
                    menu_width = self.current_context_menu.winfo_width()
                    menu_height = self.current_context_menu.winfo_height()
                    
                    in_menu_area = (menu_x <= mouse_x <= menu_x + menu_width and 
                                  menu_y <= mouse_y <= menu_y + menu_height)
                except Exception:
                    in_menu_area = False
                
                # 如果鼠标离开了项目区域且不在菜单区域内，关闭菜单
                if not in_project_area and not in_menu_area:
                    self._close_all_context_menus()
                    # 解绑事件
                    self.controller.root.unbind('<Motion>', motion_handler_id)
                    
            except Exception as e:
                print(f"鼠标移动事件处理出错: {e}")
        
        # 绑定全局鼠标移动事件
        motion_handler_id = self.controller.root.bind('<Motion>', on_mouse_move, add='+')
        
        # 也绑定点击外部关闭作为备用
        self._bind_click_outside_close()
    
    def _bind_click_outside_close(self):
        """绑定点击外部关闭事件（备用机制）"""
        def on_click_outside(event):
            try:
                if not self.current_context_menu or not self.current_context_menu.winfo_exists():
                    return
                    
                # 检查点击位置是否在菜单外部
                menu_x = self.current_context_menu.winfo_rootx()
                menu_y = self.current_context_menu.winfo_rooty()
                menu_width = self.current_context_menu.winfo_width()
                menu_height = self.current_context_menu.winfo_height()
                
                if not (menu_x <= event.x_root <= menu_x + menu_width and 
                       menu_y <= event.y_root <= menu_y + menu_height):
                    self._close_all_context_menus()
            except Exception:
                pass
        
        # 绑定左键点击事件
        self.controller.root.bind('<Button-1>', on_click_outside, add='+')
    
    def context_menu_action(self, menu, action):
        """处理菜单动作"""
        try:
            if menu and menu.winfo_exists():
                menu.destroy()
        except Exception:
            pass
        
        # 执行动作
        if action:
            action()
    
    def delete_project(self, project):
        """删除项目（从列表中移除，不删除文件）"""
        from tkinter import messagebox
        
        # 确认对话框
        result = messagebox.askyesno(
            "确认删除", 
            f"确定要从列表中移除项目 '{project['name']}' 吗？\n\n注意：这只会从工程列表中移除，不会删除实际文件。",
            parent=self.controller.root
        )
        
        if result:
            try:
                # 从工程列表中移除
                self.project_manager.projects = [p for p in self.project_manager.projects if p['path'] != project['path']]
                
                # 从最近列表中移除
                self.project_manager.recent_projects = [p for p in self.project_manager.recent_projects if p['path'] != project['path']]
                
                # 保存配置
                self.project_manager.save_config()
                
                # 刷新界面
                self.refresh_content()
                
                self.show_status(f"已从列表中移除项目: {project['name']}", "success")
                
            except Exception as e:
                self.show_status(f"删除项目失败: {e}", "error")
    
    def open_project(self, project):
        """打开工程"""
        if self.project_manager.open_project(project):
            self.show_status(f"正在打开工程: {project['name']}", "success")
            # 刷新最近打开列表
            self.update_recent_projects()
        else:
            self.show_status(f"打开工程失败: {project['name']}", "error")
    
    def open_project_folder(self, project):
        """打开工程文件夹"""
        try:
            folder_path = project['dir']
            if os.path.exists(folder_path):
                os.startfile(folder_path)
                self.show_status(f"已打开工程文件夹: {project['name']}", "success")
            else:
                self.show_status("工程文件夹不存在", "error")
        except Exception as e:
            self.show_status(f"打开文件夹失败: {e}", "error")
    
    def show_project_info(self, project):
        """显示工程详细信息"""
        # 创建信息对话框
        info_dialog = ctk.CTkToplevel(self.controller.root)
        info_dialog.title(f"工程信息 - {project['name']}")
        info_dialog.geometry("500x400")
        info_dialog.transient(self.controller.root)
        info_dialog.grab_set()
        
        # 居中显示
        DialogUtils.center_window(info_dialog, self.controller.root)
        
        # 主框架
        main_frame = ctk.CTkFrame(info_dialog, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 标题
        title_label = ctk.CTkLabel(main_frame, text=project['name'],
                                  font=ctk.CTkFont(size=16, weight="bold"))
        title_label.pack(pady=(0, 15))
        
        # 滚动信息区域
        info_scroll = ctk.CTkScrollableFrame(main_frame)
        info_scroll.pack(fill="both", expand=True, pady=(0, 15))
        
        # 基本信息
        info_items = [
            ("项目名称", project['name']),
            ("项目路径", project['path']),
            ("项目目录", project['dir']),
            ("修改时间", self.format_datetime(project.get('modified', ''))),
            ("创建时间", self.format_datetime(project.get('created', ''))),
            ("文件大小", self.format_file_size(project.get('size', 0))),
        ]
        
        # 获取详细信息
        detailed_info = self.project_manager.get_project_info(project['path'])
        if detailed_info:
            info_items.extend([
                ("引擎版本", detailed_info.get('engine_version', '未知')),
                ("项目描述", detailed_info.get('description', '无')),
                ("项目分类", detailed_info.get('category', '无')),
                ("公司名称", detailed_info.get('company', '无')),
                ("插件数量", str(detailed_info.get('plugins', 0))),
                ("模块数量", str(detailed_info.get('modules', 0))),
            ])
        
        # 显示信息
        for label, value in info_items:
            item_frame = ctk.CTkFrame(info_scroll, fg_color="transparent")
            item_frame.pack(fill="x", pady=2)
            
            label_widget = ctk.CTkLabel(item_frame, text=f"{label}:",
                                       font=ctk.CTkFont(size=12, weight="bold"),
                                       width=100, anchor="w")
            label_widget.pack(side="left", padx=(0, 10))
            
            value_widget = ctk.CTkLabel(item_frame, text=str(value),
                                       font=ctk.CTkFont(size=12),
                                       anchor="w")
            value_widget.pack(side="left", fill="x", expand=True)
        
        # 关闭按钮
        close_btn = ctk.CTkButton(main_frame, text="关闭",
                                 command=info_dialog.destroy)
        close_btn.pack()
    
    def format_datetime(self, datetime_str):
        """格式化日期时间"""
        try:
            if datetime_str:
                dt = datetime.fromisoformat(datetime_str)
                return dt.strftime("%Y-%m-%d %H:%M:%S")
            return "未知"
        except:
            return "未知"
    
    def format_file_size(self, size_bytes):
        """格式化文件大小"""
        try:
            if size_bytes == 0:
                return "0 B"
            size_names = ["B", "KB", "MB", "GB"]
            i = 0
            while size_bytes >= 1024 and i < len(size_names) - 1:
                size_bytes /= 1024.0
                i += 1
            return f"{size_bytes:.1f} {size_names[i]}"
        except:
            return "未知"
    
    def on_search_change(self, *args):
        """搜索变化回调"""
        self.update_all_projects()
    
    def on_sort_change(self, value):
        """排序变化回调"""
        self.update_all_projects()
    
    def show_status(self, message, status_type="info"):
        """显示状态信息"""
        colors = {
            "info": ("blue", "blue"),
            "success": ("green", "green"),
            "error": ("red", "red"),
            "warning": ("orange", "orange")
        }
        
        color = colors.get(status_type, colors["info"])
        self.status_label.configure(text=message, text_color=color)
        
        # 3秒后清空状态
        self.after(3000, lambda: self.status_label.configure(text=""))