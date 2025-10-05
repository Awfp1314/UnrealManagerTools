import customtkinter as ctk
from tkinter import Menu, messagebox
import os
import webbrowser
import customtkinter as ctk
from utils.file_utils import FileUtils
from utils.dialog_utils import DialogUtils

class AssetCard(ctk.CTkFrame):
    def __init__(self, parent, asset, controller, image_utils):
        super().__init__(parent, 
                        corner_radius=12,
                        border_width=1,
                        border_color=("gray70", "gray30"))
        self.asset = asset
        self.controller = controller
        self.image_utils = image_utils
        self.file_utils = FileUtils()
        self.create_widgets()
        self.bind_events()

    def create_widgets(self):
        """创建资产卡片组件 - 紧凑布局"""
        # 缩略图容器
        thumbnail_frame = ctk.CTkFrame(self, fg_color="transparent", height=140)
        thumbnail_frame.pack(fill="x", padx=10, pady=(10, 5))
        thumbnail_frame.pack_propagate(False)
        
        # 缩略图
        thumbnail_size = (160, 130)  # 调整缩略图尺寸
        thumbnail = self.image_utils.load_thumbnail(self.asset.get('cover'), thumbnail_size)
        self.img_label = ctk.CTkLabel(thumbnail_frame, image=thumbnail, text="",
                                     fg_color="transparent", cursor="hand2")
        # 不需要手动保存引用，CTkImage会自动处理
        self.img_label.pack(expand=True)
        
        # 资产信息
        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # 名称
        asset_name = self.asset.get('name', '未命名')
        # 如果名称太长，截断并添加省略号
        if len(asset_name) > 18:  # 调整名称长度限制
            asset_name = asset_name[:18] + "..."
            
        self.name_label = ctk.CTkLabel(info_frame, text=asset_name,
                                      font=ctk.CTkFont(size=12, weight="bold"),  # 调整字体大小
                                      cursor="hand2")
        self.name_label.pack(anchor="w", pady=(0, 5))
        
        # 分类信息
        meta_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        meta_frame.pack(fill="x")
        
        # 分类标签
        category_text = self.asset.get('category', '未分类')
        if len(category_text) > 10:  # 调整分类名称长度限制
            category_text = category_text[:10] + "..."
            
        self.category_label = ctk.CTkLabel(meta_frame, text=category_text,
                                          font=ctk.CTkFont(size=10),  # 调整字体大小
                                          text_color=("gray50", "gray50"))
        self.category_label.pack(side="left")
        
        # 添加日期（只显示月-日）
        date_added = self.asset.get('date_added', '')
        if date_added:
            try:
                # 提取月日部分
                date_parts = date_added.split()[0].split('-')  # 分解日期
                if len(date_parts) >= 3:
                    short_date = f"{date_parts[1]}-{date_parts[2]}"  # 只显示月-日
                else:
                    short_date = date_added.split()[0]
            except:
                short_date = ""
                
            if short_date:
                date_label = ctk.CTkLabel(meta_frame, text=short_date,
                                         font=ctk.CTkFont(size=9),  # 调整字体大小
                                         text_color=("gray60", "gray60"))
                date_label.pack(side="right")

    def bind_events(self):
        """绑定事件"""
        # 获取所有子组件
        all_widgets = [self]
        
        def get_all_children(widget):
            children = []
            for child in widget.winfo_children():
                children.append(child)
                children.extend(get_all_children(child))
            return children
        
        all_widgets.extend(get_all_children(self))
        
        # 为所有组件绑定事件
        for widget in all_widgets:
            widget.bind('<Button-1>', self.on_click)
            widget.bind('<Button-3>', self.on_right_click)
            widget.bind('<Enter>', self.on_enter)
            widget.bind('<Leave>', self.on_leave)

    def on_click(self, event):
        """处理左键点击"""
        self.controller.set_current_resource(self.asset)

    def on_right_click(self, event):
        """处理右键点击 - 优化版本，支持鼠标移出自动关闭"""
        # 关闭任何已存在的右键菜单
        self._close_all_context_menus()
        
        # 创建新的自定义右键菜单
        self.context_menu = ctk.CTkToplevel(self.controller.root)
        self.context_menu.title("")
        self.context_menu.geometry("200x210")  # 增加高度以容纳新选项
        self.context_menu.overrideredirect(True)
        self.context_menu.attributes("-topmost", True)
        
        # 定位菜单位置
        x = event.x_root
        y = event.y_root
        self.context_menu.geometry(f"+{x}+{y}")
        
        # 设置菜单样式 - 优化亮色主题显示
        self.context_menu.configure(fg_color=('#f0f0f0', 'gray20'))
        
        # 菜单选项
        menu_frame = ctk.CTkFrame(self.context_menu, fg_color="transparent")
        menu_frame.pack(fill="both", expand=True, padx=1, pady=1)
        
        # 菜单按钮 - 修改解压选项为导入到工程
        buttons = [
            ("📄 打开文档", self.open_document),
            ("📂 打开文件夹", self.open_folder),
            ("✏️ 编辑资产", self.edit_asset),  # 新增的编辑资产选项
            ("📁 更改分类", self.change_category),
            ("🎮 导入到UE工程", self.import_to_ue_project),  # 修改为导入到虚幻引擎工程
            ("---", None),
            ("🗑️ 删除资源", self.remove_asset)
        ]
        
        for text, command in buttons:
            if text == "---":
                # 分隔线
                separator = ctk.CTkFrame(menu_frame, height=1, fg_color=("gray70", "gray40"))
                separator.pack(fill="x", padx=5, pady=2)
            else:
                btn = ctk.CTkButton(menu_frame, text=text, 
                                   command=lambda cmd=command: self.menu_command(cmd),
                                   height=30,
                                   font=ctk.CTkFont(size=12),
                                   anchor="w",
                                   fg_color="transparent",
                                   hover_color=('#e0e0e0', 'gray30'),
                                   text_color=('#333333', '#ffffff'))
                btn.pack(fill="x", padx=2, pady=1)
        
        # 绑定智能关闭事件 - 鼠标移出资产区域自动关闭
        self._bind_smart_close_events()
    
    def _close_all_context_menus(self):
        """关闭所有已存在的右键菜单"""
        # 关闭当前的右键菜单
        if hasattr(self, 'context_menu') and self.context_menu:
            try:
                if self.context_menu.winfo_exists():
                    self.context_menu.destroy()
            except Exception:
                pass
            finally:
                self.context_menu = None
    
    def _bind_smart_close_events(self):
        """绑定智能关闭事件"""
        if not self.context_menu:
            return
            
        # 获取资产卡片的边界
        try:
            card_x = self.winfo_rootx()
            card_y = self.winfo_rooty()
            card_width = self.winfo_width()
            card_height = self.winfo_height()
        except Exception:
            # 如果获取失败，使用默认的点击外部关闭
            self._bind_click_outside_close()
            return
        
        # 鼠标移动事件处理
        def on_mouse_move(event):
            try:
                if not self.context_menu or not self.context_menu.winfo_exists():
                    return
                
                mouse_x = event.x_root
                mouse_y = event.y_root
                
                # 检查鼠标是否在资产卡片区域内
                in_card_area = (card_x <= mouse_x <= card_x + card_width and 
                               card_y <= mouse_y <= card_y + card_height)
                
                # 检查鼠标是否在菜单区域内
                try:
                    menu_x = self.context_menu.winfo_rootx()
                    menu_y = self.context_menu.winfo_rooty()
                    menu_width = self.context_menu.winfo_width()
                    menu_height = self.context_menu.winfo_height()
                    
                    in_menu_area = (menu_x <= mouse_x <= menu_x + menu_width and 
                                  menu_y <= mouse_y <= menu_y + menu_height)
                except Exception:
                    in_menu_area = False
                
                # 如果鼠标离开了资产卡片区域且不在菜单区域内，关闭菜单
                if not in_card_area and not in_menu_area:
                    self._close_all_context_menus()
                    # 解绑事件
                    self.controller.root.unbind('<Motion>', motion_handler_id)
                    
            except Exception as e:
                print(f"资产卡片鼠标移动事件处理出错: {e}")
        
        # 绑定全局鼠标移动事件
        motion_handler_id = self.controller.root.bind('<Motion>', on_mouse_move, add='+')
        
        # 也绑定点击外部关闭作为备用
        self._bind_click_outside_close()
    
    def _bind_click_outside_close(self):
        """绑定点击外部关闭事件（备用机制）"""
        def on_click_outside(event):
            try:
                if not self.context_menu or not self.context_menu.winfo_exists():
                    return
                    
                # 检查点击位置是否在菜单外部
                menu_x = self.context_menu.winfo_rootx()
                menu_y = self.context_menu.winfo_rooty()
                menu_width = self.context_menu.winfo_width()
                menu_height = self.context_menu.winfo_height()
                
                if not (menu_x <= event.x_root <= menu_x + menu_width and 
                       menu_y <= event.y_root <= menu_y + menu_height):
                    self._close_all_context_menus()
            except Exception:
                pass
        
        # 绑定左键点击事件
        self.controller.root.bind('<Button-1>', on_click_outside, add='+')

    def menu_command(self, command):
        """处理菜单命令"""
        try:
            if hasattr(self, 'context_menu') and self.context_menu:
                self.context_menu.destroy()
                self.context_menu = None
        except Exception:
            pass
            
        if command:
            command()

    def open_folder(self):
        """打开资源文件夹"""
        path = self.asset.get('path', '')
        if path and os.path.exists(path):
            try:
                os.startfile(path)
            except:
                webbrowser.open(path)
        else:
            # 使用状态显示替代弹窗
            if hasattr(self.controller, 'show_status'):
                self.controller.show_status("资源路径不存在", "error")

    def on_enter(self, event):
        """鼠标进入"""
        self.configure(fg_color=("gray80", "gray40"))

    def on_leave(self, event):
        """鼠标离开"""
        self.configure(fg_color=("gray90", "gray25"))

    def open_document(self):
        """打开文档"""
        doc_path = self.asset.get('doc', '')
        if doc_path and os.path.exists(doc_path):
            try:
                os.startfile(doc_path)
            except:
                webbrowser.open(doc_path)
        else:
            # 使用状态显示替代弹窗
            if hasattr(self.controller, 'show_status'):
                self.controller.show_status("该资源没有文档", "error")

    def import_to_ue_project(self):
        """导入到虚幻引擎工程"""
        import threading
        
        source_path = self.asset.get('path', '')
        if not source_path or not os.path.exists(source_path):
            if hasattr(self.controller, 'show_status'):
                self.controller.show_status("资源路径不存在", "error")
            return
        
        # 查找压缩包
        archive_files = self.find_archive_files(source_path)
        if not archive_files:
            if hasattr(self.controller, 'show_status'):
                self.controller.show_status("未找到支持的压缩包(.zip/.7z)", "error")
            return
        
        # 显示UE工程选择对话框
        self.show_ue_project_selection_dialog(archive_files)
    
    def find_archive_files(self, folder_path):
        """查找文件夹中的压缩包"""
        archive_files = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(('.zip', '.7z')):
                    archive_files.append(os.path.join(root, file))
        return archive_files
    
    def show_ue_project_selection_dialog(self, archive_files):
        """显示UE工程选择对话框"""
        # 从主窗口获取已加载的工程列表
        projects = self.get_preloaded_projects()
        
        # 创建工程选择对话框
        selection_dialog = ctk.CTkToplevel(self.controller.root)
        selection_dialog.title("选择虚幻引擎工程")
        selection_dialog.geometry("800x700")  # 进一步增加尺寸，确保按钮有足够空间
        selection_dialog.transient(self.controller.root)
        selection_dialog.grab_set()
        selection_dialog.resizable(True, True)  # 允许用户调整大小
        
        # 居中显示
        DialogUtils.center_window(selection_dialog)
        
        # 主框架 - 减少内边距，给内容更多空间
        main_frame = ctk.CTkFrame(selection_dialog, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # 标题
        title_label = ctk.CTkLabel(main_frame, text="选择虚幻引擎工程文件",
                                  font=ctk.CTkFont(size=16, weight="bold"))
        title_label.pack(pady=(0, 15))
        
        # 状态显示
        status_label = ctk.CTkLabel(main_frame, text=f"已找到 {len(projects)} 个工程",
                                   font=ctk.CTkFont(size=12),
                                   text_color=("green", "green"))
        status_label.pack(pady=(0, 15))
        
        # 工程列表框架 - 给列表更多空间
        projects_frame = ctk.CTkFrame(main_frame)
        projects_frame.pack(fill="both", expand=True, pady=(0, 20))  # 增加底部间距
        
        # 列表标题
        list_title = ctk.CTkLabel(projects_frame, text="可用的UE工程:",
                                 font=ctk.CTkFont(size=13, weight="bold"))
        list_title.pack(anchor="w", padx=15, pady=(15, 5))
        
        # 滚动框架 - 确保有足够高度
        scrollable_frame = ctk.CTkScrollableFrame(projects_frame, height=400)  # 进一步增加高度
        scrollable_frame.pack(fill="both", expand=True, padx=15, pady=(0, 20))  # 增加底部间距
        
        # 显示工程列表
        self.display_found_projects_simple(scrollable_frame, projects, archive_files)
        
        # 按钮框架 - 确保有足够空间且不收缩
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent", height=50)
        button_frame.pack(fill="x", pady=(10, 0))
        button_frame.pack_propagate(False)  # 防止框架收缩
        
        # 手动选择按钮 - 设置明确的尺寸
        manual_button = ctk.CTkButton(button_frame, text="手动选择文件", 
                                     width=120, height=35,
                                     command=lambda: self.manual_select_project(selection_dialog, archive_files))
        manual_button.pack(side="left", padx=(0, 10), pady=5)
        
        # 取消按钮 - 设置明确的尺寸
        cancel_button = ctk.CTkButton(button_frame, text="取消",
                                     width=80, height=35,
                                     command=selection_dialog.destroy,
                                     fg_color="transparent",
                                     border_width=1)
        cancel_button.pack(side="right", padx=(10, 0), pady=5)
        
        # 存储找到的工程
        self.found_projects = projects
        self.selection_dialog = selection_dialog
    
    def get_preloaded_projects(self):
        """从主窗口获取已加载的工程列表"""
        try:
            # 尝试从内容管理器中获取虚幻工程组件
            content_manager = self.controller.content_manager
            if hasattr(content_manager, 'content_frames') and 'ue_projects' in content_manager.content_frames:
                ue_projects_content = content_manager.content_frames['ue_projects']
                if hasattr(ue_projects_content, 'project_manager'):
                    projects = ue_projects_content.project_manager.get_projects()
                    # 转换为对话框需要的格式
                    return [{
                        'name': project['name'],
                        'path': project['path'],
                        'dir': project['dir']
                    } for project in projects]
            
            # 如果获取失败，返回空列表
            print("无法获取预加载的工程列表，使用手动选择")
            return []
            
        except Exception as e:
            print(f"获取预加载工程列表失败: {e}")
            return []
    
    def display_found_projects_simple(self, parent, projects, archive_files):
        """显示找到的工程列表（简化版）"""
        if not projects:
            no_projects_label = ctk.CTkLabel(parent, 
                                           text="未找到UE工程文件\n请点击'手动选择文件'按钮选择工程",
                                           font=ctk.CTkFont(size=12),
                                           text_color=("gray50", "gray50"))
            no_projects_label.pack(pady=50)
            return
        
        # 显示每个工程
        for project in projects:
            project_frame = ctk.CTkFrame(parent, height=80)  # 设置固定高度
            project_frame.pack(fill="x", padx=5, pady=3)
            project_frame.pack_propagate(False)  # 防止框架收缩
            
            # 工程信息
            info_frame = ctk.CTkFrame(project_frame, fg_color="transparent")
            info_frame.pack(fill="both", expand=True, padx=12, pady=10)
            
            # 工程名称
            name_label = ctk.CTkLabel(info_frame, text=project['name'],
                                     font=ctk.CTkFont(size=13, weight="bold"))
            name_label.pack(anchor="w")
            
            # 工程路径
            path_label = ctk.CTkLabel(info_frame, text=project['path'],
                                     font=ctk.CTkFont(size=10),
                                     text_color=("gray50", "gray50"))
            path_label.pack(anchor="w", pady=(2, 8))
            
            # 选择按钮 - 在右上角固定位置
            select_button = ctk.CTkButton(info_frame, text="选择此工程",
                                         width=100, height=32,
                                         command=lambda p=project: self.select_project(p, archive_files))
            select_button.place(relx=1.0, rely=0.0, anchor="ne")
    

    

    
    def display_found_projects(self, projects, archive_files):
        """显示找到的工程列表"""
        self.found_projects = projects
        
        if not projects:
            no_projects_label = ctk.CTkLabel(self.scrollable_frame, 
                                           text="未找到UE工程文件",
                                           font=ctk.CTkFont(size=12),
                                           text_color=("gray50", "gray50"))
            no_projects_label.pack(pady=20)
            return
        
        # 显示每个工程
        for project in projects:
            project_frame = ctk.CTkFrame(self.scrollable_frame, height=80)  # 设置固定高度
            project_frame.pack(fill="x", padx=5, pady=3)
            project_frame.pack_propagate(False)  # 防止框架收缩
            
            # 工程信息
            info_frame = ctk.CTkFrame(project_frame, fg_color="transparent")
            info_frame.pack(fill="both", expand=True, padx=12, pady=10)
            
            # 工程名称
            name_label = ctk.CTkLabel(info_frame, text=project['name'],
                                     font=ctk.CTkFont(size=13, weight="bold"))
            name_label.pack(anchor="w")
            
            # 工程路径
            path_label = ctk.CTkLabel(info_frame, text=project['path'],
                                     font=ctk.CTkFont(size=10),
                                     text_color=("gray50", "gray50"))
            path_label.pack(anchor="w", pady=(2, 8))
            
            # 选择按钮 - 在右上角固定位置
            select_button = ctk.CTkButton(info_frame, text="选择此工程",
                                         width=100, height=32,
                                         command=lambda p=project: self.select_project(p, archive_files))
            select_button.place(relx=1.0, rely=0.0, anchor="ne")
    
    def manual_select_project(self, dialog, archive_files):
        """手动选择工程文件"""
        from tkinter import filedialog
        
        ue_project_file = filedialog.askopenfilename(
            title="选择虚幻引擎工程文件",
            filetypes=[("虚幻引擎工程", "*.uproject")]
        )
        
        if ue_project_file:
            project = {
                'name': os.path.splitext(os.path.basename(ue_project_file))[0],
                'path': ue_project_file,
                'dir': os.path.dirname(ue_project_file)
            }
            dialog.destroy()
            self.process_selected_project(project, archive_files)
    
    def select_project(self, project, archive_files):
        """选择工程"""
        self.selection_dialog.destroy()
        self.process_selected_project(project, archive_files)
    
    def process_selected_project(self, project, archive_files):
        """处理选中的工程"""
        # 获取工程的Content目录
        project_dir = project['dir']
        content_dir = os.path.join(project_dir, "Content")
        
        # 检查Content目录是否存在
        if not os.path.exists(content_dir):
            try:
                os.makedirs(content_dir, exist_ok=True)
                print(f"创建 Content 目录: {content_dir}")
            except Exception as e:
                if hasattr(self.controller, 'show_status'):
                    self.controller.show_status(f"无法创建Content目录: {e}", "error")
                return
        
        # 显示导入进度对话框
        self.show_import_progress_dialog(archive_files, content_dir, project['name'])
        """查找文件夹中的压缩包"""
        archive_files = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(('.zip', '.7z')):
                    archive_files.append(os.path.join(root, file))
        return archive_files
    
    def show_import_progress_dialog(self, archive_files, content_dir, project_name):
        """显示导入进度对话框"""
        import threading
        
        # 创建进度对话框
        progress_dialog = ctk.CTkToplevel(self.controller.root)
        progress_dialog.title("导入到虚幻引擎工程")
        progress_dialog.geometry("500x250")  # 增加高度以显示更多信息
        progress_dialog.transient(self.controller.root)
        progress_dialog.grab_set()
        
        # 居中显示
        DialogUtils.center_window(progress_dialog)
        
        # 创建进度界面
        main_frame = ctk.CTkFrame(progress_dialog, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 标题
        title_label = ctk.CTkLabel(main_frame, text=f"正在导入到 {project_name}...",
                                  font=ctk.CTkFont(size=16, weight="bold"))
        title_label.pack(pady=(0, 10))
        
        # 目标目录显示
        target_label = ctk.CTkLabel(main_frame, text=f"目标目录: {content_dir}",
                                   font=ctk.CTkFont(size=10),
                                   text_color=("gray50", "gray50"))
        target_label.pack(pady=(0, 15))
        
        # 当前文件显示
        current_file_label = ctk.CTkLabel(main_frame, text="准备中...",
                                         font=ctk.CTkFont(size=12))
        current_file_label.pack(pady=(0, 10))
        
        # 进度条和百分比显示
        progress_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        progress_frame.pack(fill="x", pady=(0, 10))
        
        # 进度条
        progress_bar = ctk.CTkProgressBar(progress_frame, width=350)
        progress_bar.pack(side="left", fill="x", expand=True)
        progress_bar.set(0)
        
        # 百分比标签
        progress_label = ctk.CTkLabel(progress_frame, text="0%",
                                     font=ctk.CTkFont(size=12, weight="bold"),
                                     width=50)
        progress_label.pack(side="right", padx=(10, 0))
        
        # 取消按钮
        cancel_button = ctk.CTkButton(main_frame, text="取消", width=100,
                                     command=lambda: self.cancel_import(progress_dialog))
        cancel_button.pack()
        
        # 初始化取消标志
        self.import_cancelled = False
        
        # 绑定关闭事件
        def on_dialog_close():
            self.import_cancelled = True
            try:
                progress_dialog.destroy()
            except:
                pass
        
        progress_dialog.protocol("WM_DELETE_WINDOW", on_dialog_close)
        
        # 在新线程中执行导入
        def import_thread():
            try:
                total_files = len(archive_files)
                print(f"开始导入，总共 {total_files} 个文件")
                
                for i, archive_file in enumerate(archive_files):
                    if self.import_cancelled:
                        print("导入被取消")
                        break
                        
                    # 更新当前文件显示
                    filename = os.path.basename(archive_file)
                    print(f"正在处理文件 {i+1}/{total_files}: {filename}")
                    
                    # 使用立即执行的函数来避免lambda闭包问题
                    def update_current_file(f):
                        def update():
                            try:
                                if not self.import_cancelled:
                                    current_file_label.configure(text=f"正在导入: {f}")
                            except:
                                pass
                        return update
                    
                    progress_dialog.after(0, update_current_file(filename))
                    
                    # 先更新进度条到开始状态
                    start_progress = i / total_files
                    def update_start_progress(p):
                        def update():
                            try:
                                if not self.import_cancelled:
                                    progress_bar.set(p)
                                    progress_label.configure(text=f"{int(p * 100)}%")
                                    # 强制更新UI
                                    progress_dialog.update_idletasks()
                            except:
                                pass
                        return update
                    
                    progress_dialog.after(0, update_start_progress(start_progress))
                    
                    # 导入文件（解压并优化到Content目录）
                    success = self.import_single_archive_to_content(archive_file, content_dir, 
                                                                   lambda p: self.update_import_progress(progress_dialog, progress_bar, progress_label, start_progress, p / total_files))
                    
                    if not success and not self.import_cancelled:
                        error_msg = f"导入 {filename} 失败"
                        print(error_msg)
                        def show_error(msg):
                            def show():
                                try:
                                    self.show_import_error(msg)
                                except:
                                    pass
                            return show
                        progress_dialog.after(0, show_error(error_msg))
                    elif success:
                        print(f"导入 {filename} 成功")
                    
                    # 更新完成进度
                    end_progress = (i + 1) / total_files
                    def update_end_progress(p):
                        def update():
                            try:
                                if not self.import_cancelled:
                                    progress_bar.set(p)
                                    progress_label.configure(text=f"{int(p * 100)}%")
                                    # 强制更新UI
                                    progress_dialog.update_idletasks()
                            except:
                                pass
                        return update
                    
                    progress_dialog.after(0, update_end_progress(end_progress))
                
                if not self.import_cancelled:
                    # 导入完成，设置进度为100%
                    def set_complete_progress():
                        def update():
                            try:
                                progress_bar.set(1.0)
                                progress_label.configure(text="100%")
                                progress_dialog.update_idletasks()
                            except:
                                pass
                        return update
                    
                    progress_dialog.after(0, set_complete_progress())
                    
                    # 稍微延迟后关闭对话框让用户看到100%
                    def complete_after_delay():
                        try:
                            self.import_completed(progress_dialog, content_dir)
                        except:
                            pass
                    
                    progress_dialog.after(500, complete_after_delay)  # 500ms延迟
                    print("所有文件导入完成")
                    
            except Exception as e:
                error_msg = f"导入过程中出错: {str(e)}"
                print(error_msg)
                def show_error(msg):
                    def show():
                        try:
                            self.show_import_error(msg)
                        except:
                            pass
                    return show
                progress_dialog.after(0, show_error(error_msg))
        
        # 启动导入线程
        import_thread = threading.Thread(target=import_thread, daemon=True)
        import_thread.start()
    
    def update_progress_in_thread(self, dialog, progress_bar, progress_label, base_progress, additional_progress):
        """线程安全的进度更新"""
        total_progress = base_progress + additional_progress
        def update():
            try:
                if not self.extraction_cancelled:
                    final_progress = min(total_progress, 1.0)
                    progress_bar.set(final_progress)
                    progress_label.configure(text=f"{int(final_progress * 100)}%")
                    # 强制更新UI
                    dialog.update_idletasks()
            except:
                pass
        dialog.after(0, update)
    
    def update_import_progress(self, dialog, progress_bar, progress_label, base_progress, additional_progress):
        """线程安全的导入进度更新"""
        total_progress = base_progress + additional_progress
        def update():
            try:
                if not self.import_cancelled:
                    final_progress = min(total_progress, 1.0)
                    progress_bar.set(final_progress)
                    progress_label.configure(text=f"{int(final_progress * 100)}%")
                    # 强制更新UI
                    dialog.update_idletasks()
            except:
                pass
        dialog.after(0, update)
    
    def import_single_archive_to_content(self, archive_path, content_dir, progress_callback=None):
        """导入单个压缩包到UE工程的Content目录"""
        filename = os.path.basename(archive_path)
        name_without_ext = os.path.splitext(filename)[0]
        
        # 创建临时解压目录
        import tempfile
        temp_extract_path = tempfile.mkdtemp(prefix=f"ue_import_{name_without_ext}_")
        final_import_path = os.path.join(content_dir, name_without_ext)
        
        # 如果目标目录已存在，添加数字后缀
        counter = 1
        original_final_path = final_import_path
        while os.path.exists(final_import_path):
            final_import_path = f"{original_final_path}_{counter}"
            counter += 1
        
        try:
            print(f"开始导入 {filename} 到 {final_import_path}")
            
            # 执行解压到临时目录
            success = self._extract_archive_to_temp(archive_path, temp_extract_path, progress_callback)
            
            if success and not self.import_cancelled:
                # 优化目录结构并导入到Content目录
                self._optimize_and_import_to_content(temp_extract_path, final_import_path)
                print(f"导入完成: {final_import_path}")
                return True
            else:
                # 清理临时目录
                self._cleanup_directory(temp_extract_path)
                return False
                
        except Exception as e:
            print(f"导入 {archive_path} 失败: {e}")
            # 清理临时目录
            self._cleanup_directory(temp_extract_path)
            return False
    
    def _optimize_and_import_to_content(self, temp_path, final_path):
        """优化目录结构并导入到Content目录"""
        import shutil
        
        try:
            # 递归优化，直到找到真正的内容
            current_path = temp_path
            
            # 获取最终目录的名称（不包括路径）
            archive_name = os.path.basename(final_path)
            
            # 持续检查和优化，直到无法再优化
            max_iterations = 10  # 防止无限循环
            iteration = 0
            
            while iteration < max_iterations:
                temp_contents = os.listdir(current_path)
                
                if not temp_contents:
                    print("目录为空，跳过优化")
                    break
                
                # 情况1：只有一个子目录，且该目录包含实际内容
                if len(temp_contents) == 1:
                    single_item = temp_contents[0]
                    single_item_path = os.path.join(current_path, single_item)
                    
                    if os.path.isdir(single_item_path) and self._contains_meaningful_content(single_item_path):
                        print(f"发现单一子目录 '{single_item}'，检查是否需要优化")
                        
                        # 检查是否是同名嵌套或可以优化的目录
                        if single_item == archive_name or self._should_flatten_directory(single_item):
                            print(f"优化目录 '{single_item}'，继续检查")
                            # 更新当前路径为子目录，继续检查
                            current_path = single_item_path
                            iteration += 1
                            continue
                        else:
                            # 不同名的单一子目录，也可以优化
                            print(f"发现单一子目录 '{single_item}'，提升内容到根级别")
                            current_path = single_item_path
                            iteration += 1
                            continue
                
                # 情况2：检查是否存在与压缩包同名的目录
                found_same_name = False
                for item in temp_contents:
                    item_path = os.path.join(current_path, item)
                    if os.path.isdir(item_path) and item == archive_name:
                        print(f"发现同名目录 '{item}'，继续优化")
                        current_path = item_path
                        found_same_name = True
                        iteration += 1
                        break
                
                if found_same_name:
                    continue
                
                # 无法再优化，退出循环
                break
            
            # 移动最终的内容到Content目录
            if current_path != temp_path:
                print(f"优化后的路径: {current_path}")
                shutil.move(current_path, final_path)
                # 清理原始临时目录
                if os.path.exists(temp_path) and temp_path != current_path:
                    self._cleanup_directory(temp_path)
            else:
                # 无需优化，直接移动
                print("使用默认结构，移动所有内容")
                shutil.move(temp_path, final_path)
            
        except Exception as e:
            print(f"优化并导入目录结构时出错: {e}")
            # 发生错误时，尝试简单移动
            try:
                if os.path.exists(temp_path):
                    shutil.move(temp_path, final_path)
            except:
                print("简单移动也失败，保留临时目录")
    
    def _should_flatten_directory(self, directory_name):
        """判断是否应该扁平化目录（对UE资产的特殊处理）"""
        # 常见的UE资产包装目录名称，这些应该被扁平化
        flatten_names = [
            'source', 'Source', 'content', 'Content', 'assets', 'Assets',
            'materials', 'Materials', 'textures', 'Textures', 'meshes', 'Meshes',
            'maps', 'Maps', 'blueprints', 'Blueprints'
        ]
        return directory_name in flatten_names
    
    def cancel_import(self, dialog):
        """取消导入"""
        print("用户取消导入操作")
        self.import_cancelled = True
        
        # 延迟一下然后关闭对话框，让线程有时间检查取消状态
        def close_dialog():
            try:
                dialog.destroy()
                if hasattr(self.controller, 'show_status'):
                    self.controller.show_status("导入已取消", "error")
            except:
                pass
        
        dialog.after(100, close_dialog)  # 100ms延迟
    
    def import_completed(self, dialog, content_dir):
        """导入完成"""
        dialog.destroy()
        if hasattr(self.controller, 'show_status'):
            self.controller.show_status(f"导入完成，目标目录: {content_dir}", "success")
    
    def show_import_error(self, error_msg):
        """显示导入错误"""
        if hasattr(self.controller, 'show_status'):
            self.controller.show_status(error_msg, "error")
        else:
            messagebox.showerror("错误", error_msg)
    
    def extract_single_archive(self, archive_path, dest_dir, progress_callback=None):
        """解压单个压缩包"""
        filename = os.path.basename(archive_path)
        name_without_ext = os.path.splitext(filename)[0]
        
        # 创建临时解压目录
        temp_extract_path = os.path.join(dest_dir, f"temp_{name_without_ext}")
        final_extract_path = os.path.join(dest_dir, name_without_ext)
        
        # 如果最终目标目录已存在，添加数字后缀
        counter = 1
        original_final_path = final_extract_path
        while os.path.exists(final_extract_path):
            final_extract_path = f"{original_final_path}_{counter}"
            counter += 1
        
        try:
            # 确保临时目录存在
            os.makedirs(temp_extract_path, exist_ok=True)
            
            # 执行解压
            success = self._extract_archive_to_temp(archive_path, temp_extract_path, progress_callback)
            
            if success and not self.extraction_cancelled:
                # 优化目录结构
                self._optimize_directory_structure(temp_extract_path, final_extract_path)
                print(f"解压并优化完成: {final_extract_path}")
                return True
            else:
                # 清理临时目录
                self._cleanup_directory(temp_extract_path)
                return False
                
        except Exception as e:
            print(f"解压 {archive_path} 失败: {e}")
            # 清理临时目录
            self._cleanup_directory(temp_extract_path)
            return False
    
    def _extract_archive_to_temp(self, archive_path, temp_extract_path, progress_callback=None):
        """将压缩包解压到临时目录"""
        if archive_path.lower().endswith('.zip'):
            print(f"正在解压 ZIP 文件: {archive_path} 到 {temp_extract_path}")
            import zipfile
            
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                total_files = len(file_list)
                
                for i, file_info in enumerate(file_list):
                    if hasattr(self, 'import_cancelled') and self.import_cancelled:
                        return False
                    if hasattr(self, 'extraction_cancelled') and self.extraction_cancelled:
                        return False
                        
                    # 解压单个文件
                    zip_ref.extract(file_info, temp_extract_path)
                    
                    # 更新进度
                    if progress_callback and total_files > 0:
                        progress = (i + 1) / total_files
                        progress_callback(progress)
                        
                        # 对于小文件，添加微小延迟让进度更可见
                        if total_files > 10 and i % 10 == 0:
                            import time
                            time.sleep(0.01)  # 10ms延迟
                        
            return True
            
        elif archive_path.lower().endswith('.7z'):
            print(f"正在解压 7Z 文件: {archive_path} 到 {temp_extract_path}")
            try:
                import py7zr
                # 使用新的py7zr API
                archive = py7zr.SevenZipFile(archive_path, mode='r')
                try:
                    file_list = archive.getnames()
                    total_files = len(file_list)
                    
                    # py7zr不支持单文件解压，但可以模拟进度
                    if progress_callback:
                        # 更加细致的进度模拟，使用更多步骤
                        for i in range(20):  # 增加到20步
                            if hasattr(self, 'import_cancelled') and self.import_cancelled:
                                return False
                            if hasattr(self, 'extraction_cancelled') and self.extraction_cancelled:
                                return False
                            progress_callback(0.05 + (i * 0.045))  # 0.05到0.95
                            import time
                            time.sleep(0.02)  # 20ms延迟让进度更可见
                        
                    archive.extractall(path=temp_extract_path)
                    
                    if progress_callback:
                        progress_callback(1.0)  # 完成
                        
                finally:
                    archive.close()
                    
                return True
                
            except ImportError:
                print("py7zr 库未安装，尝试使用系统命令")
                return self.extract_7z_with_system_command(archive_path, temp_extract_path, progress_callback)
            except Exception as e:
                print(f"py7zr 解压失败: {e}，尝试使用系统命令")
                return self.extract_7z_with_system_command(archive_path, temp_extract_path, progress_callback)
        
        print(f"不支持的文件格式: {archive_path}")
        return False
    
    def _optimize_directory_structure(self, temp_path, final_path):
        """优化目录结构，去除多余的嵌套目录"""
        import shutil
        
        try:
            # 递归优化，直到找到真正的内容
            current_path = temp_path
            
            # 获取最终目录的名称（不包括路径）
            archive_name = os.path.basename(final_path)
            
            # 持续检查和优化，直到无法再优化
            max_iterations = 10  # 防止无限循环
            iteration = 0
            
            while iteration < max_iterations:
                temp_contents = os.listdir(current_path)
                
                if not temp_contents:
                    print("目录为空，跳过优化")
                    break
                
                # 情况1：只有一个子目录，且该目录包含实际内容
                if len(temp_contents) == 1:
                    single_item = temp_contents[0]
                    single_item_path = os.path.join(current_path, single_item)
                    
                    if os.path.isdir(single_item_path) and self._contains_meaningful_content(single_item_path):
                        print(f"发现单一子目录 '{single_item}'，检查是否需要优化")
                        
                        # 检查是否是同名嵌套
                        if single_item == archive_name:
                            print(f"发现同名嵌套 '{single_item}'，继续优化")
                            # 更新当前路径为子目录，继续检查
                            current_path = single_item_path
                            iteration += 1
                            continue
                        else:
                            # 不同名的单一子目录，也可以优化
                            print(f"发现单一子目录 '{single_item}'，提升内容到根级别")
                            current_path = single_item_path
                            iteration += 1
                            continue
                
                # 情况2：检查是否存在与压缩包同名的目录
                found_same_name = False
                for item in temp_contents:
                    item_path = os.path.join(current_path, item)
                    if os.path.isdir(item_path) and item == archive_name:
                        print(f"发现同名目录 '{item}'，继续优化")
                        current_path = item_path
                        found_same_name = True
                        iteration += 1
                        break
                
                if found_same_name:
                    continue
                
                # 无法再优化，退出循环
                break
            
            # 移动最终的内容到目标目录
            if current_path != temp_path:
                print(f"优化后的路径: {current_path}")
                shutil.move(current_path, final_path)
                # 清理原始临时目录
                if os.path.exists(temp_path) and temp_path != current_path:
                    self._cleanup_directory(temp_path)
            else:
                # 无需优化，直接移动
                print("使用默认结构，移动所有内容")
                shutil.move(temp_path, final_path)
            
        except Exception as e:
            print(f"优化目录结构时出错: {e}")
            # 发生错误时，尝试简单移动
            try:
                if os.path.exists(temp_path):
                    shutil.move(temp_path, final_path)
            except:
                print("简单移动也失败，保留临时目录")
    
    def _contains_meaningful_content(self, directory_path):
        """检查目录是否包含有意义的内容（非空目录或有实际文件）"""
        try:
            for root, dirs, files in os.walk(directory_path):
                # 如果有文件，说明有实际内容
                if files:
                    return True
                # 如果有非空的子目录，也算有内容
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    if os.listdir(dir_path):  # 非空目录
                        return True
            return False
        except:
            return True  # 出错时保守处理，认为有内容
    
    def _cleanup_directory(self, directory_path):
        """清理目录"""
        import shutil
        try:
            if os.path.exists(directory_path):
                shutil.rmtree(directory_path)
                print(f"已清理目录: {directory_path}")
        except Exception as e:
            print(f"清理目录失败: {e}")
    
    def extract_7z_with_system_command(self, archive_path, temp_extract_path, progress_callback=None):
        """使用系统命令解压7z文件到临时目录"""
        try:
            import subprocess
            print(f"尝试使用系统 7z 命令解压: {archive_path}")
            
            # 确保临时目录存在
            os.makedirs(temp_extract_path, exist_ok=True)
            
            if progress_callback:
                progress_callback(0.1)  # 开始
            
            # 尝试使用7zip命令行工具
            cmd = ['7z', 'x', archive_path, f'-o{temp_extract_path}', '-y']
            print(f"执行命令: {' '.join(cmd)}")
            
            # 模拟进度更新
            if progress_callback:
                for i in range(5):
                    if hasattr(self, 'import_cancelled') and self.import_cancelled:
                        return False
                    if hasattr(self, 'extraction_cancelled') and self.extraction_cancelled:
                        return False
                    progress_callback(0.1 + (i * 0.15))  # 0.1到0.85
                    import time
                    time.sleep(0.1)
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if progress_callback:
                progress_callback(0.9)  # 接近完成
            
            print(f"7z 命令返回码: {result.returncode}")
            if result.stdout:
                print(f"7z 输出: {result.stdout}")
            if result.stderr:
                print(f"7z 错误: {result.stderr}")
            
            if result.returncode == 0:
                if progress_callback:
                    progress_callback(1.0)  # 完成
                print(f"系统命令解压成功: {temp_extract_path}")
                return True
            else:
                print(f"系统命令解压失败，返回码: {result.returncode}")
                return False
                
        except subprocess.TimeoutExpired:
            print("解压超时")
            return False
        except FileNotFoundError:
            print("7z 命令未找到，请安装 7-Zip")
            return False
        except Exception as e:
            print(f"系统命令解压失败: {e}")
            return False
    
    def cancel_extraction(self, dialog):
        """取消解压"""
        self.extraction_cancelled = True
        dialog.destroy()
        if hasattr(self.controller, 'show_status'):
            self.controller.show_status("解压已取消", "error")
    
    def extraction_completed(self, dialog, dest_dir):
        """解压完成"""
        dialog.destroy()
        if hasattr(self.controller, 'show_status'):
            self.controller.show_status(f"解压完成，目标目录: {dest_dir}", "success")
    
    def show_extraction_error(self, error_msg):
        """显示解压错误"""
        if hasattr(self.controller, 'show_status'):
            self.controller.show_status(error_msg, "error")
        else:
            messagebox.showerror("错误", error_msg)

    def edit_asset(self):
        """编辑资产信息"""
        # 创建编辑资产对话框
        dialog = ctk.CTkToplevel(self.controller.root)
        dialog.title("编辑资产")
        dialog.geometry("500x650")  # 增加高度以适应所有内容
        dialog.transient(self.controller.root)
        dialog.grab_set()
        
        # 居中显示
        DialogUtils.center_window(dialog)
        
        # 创建表单
        form_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 资源名称
        ctk.CTkLabel(form_frame, text="资源名称:", 
                    font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(0, 5))
        name_var = ctk.StringVar(value=self.asset.get('name', ''))
        name_entry = ctk.CTkEntry(form_frame, textvariable=name_var, 
                                 height=35, font=ctk.CTkFont(size=13))
        name_entry.pack(fill="x", pady=(0, 15))
        
        # 资源路径
        ctk.CTkLabel(form_frame, text="资源路径:", 
                    font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(0, 5))
        path_var = ctk.StringVar(value=self.asset.get('path', ''))
        path_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        path_frame.pack(fill="x", pady=(0, 15))
        path_entry = ctk.CTkEntry(path_frame, textvariable=path_var,
                                 font=ctk.CTkFont(size=13))
        path_entry.pack(side="left", fill="x", expand=True)
        
        ctk.CTkButton(path_frame, text="选择", width=80,
                     command=lambda: self.browse_folder(path_var)).pack(side="right", padx=(5, 0))
        
        # 分类
        ctk.CTkLabel(form_frame, text="分类:", 
                    font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(0, 5))
        category_var = ctk.StringVar(value=self.asset.get('category', ''))
        
        # 添加自定义选项到分类列表
        category_list = [cat for cat in self.controller.asset_manager.categories if cat != "全部"] + ["自定义..."]
        if not category_list:
            category_list = ["未分类", "自定义..."]
            
        category_combo = ctk.CTkComboBox(form_frame, variable=category_var, 
                                       values=category_list,
                                       height=35, font=ctk.CTkFont(size=13))
        category_combo.pack(fill="x", pady=(0, 15))
        
        # 自定义分类输入框（默认隐藏）
        custom_category_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        custom_category_var = ctk.StringVar()
        custom_category_entry = ctk.CTkEntry(custom_category_frame, 
                                           textvariable=custom_category_var,
                                           placeholder_text="输入新分类名称",
                                           height=35, font=ctk.CTkFont(size=13),
                                           state="readonly")  # 初始状态为不可编辑
        
        def on_category_change(choice):
            if choice == "自定义...":
                custom_category_frame.pack(fill="x", pady=(5, 15))
                custom_category_entry.pack(fill="x")
                custom_category_entry.configure(state="normal")  # 自定义时可编辑
            else:
                custom_category_frame.pack_forget()
                custom_category_entry.configure(state="readonly")  # 已有分类时不可编辑
        
        category_combo.configure(command=on_category_change)
        
        # 封面图片
        ctk.CTkLabel(form_frame, text="封面图片:", 
                    font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(0, 5))
        cover_var = ctk.StringVar(value=self.asset.get('cover', ''))
        cover_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        cover_frame.pack(fill="x", pady=(0, 15))
        cover_entry = ctk.CTkEntry(cover_frame, textvariable=cover_var,
                                  font=ctk.CTkFont(size=13))
        cover_entry.pack(side="left", fill="x", expand=True)
        
        ctk.CTkButton(cover_frame, text="选择", width=80,
                     command=lambda: self.browse_cover_image(cover_var)).pack(side="right", padx=(5, 0))
        
        # 是否创建README
        readme_var = ctk.BooleanVar(value=bool(self.asset.get('doc', '')))
        readme_check = ctk.CTkCheckBox(form_frame, text="创建/更新README.md文档",
                                      variable=readme_var,
                                      font=ctk.CTkFont(size=13))
        readme_check.pack(anchor="w", pady=15)
        
        def apply_changes():
            category = custom_category_var.get() if category_var.get() == "自定义..." else category_var.get()
            if not category:
                if hasattr(self.controller, 'show_status'):
                    self.controller.show_status("请选择或输入分类", "error")
                return
                
            if category_var.get() == "自定义...":
                if not self.controller.asset_manager.add_category(category):
                    if hasattr(self.controller, 'show_status'):
                        self.controller.show_status("添加分类失败", "error")
                    return
            
            if self.controller.asset_manager.update_resource(
                self.asset, name_var.get(), category, path_var.get(), 
                cover_var.get(), readme_var.get()):
                dialog.destroy()
                self.controller.refresh_content()
                if hasattr(self.controller, 'show_status'):
                    self.controller.show_status(f"已更新资产: {name_var.get()}", "success")
            else:
                if hasattr(self.controller, 'show_status'):
                    self.controller.show_status("更新资产失败", "error")
                else:
                    messagebox.showerror("错误", "更新资产失败")
        
        # 按钮框架
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=20, side="bottom")  # 固定在底部
        
        ctk.CTkButton(btn_frame, text="保存", command=apply_changes,
                     width=80, height=35).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="取消", command=dialog.destroy,
                     width=80, height=35, fg_color="transparent", 
                     border_width=1).pack(side="right", padx=5)

    def browse_folder(self, folder_var):
        """浏览文件夹"""
        from tkinter import filedialog
        folder = filedialog.askdirectory(title="选择文件夹")
        if folder:
            folder_var.set(folder)

    def browse_file(self, file_var, filetypes):
        """浏览文件"""
        from tkinter import filedialog
        file = filedialog.askopenfilename(title="选择文件", filetypes=filetypes)
        if file:
            file_var.set(file)
    
    def browse_cover_image(self, cover_var):
        """浏览封面图片"""
        from tkinter import filedialog
        file = filedialog.askopenfilename(
            title="选择封面图片",
            filetypes=[("图片文件", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if file:
            cover_var.set(file)

    def remove_asset(self):
        """删除资源"""
        if messagebox.askyesno("确认", "确定要从库中移除这个资源吗？"):
            if self.controller.asset_manager.remove_resource(self.asset):
                self.controller.refresh_content()
                if hasattr(self.controller, 'show_status'):
                    self.controller.show_status("资源已移除", "success")
            else:
                if hasattr(self.controller, 'show_status'):
                    self.controller.show_status("移除资源失败", "error")

    def change_category(self):
        """更改资源分类"""
        # 创建更改分类对话框
        dialog = ctk.CTkToplevel(self.controller.root)
        dialog.title("更改分类")
        dialog.geometry("400x400")
        dialog.transient(self.controller.root)
        dialog.grab_set()
        
        # 居中显示
        DialogUtils.center_window(dialog)
        
        # 创建表单
        form_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # 标题
        title_label = ctk.CTkLabel(form_frame, text=f"更改 '{self.asset.get('name', '未命名')}' 的分类",
                                  font=ctk.CTkFont(size=16, weight="bold"))
        title_label.pack(anchor="w", pady=(0, 20))
        
        # 当前分类显示
        current_category = self.asset.get('category', '未分类')
        current_label = ctk.CTkLabel(form_frame, text=f"当前分类: {current_category}",
                                    font=ctk.CTkFont(size=13))
        current_label.pack(anchor="w", pady=(0, 10))
        
        # 新分类选择
        ctk.CTkLabel(form_frame, text="新分类:", 
                    font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(0, 5))
        
        # 获取可用的分类列表（排除"全部"）
        available_categories = [cat for cat in self.controller.asset_manager.categories if cat != "全部"]
        if not available_categories:
            available_categories = ["未分类"]
            
        category_var = ctk.StringVar(value=current_category)
        category_combo = ctk.CTkComboBox(form_frame, 
                                       variable=category_var,
                                       values=available_categories,
                                       height=35,
                                       font=ctk.CTkFont(size=13))
        category_combo.pack(fill="x", pady=(0, 20))
        
        # 按钮框架 - 修改为 pack 到底部确保可见
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=10, side="bottom")
        
        def apply_change():
            new_category = category_var.get()
            if new_category == current_category:
                dialog.destroy()
                return
                
            # 更新资源分类
            self.asset['category'] = new_category
            if self.controller.asset_manager.save_data():
                dialog.destroy()
                self.controller.refresh_content()
                if hasattr(self.controller, 'show_status'):
                    self.controller.show_status(f"已将 '{self.asset.get('name', '未命名')}' 的分类更改为: {new_category}", "success")
            else:
                if hasattr(self.controller, 'show_status'):
                    self.controller.show_status("更改分类失败", "error")
        
        ctk.CTkButton(btn_frame, text="应用", command=apply_change,
                     width=80).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="取消", command=dialog.destroy,
                     width=80, fg_color="transparent", 
                     border_width=1).pack(side="right", padx=5)

    def browse_folder(self, folder_var):
        """浏览文件夹"""
        from tkinter import filedialog
        folder = filedialog.askdirectory(title="选择文件夹")
        if folder:
            folder_var.set(folder)
