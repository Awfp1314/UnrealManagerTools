import customtkinter as ctk
import os
import threading
from datetime import datetime
from tkinter import messagebox
import webbrowser
from utils.image_utils import ImageUtils
from utils.dialog_utils import DialogUtils
from widgets.search_entry import SearchEntry
from widgets.asset_card import AssetCard

class UEAssetLibraryContent(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=10)
        self.controller = controller
        self.image_utils = ImageUtils()
        self.is_data_loaded = False  # 数据加载状态
        self.last_refresh_time = None  # 上次刷新时间
        # 防抖动计时器
        self._scroll_timer = None
        # 当前正在创建的卡片队列
        self._creating_cards = set()
        # 预创建卡片池
        self._card_pool = {}
        # 上次滚动时间
        self._last_scroll_time = 0
        # 滚动防抖动间隔（毫秒）
        self._debounce_interval = 50
        # 滚动速度相关参数
        self._scroll_speed = 0
        self._last_scroll_pos = 0
        self._scroll_speed_history = []
        self._is_scrolling = False
        
        # 双缓冲相关参数
        self._update_queue = []  # 更新队列
        self._is_updating = False  # 是否正在更新
        self._batch_update_timer = None  # 批量更新计时器
        
        self.create_widgets()
        
        # 后台预加载资源数据
        self.preload_assets_data()
    
    def preload_assets_data(self):
        """后台预加载资源数据"""
        def preload_thread():
            try:
                print(f"🔍 后台加载资源数据...")
                # 触发资源加载
                resources = self.controller.asset_manager.get_resources()
                print(f"✅ 后台资源加载完成，找到 {len(resources)} 个资源")
                
                # 标记数据已加载
                self.is_data_loaded = True
                self.last_refresh_time = datetime.now()
                
            except Exception as e:
                print(f"后台资源加载出错: {e}")
        
        # 在后台线程中执行加载，不影响界面加载速度
        threading.Thread(target=preload_thread, daemon=True).start()

    def create_widgets(self):
        """创建内容区域组件 - 现代化设计"""
        # 内容头部（现代化设计）
        header_frame = ctk.CTkFrame(self, fg_color="transparent", height=100, corner_radius=15)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        # 顶部：标题和资产总数
        top_header = ctk.CTkFrame(header_frame, fg_color="transparent")
        top_header.pack(fill="x", pady=(0, 15))
        
        # 工具名称标题和资产总数
        title_frame = ctk.CTkFrame(top_header, fg_color="transparent")
        title_frame.pack(side="left", fill="y")
        
        self.tool_title = ctk.CTkLabel(title_frame, 
                                      text="虚幻资产库",
                                      font=ctk.CTkFont(size=24, weight="bold"))
        self.tool_title.pack(side="left")
        
        self.asset_count_label = ctk.CTkLabel(title_frame, 
                                             text="",
                                             font=ctk.CTkFont(size=16, weight="bold"),
                                             text_color=("#2563eb", "#60a5fa"))
        self.asset_count_label.pack(side="left", padx=(15, 0))
        
        # 底部：搜索和操作区域
        bottom_header = ctk.CTkFrame(header_frame, fg_color="transparent")
        bottom_header.pack(fill="x")
        
        # 左侧：搜索框
        search_frame = ctk.CTkFrame(bottom_header, fg_color="transparent")
        search_frame.pack(side="left", fill="x", expand=True)
        
        # 搜索框（现代化设计）
        self.search_entry = SearchEntry(search_frame, 
                                       placeholder_text="🔍 搜索资产...",
                                       height=40,
                                       command=self.on_search)
        self.search_entry.pack(side="left", fill="x", expand=True)
        
        # 右侧：操作按钮组
        ops_frame = ctk.CTkFrame(bottom_header, fg_color="transparent")
        ops_frame.pack(side="right", padx=(15, 0))
        
        # 分类下拉框（现代化设计）
        category_frame = ctk.CTkFrame(ops_frame, fg_color="transparent")
        category_frame.pack(side="left", padx=(0, 15))
        
        self.category_var = ctk.StringVar(value="全部")
        self.category_combo = ctk.CTkComboBox(category_frame, 
                                            variable=self.category_var,
                                            values=self.controller.asset_manager.categories,
                                            command=self.on_category_change,
                                            width=150,
                                            height=40,
                                            state="readonly",
                                            font=ctk.CTkFont(size=13),
                                            dropdown_font=ctk.CTkFont(size=13))
        self.category_combo.pack(side="left")
        
        # 使用延迟自动关闭下拉菜单，同时保留悬浮动画
        self.category_combo.bind("<<ComboboxSelected>>", self._start_close_timer)
        self.close_timer = None
        
        # 按钮框架（现代化设计）
        buttons_frame = ctk.CTkFrame(ops_frame, fg_color="transparent")
        buttons_frame.pack(side="left")
        
        # 刷新按钮（现代化设计）
        self.refresh_btn = ctk.CTkButton(buttons_frame, 
                                        text="🔄 刷新",
                                        command=lambda: self.refresh_content(force=True),
                                        height=40,
                                        width=100,
                                        font=ctk.CTkFont(size=13, weight="bold"),
                                        fg_color=("#2563eb", "#3b82f6"),
                                        hover_color=("#1d4ed8", "#2563eb"))
        self.refresh_btn.pack(side="left", padx=5)
        
        # 管理分类按钮（现代化设计）
        self.manage_category_btn = ctk.CTkButton(buttons_frame, 
                                                text="📂 分类",
                                                command=self.show_manage_categories_dialog,
                                                height=40,
                                                width=100,
                                                font=ctk.CTkFont(size=13, weight="bold"),
                                                fg_color=("#8b5cf6", "#a78bfa"),
                                                hover_color=("#7c3aed", "#8b5cf6"))
        self.manage_category_btn.pack(side="left", padx=5)
        
        # 添加资产按钮（现代化设计）
        self.add_btn = ctk.CTkButton(buttons_frame, 
                                    text="➕ 添加",
                                    command=self.import_assets,
                                    height=40,
                                    width=100,
                                    font=ctk.CTkFont(size=13, weight="bold"),
                                    fg_color=("#10b981", "#34d399"),
                                    hover_color=("#059669", "#10b981"))
        self.add_btn.pack(side="left", padx=5)
        
        # 刷新状态提示（现代化设计）
        self.status_frame = ctk.CTkFrame(self, fg_color="transparent", height=40)
        self.status_frame.pack(fill="x", padx=20, pady=(0, 10))
        self.status_frame.pack_propagate(False)
        
        self.status_label = ctk.CTkLabel(self.status_frame, 
                                        text="",
                                        font=ctk.CTkFont(size=13, weight="bold"),
                                        text_color=("gray50", "gray50"))
        self.status_label.pack(side="left")
        
        # 创建资产网格容器 - 现代化背景显示
        self.asset_scrollable = ctk.CTkScrollableFrame(self, 
                                                      fg_color=("gray90", "gray15"),
                                                      corner_radius=15,
                                                      border_width=1,
                                                      border_color=("gray80", "gray20"))
        self.asset_scrollable.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # 启用Canvas的双缓冲优化
        try:
            # 获取底层Canvas
            canvas = self.asset_scrollable._parent_canvas
            # 启用双缓冲渲染模式
            if hasattr(canvas, 'configure'):
                # 在Tkinter中，双缓冲是通过底层的tk.call实现的
                canvas.configure(highlightthickness=0)
                canvas['bd'] = 0
        except Exception as e:
            print(f"启用Canvas双缓冲时出错: {e}")
        
        # 为资产滚动区域绑定鼠标滚轮事件
        self.bind_children_mousewheel(self.asset_scrollable)
    
    def on_search(self, search_term):
        """处理搜索"""
        self.controller.set_search_term(search_term)
        self.refresh_content(force=False)  # 搜索时不强制刷新

    def on_category_change(self, category):
        """处理分类变更"""
        self.controller.set_current_category(category)
        self.refresh_content(force=False)  # 分类变更时不强制刷新
        
    def _start_close_timer(self, event=None):
        """开始下拉菜单自动关闭计时器"""
        # 取消之前的计时器
        if self.close_timer is not None:
            self.after_cancel(self.close_timer)
        
        # 2秒后自动关闭下拉菜单
        self.close_timer = self.after(2000, self._auto_close_dropdown)
        
    def _queue_ui_update(self, update_func, *args, **kwargs):
        """将UI更新任务添加到队列"""
        # 如果组件已被销毁，不执行更新
        if not self.winfo_exists():
            return
        
        # 将更新函数和参数添加到队列
        self._update_queue.append((update_func, args, kwargs))
        
        # 安排批量更新
        self._schedule_batch_update()
        
    def _schedule_batch_update(self):
        """安排批量更新"""
        # 如果已经有更新计划，则不重复安排
        if self._batch_update_timer is not None:
            return
        
        # 安排更新（使用更短的延迟以提高响应速度）
        self._batch_update_timer = self.after(10, self._process_update_queue)
        
    def _process_update_queue(self):
        """处理更新队列，批量执行UI更新"""
        # 重置计时器
        self._batch_update_timer = None
        
        # 如果已经在更新中，则稍后再处理
        if self._is_updating:
            self._schedule_batch_update()
            return
        
        # 标记为正在更新
        self._is_updating = True
        
        try:
            # 限制每批处理的更新数量，避免UI卡顿
            batch_size = 10
            updates_to_process = self._update_queue[:batch_size]
            self._update_queue = self._update_queue[batch_size:]
            
            # 执行更新
            for update_func, args, kwargs in updates_to_process:
                try:
                    update_func(*args, **kwargs)
                except Exception as e:
                    print(f"执行UI更新时出错: {e}")
            
            # 如果还有未处理的更新，继续安排
            if self._update_queue:
                self._schedule_batch_update()
        finally:
            # 标记为更新完成
            self._is_updating = False
        
        # 监听下拉菜单的离开事件
        if hasattr(self.category_combo, '_dropdown_menu') and self.category_combo._dropdown_menu is not None:
            self.category_combo._dropdown_menu.bind("<Leave>", lambda e: self.after(500, self._auto_close_dropdown))
            
    def _auto_close_dropdown(self):
        """自动关闭下拉菜单的方法"""
        if hasattr(self.category_combo, '_dropdown_menu') and self.category_combo._dropdown_menu is not None:
            self.category_combo._dropdown_menu.place_forget()
            self.close_timer = None

    def refresh_content(self, force=False):
        """刷新内容显示 - 智能刷新机制"""
        # 智能刷新判断
        if not force and self.is_data_loaded:
            # 数据已加载且非强制刷新，直接显示现有数据
            print(f"⚡ 快速显示已加载的资源数据")
            self._update_display_only()
            return
        
        # 需要刷新数据
        print(f"🔄 刷新资源数据")
        
        # 显示刷新状态
        self.show_status("正在刷新...", "refresh")
        
        # 更新分类下拉框 - 修复同步问题
        self.update_category_combo()
        
        # 执行分类路径扫描（仅在强制刷新时执行，对全部分类进行扫描）
        if force:
            self.scan_all_category_paths()
        
        # 获取过滤后的资源
        filtered_assets = self.controller.asset_manager.get_filtered_resources(
            self.controller.app_state.current_category, 
            self.controller.app_state.search_term
        )
        
        # 更新资产总数显示
        total_count = len(self.controller.asset_manager.resources)
        filtered_count = len(filtered_assets)
        if total_count == filtered_count:
                self.asset_count_label.configure(text=f"总资源数量: {total_count}")
        else:
                self.asset_count_label.configure(text=f"{filtered_count}/{total_count}")
        
        self.display_assets(filtered_assets)
        
        # 标记数据已加载
        self.is_data_loaded = True
        self.last_refresh_time = datetime.now()
        
        # 显示刷新成功状态
        self.show_status("刷新成功", "success")

    def scan_all_category_paths(self):
        """扫描所有分类路径并添加新资产"""
        # 收集所有新文件夹
        new_folders = []
        
        # 获取现有资源路径集合（用于快速查找）
        existing_paths = {asset['path'] for asset in self.controller.asset_manager.resources}
        
        # 遍历所有分类
        for category in self.controller.asset_manager.categories:
            if category == "全部":
                continue
                
            # 获取分类路径
            paths = self.controller.asset_manager.get_category_paths(category)
            
            if not paths:
                continue
                
            # 扫描每个路径
            for path in paths:
                if not os.path.exists(path):
                    continue
                    
                try:
                    # 遍历路径下的所有文件夹
                    for item in os.listdir(path):
                        item_path = os.path.join(path, item)
                        if os.path.isdir(item_path):
                            # 检查是否已存在
                            if item_path not in existing_paths:
                                new_folders.append({
                                    'name': item,
                                    'path': item_path,
                                    'parent_path': path,
                                    'category': category
                                })
                except Exception as e:
                    print(f"扫描路径 {path} 时出错: {e}")
        
        # 如果有新文件夹，触发添加资产弹窗
        if new_folders:
            self.show_add_new_assets_dialog(new_folders)

    def show_add_new_assets_dialog(self, new_folders):
        """显示添加新资产对话框（批量处理）"""
        if not new_folders:
            return
            
        # 创建批量处理队列
        self.new_folders_queue = new_folders
        self.current_folder_index = 0
        
        # 显示第一个文件夹的添加对话框
        self.show_next_add_asset_dialog()

    def show_next_add_asset_dialog(self):
        """显示下一个添加资产对话框"""
        if self.current_folder_index >= len(self.new_folders_queue):
            # 所有文件夹处理完成，刷新界面
            self.refresh_content()
            return
            
        # 获取当前文件夹
        folder_info = self.new_folders_queue[self.current_folder_index]
        
        # 显示导入对话框（使用文件夹信息）
        self.show_import_dialog_for_new_folder(folder_info)

    def show_import_dialog_for_new_folder(self, folder_info):
        """为新文件夹显示导入对话框"""
        dialog = ctk.CTkToplevel(self.controller.root)
        dialog.title("添加新资产")
        dialog.geometry("500x550")  # 增加高度以确保按钮可见
        dialog.transient(self.controller.root)
        dialog.grab_set()
        dialog.resizable(False, False)  # 设置弹窗为不可由用户自由调整大小
        
        # 居中显示
        DialogUtils.center_window(dialog, self.controller.root)
        
        # 创建表单
        form_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 资源名称
        ctk.CTkLabel(form_frame, text="资源名称:", 
                    font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(0, 5))
        name_var = ctk.StringVar(value=folder_info['name'])
        name_entry = ctk.CTkEntry(form_frame, textvariable=name_var, 
                                 height=35, font=ctk.CTkFont(size=13))
        name_entry.pack(fill="x", pady=(0, 5))
        
        # 添加名称重复提示标签（默认隐藏）
        name_error_label = ctk.CTkLabel(form_frame, text="", 
                                       font=ctk.CTkFont(size=12),
                                       text_color=("red", "red"))
        name_error_label.pack(anchor="w", pady=(0, 10))
        
        # 分类
        ctk.CTkLabel(form_frame, text="分类:", 
                    font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(0, 5))
        category_var = ctk.StringVar(value=folder_info['category'])
        
        # 获取现有分类列表（不包括"全部"）
        category_list = [cat for cat in self.controller.asset_manager.categories if cat != "全部"]
        if not category_list:
            category_list = [folder_info['category']]  # 使用扫描到的分类
            
        # 创建可编辑的组合框，允许用户输入新的分类名称
        category_combo = ctk.CTkComboBox(form_frame, variable=category_var, 
                                       values=category_list,
                                       height=35, font=ctk.CTkFont(size=13),
                                       state="normal")  # 设置为可编辑状态
        category_combo.pack(fill="x", pady=(0, 15))
        
        # 封面图片
        ctk.CTkLabel(form_frame, text="封面图片:", 
                    font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(0, 5))
        cover_var = ctk.StringVar()
        cover_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        cover_frame.pack(fill="x", pady=(0, 15))
        cover_entry = ctk.CTkEntry(cover_frame, textvariable=cover_var,
                                  font=ctk.CTkFont(size=13))
        cover_entry.pack(side="left", fill="x", expand=True)
        
        # 修改浏览按钮，使其打开新文件夹路径而不是分类配置路径
        ctk.CTkButton(cover_frame, text="选择", width=80,
                     command=lambda: self.browse_cover_image_for_new_folder(cover_var, folder_info['path'])).pack(side="right", padx=(5, 0))
        
        # 是否创建README
        readme_var = ctk.BooleanVar(value=False)
        readme_check = ctk.CTkCheckBox(form_frame, text="创建README.md文档",
                                      variable=readme_var,
                                      font=ctk.CTkFont(size=13))
        readme_check.pack(anchor="w", pady=15)
        
        # 添加是否可以导入的选择框
        importable_var = ctk.BooleanVar(value=True)
        importable_check = ctk.CTkCheckBox(form_frame, text="允许导入到虚幻工程",
                                          variable=importable_var,
                                          font=ctk.CTkFont(size=13))
        importable_check.pack(anchor="w", pady=5)
        
        # 按钮框架
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=20, side="bottom")
        
        # 创建导入按钮
        import_button = ctk.CTkButton(btn_frame, text="导入", width=80, height=35)
        import_button.pack(side="left", padx=5)
        
        skip_button = ctk.CTkButton(btn_frame, text="跳过", 
                                   command=lambda: self.skip_current_folder(dialog),
                                   width=80, height=35, fg_color="transparent", 
                                   border_width=1)
        skip_button.pack(side="left", padx=5)
        
        ctk.CTkButton(btn_frame, text="取消", command=lambda: self.cancel_batch_import(dialog),
                     width=80, height=35, fg_color="transparent", 
                     border_width=1).pack(side="right", padx=5)
        
        # 实时检测资源名称是否重复
        def check_name_duplicate(*args):
            """实时检测资源名称是否重复"""
            resource_name = name_var.get().strip()
            # 只有当名称不为空时才检查
            if resource_name:
                existing_resources = [r for r in self.controller.asset_manager.resources if r['name'] == resource_name]
                if existing_resources:
                    # 显示红色错误提示
                    name_error_label.configure(text="资源名称已存在，请使用其他名称")
                    # 禁用导入按钮
                    import_button.configure(state="disabled")
                else:
                    # 清除错误提示
                    name_error_label.configure(text="")
                    # 启用导入按钮
                    import_button.configure(state="normal")
            else:
                # 清除错误提示
                name_error_label.configure(text="")
                # 禁用导入按钮（名称为空时）
                import_button.configure(state="disabled")
        
        # 绑定名称变量的变化事件
        name_var.trace("w", check_name_duplicate)
        
        # 初始化导入按钮状态
        check_name_duplicate()  # 检查初始名称状态
        
        def finalize_import():
            # 检查是否有名称重复错误
            if name_error_label.cget("text"):
                return  # 如果有错误，不执行导入操作
            
            # 获取用户输入的分类名称
            category = category_var.get()
            if not category:
                self.show_status("请输入或选择分类", "error")
                return
                
            # 检查分类是否已存在，如果不存在则创建新分类
            if category not in self.controller.asset_manager.categories:
                if not self.controller.asset_manager.add_category(category):
                    self.show_status("添加分类失败", "error")
                    return
            
            # 再次检查资源名称是否重复（防止在输入过程中有其他操作）
            resource_name = name_var.get()
            existing_resources = [r for r in self.controller.asset_manager.resources if r['name'] == resource_name]
            if existing_resources:
                # 在对话框中显示红色错误提示
                name_error_label.configure(text="资源名称已存在，请使用其他名称")
                # 禁用导入按钮
                import_button.configure(state="disabled")
                return
            
            # 添加资源并设置importable字段
            if self.controller.asset_manager.add_resource(name_var.get(), folder_info['path'], category, 
                                             cover_var.get(), readme_var.get()):
                # 更新刚添加的资源，添加importable字段
                if self.controller.asset_manager.resources:
                    latest_asset = self.controller.asset_manager.resources[-1]
                    latest_asset['importable'] = importable_var.get()
                    self.controller.asset_manager.save_data()
                
                dialog.destroy()
                self.show_status(f"资源导入成功: {name_var.get()}", "success")
                
                # 如果勾选了创建README，则自动打开README.md文件
                if readme_var.get():
                    doc_path = os.path.join(folder_info['path'], "README.md")
                    if os.path.exists(doc_path):
                        try:
                            os.startfile(doc_path)
                        except Exception as e:
                            print(f"打开README文件失败: {e}")
                
                # 处理下一个文件夹
                self.current_folder_index += 1
                self.show_next_add_asset_dialog()
            else:
                self.show_status("资源导入失败", "error")
        
        # 绑定导入按钮的命令
        import_button.configure(command=finalize_import)

    def skip_current_folder(self, dialog):
        """跳过当前文件夹"""
        dialog.destroy()
        self.current_folder_index += 1
        self.show_next_add_asset_dialog()

    def cancel_batch_import(self, dialog):
        """取消批量导入"""
        dialog.destroy()
        self.new_folders_queue = []
        self.current_folder_index = 0
        self.refresh_content()

    def _update_display_only(self):
        """仅更新显示，不重新加载数据"""
        try:
            # 获取过滤后的资源
            filtered_assets = self.controller.asset_manager.get_filtered_resources(
                self.controller.app_state.current_category, 
                self.controller.app_state.search_term
            )
            
            # 更新资产总数显示
            total_count = len(self.controller.asset_manager.resources)
            filtered_count = len(filtered_assets)
            if total_count == filtered_count:
                self.asset_count_label.configure(text=f"共 {total_count} 个资源")
            else:
                self.asset_count_label.configure(text=f"共 {filtered_count}/{total_count} 个资源")
            
            self.display_assets(filtered_assets)
            
        except Exception as e:
            print(f"更新显示出错: {e}")
            # 出错时回退到完整刷新
            self.refresh_content(force=True)

    def update_category_combo(self):
        """更新分类下拉框"""
        # 获取当前选中的分类
        current_selection = self.category_var.get()
        
        # 更新下拉框的值
        self.category_combo.configure(values=self.controller.asset_manager.categories)
        
        # 如果当前选中的分类仍然存在，保持选中状态
        if current_selection in self.controller.asset_manager.categories:
            self.category_var.set(current_selection)
        else:
            # 否则选择"全部"
            self.category_var.set("全部")
            self.controller.set_current_category("全部")

    def show_status(self, message, status_type="info"):
        """显示状态信息"""
        colors = {
            "info": ("gray50", "gray50"),
            "success": ("green", "lightgreen"),
            "error": ("red", "lightcoral"),
            "refresh": ("blue", "lightblue")
        }
        
        color = colors.get(status_type, colors["info"])
        self.status_label.configure(text=message, text_color=color)
        
        # 如果是成功状态，3秒后清除
        if status_type == "success":
            self.after(3000, lambda: self.status_label.configure(text=""))

    def display_assets(self, assets):
        """显示资产列表 - 根据资产数量决定使用一次性加载还是懒加载"""
        # 清空现有显示
        for widget in self.asset_scrollable.winfo_children():
            widget.destroy()
        
        if not assets:
            # 创建美化的空状态显示
            empty_container = ctk.CTkFrame(self.asset_scrollable, 
                                          fg_color="transparent",
                                          height=400)
            empty_container.pack(fill="both", expand=True, pady=50)
            empty_container.pack_propagate(False)
            
            # 空状态图标和文本
            empty_icon = ctk.CTkLabel(empty_container, 
                                     text="📦",
                                     font=ctk.CTkFont(size=48))
            empty_icon.pack(pady=(80, 10))
            
            empty_label = ctk.CTkLabel(empty_container, 
                                      text="暂无匹配的资源",
                                      font=ctk.CTkFont(size=16, weight="bold"),
                                      text_color=("gray50", "gray50"))
            empty_label.pack(pady=(0, 5))
            
            # 提示文本
            tip_label = ctk.CTkLabel(empty_container, 
                                    text="点击「+ 添加资产」按钮来导入新的资源",
                                    font=ctk.CTkFont(size=12),
                                    text_color=("gray40", "gray60"))
            tip_label.pack(pady=(0, 20))
            
            # 添加快捷按钮
            quick_add_btn = ctk.CTkButton(empty_container,
                                         text="📎 立即添加资产",
                                         command=self.import_assets,
                                         height=40,
                                         width=150,
                                         font=ctk.CTkFont(size=13))
            quick_add_btn.pack(pady=10)
            return
        
        # 设置懒加载阈值 - 降低阈值，让更多情况下使用一次性加载
        LAZY_LOAD_THRESHOLD = 50
        
        # 根据资产数量决定使用哪种加载方式
        if len(assets) <= LAZY_LOAD_THRESHOLD:
            # 资产数量不多，一次性加载所有卡片
            self.create_simple_layout(assets)
        else:
            # 资产数量较多，使用懒加载
            self.create_lazy_loading_layout(assets)

    def show_manage_categories_dialog(self):
        """显示管理分类对话框 - 修改了窗口大小"""
        dialog = ctk.CTkToplevel(self.controller.root)
        dialog.title("管理分类")
        # 修改窗口大小：宽度x高度（增加高度以确保按钮可见）
        dialog.geometry("600x550")  # 增加窗口高度
        dialog.transient(self.controller.root)
        dialog.grab_set()
        dialog.resizable(False, False)  # 设置弹窗为不可由用户自由调整大小
        
        # 居中显示
        DialogUtils.center_window(dialog, self.controller.root)
        
        # 创建主框架
        main_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 标题
        title_label = ctk.CTkLabel(main_frame, text="分类管理",
                                  font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(anchor="w", pady=(0, 20))
        
        # 分类列表框架
        list_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        list_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # 分类列表标题
        list_title_frame = ctk.CTkFrame(list_frame, fg_color="transparent")
        list_title_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(list_title_frame, text="现有分类:",
                    font=ctk.CTkFont(size=14, weight="bold")).pack(side="left")
        
        # 分类列表
        self.categories_scrollable = ctk.CTkScrollableFrame(list_frame, height=250)  # 增加高度
        self.categories_scrollable.pack(fill="both", expand=True)
        
        # 加载分类列表
        self.category_widgets = {}
        categories = [cat for cat in self.controller.asset_manager.categories if cat != "全部"]
        
        for category in categories:
            self.create_category_item(self.categories_scrollable, category)
        
        # 添加分类框架
        add_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        add_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(add_frame, text="添加新分类:",
                    font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", pady=(0, 10))
        
        add_input_frame = ctk.CTkFrame(add_frame, fg_color="transparent")
        add_input_frame.pack(fill="x")
        
        self.new_category_var = ctk.StringVar()
        new_category_entry = ctk.CTkEntry(add_input_frame, 
                                         textvariable=self.new_category_var,
                                         placeholder_text="输入新分类名称",
                                         height=35,
                                         font=ctk.CTkFont(size=13))
        new_category_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        add_btn = ctk.CTkButton(add_input_frame, 
                               text="添加",
                               command=lambda: self.add_category_from_dialog(),
                               height=35,
                               width=80,
                               font=ctk.CTkFont(size=13))
        add_btn.pack(side="right")
        
        # 按钮框架
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        close_btn = ctk.CTkButton(btn_frame, 
                                 text="关闭",
                                 command=dialog.destroy,
                                 height=35,
                                 width=80,
                                 font=ctk.CTkFont(size=13))
        close_btn.pack(side="right")

    def create_category_item(self, parent, category):
        """创建分类列表项"""
        item_frame = ctk.CTkFrame(parent, fg_color="transparent")
        item_frame.pack(fill="x", pady=5)
        
        # 分类名称
        name_label = ctk.CTkLabel(item_frame, 
                                 text=category,
                                 font=ctk.CTkFont(size=13))
        name_label.pack(side="left", fill="x", expand=True)
        
        # 删除按钮 - 对于默认分类禁用删除按钮
        if category == "默认":
            # 默认分类不可删除，显示为禁用状态
            delete_btn = ctk.CTkButton(item_frame,
                                      text="删除",
                                      state="disabled",  # 禁用按钮
                                      width=60,
                                      height=30,
                                      font=ctk.CTkFont(size=12),
                                      fg_color="gray")  # 灰色表示禁用
        else:
            # 其他分类可以删除
            delete_btn = ctk.CTkButton(item_frame,
                                      text="删除",
                                      command=lambda: self.delete_category(category, item_frame),
                                      width=60,
                                      height=35,  # 增加按钮高度
                                      font=ctk.CTkFont(size=12),
                                      fg_color="#d9534f",
                                      hover_color="#c9302c")
        delete_btn.pack(side="right", padx=(5, 0))
        
        # 保存引用以便后续删除
        self.category_widgets[category] = {
            "frame": item_frame,
            "label": name_label,
            "button": delete_btn
        }

    def add_category_from_dialog(self):
        """从对话框添加分类"""
        category_name = self.new_category_var.get().strip()
        if not category_name:
            self.show_status("请输入分类名称", "error")
            return
            
        if category_name in self.controller.asset_manager.categories:
            self.show_status("分类已存在", "error")
            return
            
        if self.controller.asset_manager.add_category(category_name):
            # 清空输入框
            self.new_category_var.set("")
            
            # 添加新分类到列表
            self.create_category_item(self.categories_scrollable, category_name)
            
            # 刷新主界面
            self.update_category_combo()
            self.show_status(f"已添加分类: {category_name}", "success")
        else:
            self.show_status("添加分类失败", "error")

    def delete_category(self, category, item_frame):
        """删除分类"""
        # 默认分类不可删除
        if category == "默认":
            self.show_status("默认分类不可删除", "error")
            return
            
        # 检查是否有资源使用此分类
        resources_in_category = [r for r in self.controller.asset_manager.resources 
                                if r.get('category') == category]
        
        if resources_in_category:
            self.show_status(f"分类 '{category}' 中有 {len(resources_in_category)} 个资源，无法删除", "error")
            return
            
        if messagebox.askyesno("确认删除", f"确定要删除分类 '{category}' 吗？"):
            # 从数据管理器中删除
            if category in self.controller.asset_manager.categories:
                self.controller.asset_manager.categories.remove(category)
                self.controller.asset_manager.save_data()
                
                # 从UI中删除
                item_frame.destroy()
                if category in self.category_widgets:
                    del self.category_widgets[category]
                
                # 刷新主界面 - 确保下拉框同步更新
                self.update_category_combo()
                self.show_status(f"已删除分类: {category}", "success")

    # 其他方法保持不变...
    def import_assets(self):
        """导入资产"""
        from tkinter import filedialog
        path = filedialog.askdirectory(title="选择资源文件夹")
        if path:
            self.show_import_dialog(path)

    def show_import_dialog(self, path):
        """显示导入对话框"""
        dialog = ctk.CTkToplevel(self.controller.root)
        dialog.title("导入资源")
        dialog.geometry("500x550")  # 增加高度以确保按钮可见
        dialog.transient(self.controller.root)
        dialog.grab_set()
        dialog.resizable(False, False)  # 设置弹窗为不可由用户自由调整大小
        
        # 居中显示
        DialogUtils.center_window(dialog, self.controller.root)
        
        # 创建表单
        form_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 资源名称
        ctk.CTkLabel(form_frame, text="资源名称:", 
                    font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(0, 5))
        import os
        default_name = os.path.basename(path)
        name_var = ctk.StringVar(value=default_name)
        name_entry = ctk.CTkEntry(form_frame, textvariable=name_var, 
                                 height=35, font=ctk.CTkFont(size=13))
        name_entry.pack(fill="x", pady=(0, 5))
        
        # 添加名称重复提示标签（默认隐藏）
        name_error_label = ctk.CTkLabel(form_frame, text="", 
                                       font=ctk.CTkFont(size=12),
                                       text_color=("red", "red"))
        name_error_label.pack(anchor="w", pady=(0, 10))
        
        # 分类
        ctk.CTkLabel(form_frame, text="分类:", 
                    font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(0, 5))
        category_var = ctk.StringVar(value="默认")
        
        # 获取现有分类列表（不包括"全部"）
        category_list = [cat for cat in self.controller.asset_manager.categories if cat != "全部"]
        if not category_list:
            category_list = ["默认"]
            
        # 创建可编辑的组合框，允许用户输入新的分类名称
        category_combo = ctk.CTkComboBox(form_frame, variable=category_var, 
                                       values=category_list,
                                       height=35, font=ctk.CTkFont(size=13),
                                       state="normal")  # 设置为可编辑状态
        category_combo.pack(fill="x", pady=(0, 15))
        
        # 封面图片
        ctk.CTkLabel(form_frame, text="封面图片:", 
                    font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(0, 5))
        cover_var = ctk.StringVar()
        cover_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        cover_frame.pack(fill="x", pady=(0, 15))
        cover_entry = ctk.CTkEntry(cover_frame, textvariable=cover_var,
                                  font=ctk.CTkFont(size=13))
        cover_entry.pack(side="left", fill="x", expand=True)
        
        ctk.CTkButton(cover_frame, text="选择", width=80,
                     command=lambda: self.browse_cover_image(cover_var)).pack(side="right", padx=(5, 0))
        
        # 是否创建README
        readme_var = ctk.BooleanVar(value=False)
        readme_check = ctk.CTkCheckBox(form_frame, text="创建README.md文档",
                                      variable=readme_var,
                                      font=ctk.CTkFont(size=13))
        readme_check.pack(anchor="w", pady=15)
        
        # 添加是否可以导入的选择框
        importable_var = ctk.BooleanVar(value=True)
        importable_check = ctk.CTkCheckBox(form_frame, text="允许导入到虚幻工程",
                                          variable=importable_var,
                                          font=ctk.CTkFont(size=13))
        importable_check.pack(anchor="w", pady=5)
        
        # 按钮框架
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=20, side="bottom")  # 固定在底部
        
        # 创建导入按钮
        import_button = ctk.CTkButton(btn_frame, text="导入", width=80, height=35)
        import_button.pack(side="left", padx=5)
        
        ctk.CTkButton(btn_frame, text="取消", command=dialog.destroy,
                     width=80, height=35).pack(side="right", padx=5)
        
        # 实时检测资源名称是否重复
        def check_name_duplicate(*args):
            """实时检测资源名称是否重复"""
            resource_name = name_var.get().strip()
            if resource_name:  # 只有当名称不为空时才检查
                existing_resources = [r for r in self.controller.asset_manager.resources if r['name'] == resource_name]
                if existing_resources:
                    # 显示红色错误提示
                    name_error_label.configure(text="资源名称已存在，请使用其他名称")
                    # 禁用导入按钮
                    import_button.configure(state="disabled")
                else:
                    # 清除错误提示
                    name_error_label.configure(text="")
                    # 启用导入按钮
                    import_button.configure(state="normal")
            else:
                # 清除错误提示
                name_error_label.configure(text="")
                # 禁用导入按钮（名称为空时）
                import_button.configure(state="disabled")
        
        # 绑定名称变量的变化事件
        name_var.trace("w", check_name_duplicate)
        
        # 初始化导入按钮状态
        check_name_duplicate()  # 检查初始名称状态
        
        def finalize_import():
            # 检查是否有名称重复错误
            if name_error_label.cget("text"):
                return  # 如果有错误，不执行导入操作
            
            # 获取用户输入的分类名称
            category = category_var.get()
            if not category:
                self.show_status("请输入或选择分类", "error")
                return
                
            # 检查分类是否已存在，如果不存在则创建新分类
            if category not in self.controller.asset_manager.categories:
                if not self.controller.asset_manager.add_category(category):
                    self.show_status("添加分类失败", "error")
                    return
            
            # 再次检查资源名称是否重复（防止在输入过程中有其他操作）
            resource_name = name_var.get()
            existing_resources = [r for r in self.controller.asset_manager.resources if r['name'] == resource_name]
            if existing_resources:
                # 在对话框中显示红色错误提示
                name_error_label.configure(text="资源名称已存在，请使用其他名称")
                # 禁用导入按钮
                import_button.configure(state="disabled")
                return
            
            # 添加资源并设置importable字段
            if self.controller.asset_manager.add_resource(name_var.get(), path, category, 
                                             cover_var.get(), readme_var.get()):
                # 更新刚添加的资源，添加importable字段
                if self.controller.asset_manager.resources:
                    latest_asset = self.controller.asset_manager.resources[-1]
                    latest_asset['importable'] = importable_var.get()
                    self.controller.asset_manager.save_data()
                
                self.refresh_content()
                dialog.destroy()
                self.show_status(f"资源导入成功: {name_var.get()}", "success")
                
                # 如果勾选了创建README，则自动打开README.md文件
                if readme_var.get():
                    doc_path = os.path.join(path, "README.md")
                    if os.path.exists(doc_path):
                        try:
                            os.startfile(doc_path)
                        except Exception as e:
                            print(f"打开README文件失败: {e}")
            else:
                self.show_status("资源导入失败", "error")
        
        # 绑定导入按钮的命令
        import_button.configure(command=finalize_import)

    def browse_cover_image_for_new_folder(self, cover_var, folder_path):
        """为新文件夹浏览封面图片"""
        from tkinter import filedialog
        # 设置初始目录为新文件夹路径
        file = filedialog.askopenfilename(
            title="选择封面图片",
            initialdir=folder_path,  # 设置初始目录为新文件夹路径
            filetypes=[("图片文件", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if file:
            cover_var.set(file)

    def browse_cover_image(self, cover_var):
        """浏览封面图片"""
        from tkinter import filedialog
        file = filedialog.askopenfilename(
            title="选择封面图片",
            filetypes=[("图片文件", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if file:
            cover_var.set(file)

    def create_simple_layout(self, assets):
        """创建简单的4列布局 - 一次性加载所有资产卡片"""
        # 使用队列来处理UI更新，避免阻塞
        self._queue_ui_update(lambda a=assets: self._do_create_simple_layout(a))
        
    def _do_create_simple_layout(self, assets):
        """实际创建简单布局的内部方法"""
        # 卡片参数
        card_width = 180
        card_height = 260
        card_margin = 15
        cards_per_row = 4  # 固定4列
        
        # 如果资产数量较少，添加一些视觉引导
        if len(assets) <= 4:
            # 添加提示信息
            info_frame = ctk.CTkFrame(self.asset_scrollable, 
                                     fg_color=("gray90", "gray25"),
                                     corner_radius=8,
                                     height=50)
            info_frame.pack(fill="x", padx=10, pady=(10, 15))
            info_frame.pack_propagate(False)
            
            info_label = ctk.CTkLabel(info_frame, 
                                     text=f"当前显示 {len(assets)} 个资源",
                                     font=ctk.CTkFont(size=12),
                                     text_color=("gray60", "gray70"))
            info_label.pack(expand=True)
        
        # 创建资产卡片 - 一次性加载所有卡片
        current_row = None
        for i, asset in enumerate(assets):
            if i % cards_per_row == 0:
                current_row = ctk.CTkFrame(self.asset_scrollable, fg_color="transparent")
                current_row.pack(fill="x", padx=10, pady=8)
            
            # 创建固定尺寸的卡片容器
            card_container = ctk.CTkFrame(current_row, 
                                        fg_color="transparent", 
                                        width=card_width, 
                                        height=card_height)
            card_container.pack(side="left", padx=card_margin//2, pady=5)
            card_container.pack_propagate(False)  # 防止容器自适应内容大小
            
            # 创建卡片
            card = AssetCard(card_container, asset, self.controller, self.image_utils)
            card.pack(fill="both", expand=True)
        
        # 如果资产数量较少，在底部添加一些装饰性内容
        if len(assets) <= 8:
            # 添加底部间距，避免卡片贴边
            spacer_frame = ctk.CTkFrame(self.asset_scrollable, 
                                       fg_color="transparent",
                                       height=100)
            spacer_frame.pack(fill="x", pady=20)
            
            # 添加一些友好的提示
            tips_frame = ctk.CTkFrame(spacer_frame, 
                                     fg_color=("gray92", "gray20"),
                                     corner_radius=8)
            tips_frame.pack(fill="x", padx=50, pady=10)
            
            tips_title = ctk.CTkLabel(tips_frame, 
                                     text="💡 使用提示",
                                     font=ctk.CTkFont(size=13, weight="bold"),
                                     text_color=("#2563eb", "#60a5fa"))
            tips_title.pack(anchor="w", padx=15, pady=(10, 5))
            
            tips_content = ctk.CTkLabel(tips_frame, 
                                       text="• 点击「添加资产」按钮可导入新资源\n• 使用搜索框快速查找特定资源\n• 可以自定义分类管理资源\n• 点击资源卡片查看详情", 
                                       font=ctk.CTkFont(size=11),
                                       text_color=("gray60", "gray70"),
                                       justify="left")
            tips_content.pack(anchor="w", padx=15, pady=(0, 10))
            
    def create_lazy_loading_layout(self, assets):
        """创建懒加载布局 - 仅加载可视区域内的资产卡片"""
        # 使用队列来处理UI更新，避免阻塞
        self._queue_ui_update(lambda a=assets: self._do_create_lazy_loading_layout(a))
        
    def _do_create_lazy_loading_layout(self, assets):
        """实际创建懒加载布局的内部方法"""
        # 卡片参数
        self.card_width = 180
        self.card_height = 260
        self.card_margin = 15
        self.cards_per_row = 4  # 固定4列
        self.assets = assets
        
        # 保存当前加载状态
        self.loaded_indices = set()
        # 保存卡片引用，用于动画和管理
        self.card_refs = {}
        # 保存骨架屏引用
        self.skeleton_refs = {}
        
        # 计算滚动区域总高度
        total_rows = (len(assets) + self.cards_per_row - 1) // self.cards_per_row
        self.total_height = total_rows * (self.card_height + 16) + 100  # 16是行间距，100是底部间距
        
        # 创建一个容器来放置所有卡片
        self.cards_container = ctk.CTkFrame(self.asset_scrollable, fg_color="transparent")
        self.cards_container.pack(fill="both", expand=True)
        self.cards_container.configure(height=self.total_height)
        
        # 添加提示信息
        info_frame = ctk.CTkFrame(self.asset_scrollable, 
                                 fg_color=("gray90", "gray25"),
                                 corner_radius=8,
                                 height=50)
        info_frame.pack(fill="x", padx=10, pady=(10, 15))
        info_frame.pack_propagate(False)
        
        info_label = ctk.CTkLabel(info_frame, 
                                 text=f"当前显示 {len(assets)} 个资源，使用懒加载优化性能",
                                 font=ctk.CTkFont(size=12),
                                 text_color=("gray60", "gray70"))
        info_label.pack(expand=True)
        
        # 绑定滚动事件，用于懒加载
        self.asset_scrollable._parent_canvas.bind("<Configure>", self.on_canvas_configure)
        self.asset_scrollable._parent_canvas.bind("<MouseWheel>", self.on_lazy_loading_mousewheel)
        # 添加滚动事件监听滚动状态
        self.asset_scrollable._parent_canvas.bind("<Motion>", self.on_mouse_motion)
        
        # 初始加载可见区域的卡片
        self.load_visible_cards()
        
    def on_canvas_configure(self, event):
        """当画布大小改变时触发"""
        self.load_visible_cards()
        
    def on_lazy_loading_mousewheel(self, event):
        """处理懒加载模式下的鼠标滚轮事件"""
        # 获取当前滚动位置
        canvas = self.asset_scrollable._parent_canvas
        current_scroll_pos = canvas.yview()[0] * self.total_height
        
        # 计算滚动速度
        if self._last_scroll_pos > 0:
            scroll_delta = abs(current_scroll_pos - self._last_scroll_pos)
            # 添加到速度历史记录
            self._scroll_speed_history.append(scroll_delta)
            # 只保留最近的5个速度样本
            if len(self._scroll_speed_history) > 5:
                self._scroll_speed_history.pop(0)
            # 计算平均速度
            self._scroll_speed = sum(self._scroll_speed_history) / len(self._scroll_speed_history)
        
        # 更新最后滚动位置
        self._last_scroll_pos = current_scroll_pos
        self._is_scrolling = True
        
        # 获取资产卡片的高度（包括边距）
        card_height = 260  # 卡片高度
        card_margin = 15   # 卡片间距
        # 计算两个卡片的高度距离
        target_scroll_distance = 2 * (card_height + card_margin)  # 550像素
        
        # 动态调整滚动放大系数：速度越快，放大系数越小
        base_amplification = 1.5
        if self._scroll_speed > 100:  # 快速滚动
            scroll_amplification = base_amplification * 0.7
        elif self._scroll_speed > 50:  # 中等速度
            scroll_amplification = base_amplification * 0.9
        else:  # 慢速滚动
            scroll_amplification = base_amplification
        
        # 应用放大系数
        adjusted_scroll_distance = target_scroll_distance * scroll_amplification
        
        # 计算滚动单位数（每个单位大约是20像素）
        scroll_units = int(adjusted_scroll_distance / 20)
        
        # 根据滚轮方向滚动
        if event.delta > 0:
            # 向上滚动
            self.asset_scrollable._parent_canvas.yview_scroll(-scroll_units, "units")
        else:
            # 向下滚动
            self.asset_scrollable._parent_canvas.yview_scroll(scroll_units, "units")
        
        # 使用防抖动方式加载可见区域的卡片
        self._debounced_load_visible_cards()
        
        # 设置滚动停止检测计时器
        self.after(200, self._check_scroll_stopped)
        
        # 阻止事件继续传播，避免其他组件处理
        return "break"
        
    def _debounced_load_visible_cards(self):
        """使用防抖动机制加载可见区域的卡片"""
        # 取消之前的计时器
        if self._scroll_timer:
            self.after_cancel(self._scroll_timer)
            
        # 根据滚动速度动态调整防抖动延迟
        if self._scroll_speed > 100:  # 快速滚动时，增加延迟，减少不必要的加载
            delay = self._debounce_interval * 3
        elif self._scroll_speed > 50:  # 中等速度
            delay = self._debounce_interval * 2
        else:  # 慢速滚动或停止
            delay = self._debounce_interval
        
        # 设置新的计时器
        self._scroll_timer = self.after(delay, self.load_visible_cards)
            
    def _check_scroll_stopped(self):
        """检查滚动是否停止"""
        current_scroll_pos = self.asset_scrollable._parent_canvas.yview()[0] * self.total_height
        if abs(current_scroll_pos - self._last_scroll_pos) < 5:  # 位置变化小于5像素认为已停止
            self._is_scrolling = False
            # 滚动停止后，确保所有可见卡片都已加载
            self.load_visible_cards()
            # 为所有已加载但未显示动画的卡片添加淡入效果
            self._animate_visible_cards()
        else:
            self._last_scroll_pos = current_scroll_pos
            self.after(100, self._check_scroll_stopped)
    
    def on_mouse_motion(self, event):
        """处理鼠标移动事件，用于检测交互状态"""
        pass
    
    def load_visible_cards(self):
        """加载可视区域内的资产卡片"""
        # 更新最后滚动时间
        self._last_scroll_time = self.winfo_exists() and self.after_idle(lambda: 0) or 0
        
        # 获取滚动条的当前位置
        canvas = self.asset_scrollable._parent_canvas
        try:
            scroll_x, scroll_y = canvas.xview()[0], canvas.yview()[0]
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()
        except:
            # 如果获取画布信息失败，直接返回
            return
        
        # 根据滚动速度动态调整预加载范围
        if self._scroll_speed > 100:  # 快速滚动时，缩小预加载范围
            preload_margin = 400  # 像素
            preload_rows = 1  # 行数
        elif self._scroll_speed > 50:  # 中等速度
            preload_margin = 600  # 像素
            preload_rows = 2  # 行数
        else:  # 慢速滚动或停止
            preload_margin = 800  # 像素
            preload_rows = 3  # 行数
        
        # 计算可见区域的上下边界
        visible_top = scroll_y * self.total_height
        visible_bottom = visible_top + canvas_height + preload_margin
        
        # 计算可见区域的行范围
        row_height = self.card_height + 16  # 卡片高度 + 行间距
        start_row = max(0, int(visible_top / row_height) - preload_rows)
        end_row = min((len(self.assets) + self.cards_per_row - 1) // self.cards_per_row, 
                     int(visible_bottom / row_height) + preload_rows)
        
        # 记录需要加载的卡片索引
        cards_to_load = []
        for row in range(start_row, end_row):
            for col in range(self.cards_per_row):
                index = row * self.cards_per_row + col
                if index >= len(self.assets):
                    break
                
                if index not in self.loaded_indices and index not in self._creating_cards:
                    cards_to_load.append((index, row, col))
        
        # 按顺序加载卡片，减少异步创建导致的混乱
        for i, (index, row, col) in enumerate(cards_to_load):
            self._creating_cards.add(index)
            # 使用队列添加骨架屏
            self._queue_ui_update(self._show_skeleton_at_position, index, row, col)
            # 根据加载顺序调整延迟时间
            delay = i * 8  # 每个卡片延迟8ms创建，比之前稍慢但更平滑
            self.after(delay, lambda idx=index, r=row, c=col: self._queue_ui_update(self.create_card_at_position, idx, r, c))
            self.loaded_indices.add(index)
    
    def _show_skeleton_at_position(self, index, row, col):
        """在指定位置显示骨架屏"""
        # 检查行框架是否存在，如果不存在则创建
        row_frame = None
        
        # 查找现有的行框架
        for child in self.cards_container.winfo_children():
            if hasattr(child, "_row_id") and child._row_id == row:
                row_frame = child
                break
        
        # 如果行框架不存在，创建新的
        if not row_frame:
            row_frame = ctk.CTkFrame(self.cards_container, fg_color="transparent")
            row_frame.pack(fill="x", padx=10, pady=8)
            row_frame._row_id = row
        
        # 创建固定尺寸的卡片容器
        skeleton_container = ctk.CTkFrame(row_frame, 
                                        fg_color=("gray85", "gray30"), 
                                        width=self.card_width, 
                                        height=self.card_height, 
                                        corner_radius=8)
        skeleton_container.pack(side="left", padx=self.card_margin//2, pady=5)
        skeleton_container.pack_propagate(False)  # 防止容器自适应内容大小
        
        # 添加骨架屏内容
        # 图片区域骨架
        image_skeleton = ctk.CTkFrame(skeleton_container, 
                                    fg_color=("gray75", "gray40"), 
                                    height=150, 
                                    corner_radius=4)
        image_skeleton.pack(fill="x", padx=10, pady=(10, 8))
        
        # 标题区域骨架
        title_skeleton = ctk.CTkFrame(skeleton_container, 
                                    fg_color=("gray75", "gray40"), 
                                    height=18, 
                                    corner_radius=4)
        title_skeleton.pack(fill="x", padx=10, pady=(0, 6))
        title_skeleton.configure(width=int(self.card_width * 0.8))
        
        # 描述区域骨架
        desc_skeleton = ctk.CTkFrame(skeleton_container, 
                                    fg_color=("gray75", "gray40"), 
                                    height=14, 
                                    corner_radius=4)
        desc_skeleton.pack(fill="x", padx=10, pady=(0, 6))
        desc_skeleton.configure(width=int(self.card_width * 0.6))
        
        # 保存骨架屏引用
        self.skeleton_refs[index] = skeleton_container
    
    def _animate_visible_cards(self):
        """为可见区域的卡片添加淡入动画效果"""
        # 将动画任务添加到队列，避免阻塞UI
        for index, card in self.card_refs.items():
            # 检查卡片是否在可视区域内
            if self._is_card_visible(index):
                # 如果卡片还没有动画过，则添加动画
                if not hasattr(card, "_animated") or not card._animated:
                    # 使用队列添加淡入动画
                    self._queue_ui_update(lambda c=card: self._fade_in_card(c))
                    card._animated = True
    
    def _is_card_visible(self, index):
        """检查卡片是否在可视区域内"""
        canvas = self.asset_scrollable._parent_canvas
        try:
            scroll_y = canvas.yview()[0]
            canvas_height = canvas.winfo_height()
        except:
            return False
        
        # 计算卡片位置
        row = index // self.cards_per_row
        row_height = self.card_height + 16
        card_top = row * row_height
        card_bottom = card_top + self.card_height
        
        # 计算可见区域
        visible_top = scroll_y * self.total_height
        visible_bottom = visible_top + canvas_height + 200  # 稍微扩大可见区域
        
        # 检查卡片是否与可见区域重叠
        return not (card_bottom < visible_top or card_top > visible_bottom)
    
    def _fade_in_card(self, card):
        """为卡片添加淡入动画"""
        # 设置初始透明度（在CTk中通过改变颜色实现类似效果）
        if hasattr(card, "configure"):
            # 记录原始颜色
            original_fg = card.cget("fg_color")
            # 初始颜色设置为更透明的版本
            if isinstance(original_fg, tuple):  # 暗黑模式和亮色模式
                light_color = original_fg[0]
                dark_color = original_fg[1]
                # 动画函数
                def animate_opacity(step=0):
                    if step <= 10:
                        # 计算当前透明度对应的颜色
                        # 在CTk中没有直接的透明度控制，这里通过改变颜色深浅模拟
                        card.configure(fg_color=original_fg)
                        # 移动卡片位置模拟上移动画
                        card.place_configure(y=-5 + step * 0.5) if hasattr(card, "place_configure") else None
                        step += 1
                        self.after(15, lambda: animate_opacity(step))
                    else:
                        card._animated = True
                
                animate_opacity()
        
    def create_card_at_position(self, index, row, col):
        """在指定位置创建资产卡片"""
        # 从创建队列中移除
        if index in self._creating_cards:
            self._creating_cards.remove(index)
        
        # 检查索引是否有效
        if index >= len(self.assets):
            return
        
        asset = self.assets[index]
        
        # 检查行框架是否存在，如果不存在则创建
        row_frame = None
        
        # 查找现有的行框架
        for child in self.cards_container.winfo_children():
            if hasattr(child, "_row_id") and child._row_id == row:
                row_frame = child
                break
        
        # 如果行框架不存在，创建新的
        if not row_frame:
            row_frame = ctk.CTkFrame(self.cards_container, fg_color="transparent")
            row_frame.pack(fill="x", padx=10, pady=8)
            row_frame._row_id = row
        
        # 移除对应的骨架屏（如果存在）
        if index in self.skeleton_refs:
            try:
                skeleton = self.skeleton_refs[index]
                # 找到骨架屏在父容器中的位置
                skeleton_index = None
                for i, child in enumerate(row_frame.winfo_children()):
                    if child == skeleton:
                        skeleton_index = i
                        break
                
                if skeleton_index is not None:
                    # 先隐藏骨架屏，避免闪烁
                    skeleton.pack_forget()
                    # 稍后再销毁骨架屏，给新卡片足够的时间显示
                    self.after(200, lambda s=skeleton: s.destroy() if s.winfo_exists() else None)
                    # 从引用字典中移除
                    del self.skeleton_refs[index]
            except Exception as e:
                print(f"移除骨架屏时出错: {e}")
        
        # 创建固定尺寸的卡片容器
        card_container = ctk.CTkFrame(row_frame, 
                                    fg_color="transparent", 
                                    width=self.card_width, 
                                    height=self.card_height)
        card_container.pack(side="left", padx=self.card_margin//2, pady=5)
        card_container.pack_propagate(False)  # 防止容器自适应内容大小
        
        # 创建卡片
        try:
            card = AssetCard(card_container, asset, self.controller, self.image_utils)
            card.pack(fill="both", expand=True)
            
            # 保存卡片引用
            self.card_refs[index] = card
            
            # 如果滚动已经停止，立即为卡片添加动画
            if not self._is_scrolling and self._is_card_visible(index):
                self._fade_in_card(card)
                card._animated = True
            else:
                # 否则标记为未动画
                card._animated = False
        except Exception as e:
            print(f"创建卡片时出错: {e}")
            # 出错时从加载集合中移除索引，以便后续可以重试
            if index in self.loaded_indices:
                self.loaded_indices.remove(index)

    # center_window 方法已被 DialogUtils 替代，移除冗余代码
    def bind_children_mousewheel(self, widget):
        """递归绑定所有子组件的鼠标滚轮事件"""
        widget.bind("<MouseWheel>", self.on_mouse_wheel)
        for child in widget.winfo_children():
            self.bind_children_mousewheel(child)

    def on_mouse_wheel(self, event):
        """处理鼠标滚轮事件，每次滚动两个资产卡片的高度距离"""
        # 获取资产卡片的高度（包括边距）
        card_height = 260  # 卡片高度
        card_margin = 15   # 卡片间距
        # 计算两个卡片的高度距离
        target_scroll_distance = 2 * (card_height + card_margin)  # 550像素
        
        # 添加一个放大系数来调整滚动敏感度
        scroll_amplification = 2.0  # 放大系数，调整为更合适的值
        
        # 应用放大系数
        adjusted_scroll_distance = target_scroll_distance * scroll_amplification
        
        # 使用相对滚动方式，类似于项目管理界面的实现
        # 计算滚动单位数（每个单位大约是20像素）
        scroll_units = int(adjusted_scroll_distance / 20)
        
        # 根据滚轮方向滚动
        if event.delta > 0:
            # 向上滚动
            self.asset_scrollable._parent_canvas.yview_scroll(-scroll_units, "units")
        else:
            # 向下滚动
            self.asset_scrollable._parent_canvas.yview_scroll(scroll_units, "units")
        
        # 阻止事件继续传播，避免其他组件处理
        return "break"
