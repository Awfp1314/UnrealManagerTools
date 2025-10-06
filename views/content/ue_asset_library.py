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
        
        self.create_widgets()
        
        # 后台预加载资源数据
        self.preload_assets_data()
    
    def preload_assets_data(self):
        """后台预加载资源数据"""
        def preload_thread():
            try:
                print(f"🔍 后台加载资源数据...")
                # 触发资源加载
                resources = self.controller.asset_manager.resources
                print(f"✅ 后台资源加载完成，找到 {len(resources)} 个资源")
                
                # 标记数据已加载
                self.is_data_loaded = True
                self.last_refresh_time = datetime.now()
                
            except Exception as e:
                print(f"后台资源加载出错: {e}")
        
        # 在后台线程中执行加载，不影响界面加载速度
        threading.Thread(target=preload_thread, daemon=True).start()

    def create_widgets(self):
        """创建内容区域组件"""
        # 内容头部
        header_frame = ctk.CTkFrame(self, fg_color="transparent", height=80)
        header_frame.pack(fill="x", padx=20, pady=10)
        header_frame.pack_propagate(False)
        
        # 顶部：标题和资产总数
        top_header = ctk.CTkFrame(header_frame, fg_color="transparent")
        top_header.pack(fill="x", pady=(0, 10))
        
        # 工具名称标题和资产总数
        title_frame = ctk.CTkFrame(top_header, fg_color="transparent")
        title_frame.pack(side="left", fill="y")
        
        self.tool_title = ctk.CTkLabel(title_frame, 
                                      text="虚幻资产库",
                                      font=ctk.CTkFont(size=18, weight="bold"))
        self.tool_title.pack(side="left")
        
        self.asset_count_label = ctk.CTkLabel(title_frame, 
                                             text="",
                                             font=ctk.CTkFont(size=14),
                                             text_color=("gray50", "gray50"))
        self.asset_count_label.pack(side="left", padx=(10, 0))
        
        # 底部：搜索和操作区域
        bottom_header = ctk.CTkFrame(header_frame, fg_color="transparent")
        bottom_header.pack(fill="x")
        
        # 左侧：搜索框
        search_frame = ctk.CTkFrame(bottom_header, fg_color="transparent")
        search_frame.pack(side="left", fill="x", expand=True)
        
        # 搜索框
        self.search_entry = SearchEntry(search_frame, 
                                       placeholder_text="搜索资产...",
                                       height=38,
                                       command=self.on_search)
        self.search_entry.pack(side="left", fill="x", expand=True)
        
        # 右侧：操作按钮
        ops_frame = ctk.CTkFrame(bottom_header, fg_color="transparent")
        ops_frame.pack(side="right", padx=(10, 0))
        
        # 分类下拉框
        category_frame = ctk.CTkFrame(ops_frame, fg_color="transparent")
        category_frame.pack(side="left", padx=(0, 10))
        
        self.category_var = ctk.StringVar(value="全部")
        self.category_combo = ctk.CTkComboBox(category_frame, 
                                            variable=self.category_var,
                                            values=self.controller.asset_manager.categories,
                                            command=self.on_category_change,
                                            width=150,
                                            height=38,
                                            state="readonly",
                                            font=ctk.CTkFont(size=13, weight="bold"),
                                            dropdown_font=ctk.CTkFont(size=13),
                                            corner_radius=8)  # 设置为不可编辑
        
        self.category_combo.pack(side="left")
        
        # 使用延迟自动关闭下拉菜单，同时保留悬浮动画
        self.category_combo.bind("<<ComboboxSelected>>", self._start_close_timer)
        self.close_timer = None
        
        # 刷新按钮
        self.refresh_btn = ctk.CTkButton(ops_frame, 
                                        text="🔄 刷新数据",
                                        command=lambda: self.refresh_content(force=True),
                                        height=38,
                                        width=120,
                                        font=ctk.CTkFont(size=13, weight="bold"),
                                        fg_color=("#2196F3", "#14375e"),
                                        hover_color=("#1976D2", "#1e5a8a"),
                                        text_color=("white", "white"),
                                        corner_radius=8)
        self.refresh_btn.pack(side="left", padx=5)
        
        # 管理分类按钮
        self.manage_category_btn = ctk.CTkButton(ops_frame, 
                                                text="管理分类",
                                                command=self.show_manage_categories_dialog,
                                                height=38,
                                                width=100,
                                                font=ctk.CTkFont(size=13, weight="bold"),
                                                fg_color="transparent",
                                                hover_color=("#e0e0e0", "#3d3d3d"),
                                                text_color=("#333333", "#ffffff"),
                                                border_width=2,
                                                border_color=("#2196F3", "#4299e1"),
                                                corner_radius=8)
        self.manage_category_btn.pack(side="left", padx=5)
        
        # 添加资产按钮
        self.add_btn = ctk.CTkButton(ops_frame, 
                                    text="+添加资产",
                                    command=self.import_assets,
                                    height=38,
                                    width=100,
                                    font=ctk.CTkFont(size=13, weight="bold"),
                                    fg_color=("#4CAF50", "#2E7D32"),
                                    hover_color=("#388E3C", "#1B5E20"),
                                    text_color=("white", "white"),
                                    corner_radius=8)
        self.add_btn.pack(side="left", padx=5)
        
        # 刷新状态提示
        self.status_frame = ctk.CTkFrame(self, fg_color="transparent", height=30)
        self.status_frame.pack(fill="x", padx=20, pady=(0, 5))
        self.status_frame.pack_propagate(False)
        
        self.status_label = ctk.CTkLabel(self.status_frame, 
                                        text="",
                                        font=ctk.CTkFont(size=12),
                                        text_color=("gray50", "gray50"))
        self.status_label.pack(side="left")
        
        # 创建资产网格容器 - 优化背景显示
        self.asset_scrollable = ctk.CTkScrollableFrame(self, 
                                                      fg_color=("gray95", "gray15"),  # 设置浅色背景
                                                      corner_radius=8)
        self.asset_scrollable.pack(fill="both", expand=True, padx=10, pady=10)

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
        
        # 如果是强制刷新，执行路径扫描和智能添加
        if force:
            self._scan_and_add_resources()
        
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
    
    def _scan_and_add_resources(self):
        """扫描分类路径并智能添加新资源"""
        current_category = self.controller.app_state.current_category
        if current_category == "全部":
            # 如果是"全部"分类，扫描所有分类的路径
            categories = [cat for cat in self.controller.asset_manager.categories if cat != "全部"]
            self._scan_multiple_categories_and_add_resources(categories)
        else:
            # 扫描当前分类的路径
            self._scan_category_and_add_resources(current_category)
    
    def _scan_multiple_categories_and_add_resources(self, categories):
        """扫描多个分类的路径并添加新资源，避免重复发现同一路径"""
        # 全局已发现的路径集合，避免重复发现
        globally_discovered_paths = set()
        all_new_folders = []
        
        # 获取所有已有的资源路径
        existing_paths = set()
        for asset in self.controller.asset_manager.resources:
            existing_paths.add(os.path.abspath(asset.get('path', '')))
        
        # 扫描每个分类的路径
        for category in categories:
            paths = self.controller.asset_manager.get_category_paths(category)
            
            # 扫描每个路径
            for base_path in paths:
                if os.path.exists(base_path):
                    try:
                        # 遍历路径下的所有直接子文件夹
                        for item in os.listdir(base_path):
                            item_path = os.path.join(base_path, item)
                            if os.path.isdir(item_path):
                                abs_path = os.path.abspath(item_path)
                                # 如果该文件夹既不在已有的资源中，也没有被其他分类发现过，则为新发现
                                if abs_path not in existing_paths and abs_path not in globally_discovered_paths:
                                    globally_discovered_paths.add(abs_path)
                                    all_new_folders.append({
                                        'name': item,
                                        'path': abs_path,
                                        'category': category
                                    })
                    except Exception as e:
                        import logging
                        logging.error(f"扫描路径失败 {base_path}: {e}")
        
        if all_new_folders:
            # 串行处理新发现的文件夹
            self._process_new_folders_serially(all_new_folders, 0)
    
    def _scan_category_and_add_resources(self, category):
        """扫描指定分类的路径并添加新资源"""
        # 扫描分类路径
        new_folders = self.controller.asset_manager.scan_category_paths(category)
        
        if new_folders:
            # 串行处理新发现的文件夹
            self._process_new_folders_serially(new_folders, 0)
    
    def _process_new_folders_serially(self, folders, index):
        """串行处理新文件夹"""
        if index >= len(folders):
            # 所有文件夹处理完毕，刷新界面
            self.refresh_content()
            return
        
        folder = folders[index]
        
        # 创建添加资产对话框
        self._show_add_asset_dialog(
            folder['name'], 
            folder['path'], 
            folder['category'],
            lambda: self._process_new_folders_serially(folders, index + 1)  # 处理下一个
        )
    
    def _show_add_asset_dialog(self, name, path, category, on_complete):
        """显示添加资产对话框"""
        from tkinter import filedialog
        import os
        
        # 创建对话框
        dialog = ctk.CTkToplevel(self.controller.root)
        dialog.title("添加新资产")
        dialog.geometry("500x600")  # 进一步增加高度以确保按钮可见
        dialog.resizable(False, False)
        dialog.transient(self.controller.root)
        dialog.grab_set()
        
        # 居中显示
        self._center_dialog_on_main_window(dialog)
        
        # 创建表单
        form_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 提示信息
        info_label = ctk.CTkLabel(form_frame, 
                                 text=f"发现新资源文件夹，是否添加到 {category} 分类？",
                                 font=ctk.CTkFont(size=14, weight="bold"),
                                 wraplength=400)
        info_label.pack(pady=(0, 20))
        
        # 文件夹信息
        folder_frame = ctk.CTkFrame(form_frame, fg_color=("gray90", "gray20"))
        folder_frame.pack(fill="x", pady=(0, 20), padx=10)
        
        ctk.CTkLabel(folder_frame, text="📁 文件夹名称:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        ctk.CTkLabel(folder_frame, text=name, font=ctk.CTkFont(size=12)).pack(anchor="w", padx=20)
        
        ctk.CTkLabel(folder_frame, text="📂 文件夹路径:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        path_label = ctk.CTkLabel(folder_frame, text=path, font=ctk.CTkFont(size=12), wraplength=400)
        path_label.pack(anchor="w", padx=20, pady=(0, 10))
        
        # 资源名称
        ctk.CTkLabel(form_frame, text="资源名称:", 
                    font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(0, 5))
        name_var = ctk.StringVar(value=name)
        name_entry = ctk.CTkEntry(form_frame, textvariable=name_var, 
                                 height=35, font=ctk.CTkFont(size=13))
        name_entry.pack(fill="x", pady=(0, 15))
        
        # 分类（固定为当前分类）
        ctk.CTkLabel(form_frame, text="分类:", 
                    font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(0, 5))
        category_label = ctk.CTkLabel(form_frame, text=category, 
                                     font=ctk.CTkFont(size=13),
                                     fg_color=("gray80", "gray25"),
                                     corner_radius=6,
                                     height=35)
        category_label.pack(fill="x", pady=(0, 15))
        
        # 封面图片
        ctk.CTkLabel(form_frame, text="封面图片:", 
                    font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(0, 5))
        cover_var = ctk.StringVar()
        
        # 自动检测文件夹内的图片作为默认封面
        default_cover = self._find_default_cover_image(path)
        if default_cover:
            cover_var.set(default_cover)
        
        cover_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        cover_frame.pack(fill="x", pady=(0, 15))
        cover_entry = ctk.CTkEntry(cover_frame, textvariable=cover_var,
                                  font=ctk.CTkFont(size=13))
        cover_entry.pack(side="left", fill="x", expand=True)
        
        # 传递文件夹路径给浏览封面图片方法
        ctk.CTkButton(cover_frame, text="选择", width=80,
                     command=lambda: self.browse_cover_image_in_folder(cover_var, path)).pack(side="right", padx=(5, 0))
        
        # 是否创建README
        readme_var = ctk.BooleanVar(value=False)
        readme_check = ctk.CTkCheckBox(form_frame, text="创建README.md文档",
                                      variable=readme_var,
                                      font=ctk.CTkFont(size=13))
        readme_check.pack(anchor="w", pady=15)
        
        # 按钮框架 - 使用 pack 到底部确保可见
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=10, side="bottom")
        
        def add_resource():
            """添加资源"""
            if self.controller.asset_manager.add_resource(
                name_var.get(), path, category, cover_var.get(), readme_var.get()):
                self.show_status(f"资源添加成功: {name_var.get()}", "success")
                dialog.destroy()
                # 自动刷新资产界面
                self.refresh_content()
                # 处理下一个文件夹
                on_complete()
            else:
                self.show_status("资源添加失败", "error")
        
        def skip_resource():
            """跳过资源"""
            dialog.destroy()
            # 自动刷新资产界面
            self.refresh_content()
            # 处理下一个文件夹
            on_complete()
        
        ctk.CTkButton(btn_frame, text="添加", command=add_resource,
                     width=80, height=35,
                     font=ctk.CTkFont(size=13, weight="bold"),
                     fg_color=("#4CAF50", "#2E7D32"),
                     hover_color=("#388E3C", "#1B5E20"),
                     text_color=("white", "white"),
                     corner_radius=8).pack(side="left", padx=5)
        
        ctk.CTkButton(btn_frame, text="跳过", command=skip_resource,
                     width=80, height=35,
                     font=ctk.CTkFont(size=13, weight="bold"),
                     fg_color=("#2196F3", "#14375e"),
                     hover_color=("#1976D2", "#1e5a8a"),
                     text_color=("white", "white"),
                     corner_radius=8).pack(side="left", padx=5)
        
        ctk.CTkButton(btn_frame, text="取消", command=lambda: [dialog.destroy(), on_complete()],
                     width=80, height=35,
                     font=ctk.CTkFont(size=13, weight="bold"),
                     fg_color=("#f44336", "#d32f2f"),
                     hover_color=("#d32f2f", "#b71c1c"),
                     text_color=("white", "white"),
                     corner_radius=8).pack(side="right", padx=5)
    
    def browse_cover_image_in_folder(self, cover_var, folder_path):
        """在指定文件夹中浏览封面图片"""
        from tkinter import filedialog
        file = filedialog.askopenfilename(
            title="选择封面图片",
            initialdir=folder_path,  # 设置初始目录为文件夹路径
            filetypes=[("图片文件", "*.png *.jpg *.jpeg *.bmp *.gif *.tga *.psd")]
        )
        if file:
            cover_var.set(file)
    
    def _find_default_cover_image(self, folder_path):
        """在文件夹中查找默认封面图片"""
        if not os.path.exists(folder_path):
            return ""
        
        # 支持的图片格式
        image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tga', '.psd'}
        
        try:
            # 遍历文件夹中的文件
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                if os.path.isfile(item_path):
                    # 检查文件扩展名
                    _, ext = os.path.splitext(item.lower())
                    if ext in image_extensions:
                        return item_path
            
            # 如果没有找到图片，返回空字符串
            return ""
        except Exception as e:
            import logging
            logging.error(f"查找默认封面图片失败: {e}")
            return ""
    
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
        """显示资产列表 - 固定4列布局，优化空状态显示"""
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
                                         height=45,
                                         width=180,
                                         font=ctk.CTkFont(size=14, weight="bold"),
                                         fg_color=("#4CAF50", "#2E7D32"),
                                         hover_color=("#388E3C", "#1B5E20"),
                                         text_color=("white", "white"),
                                         corner_radius=8)
            quick_add_btn.pack(pady=10)
            return
        
        # 创建固定4列布局
        self.create_simple_layout(assets)

    def show_manage_categories_dialog(self):
        """显示管理分类对话框 - 修改了窗口大小"""
        dialog = ctk.CTkToplevel(self.controller.root)
        dialog.title("管理分类")
        dialog.geometry("600x450")  # 减小高度以保持界面美观
        dialog.transient(self.controller.root)
        dialog.grab_set()
        dialog.resizable(False, False)  # 设置为不可由用户自由调整大小
        
        # 确保对话框始终位于主窗口的视觉中心
        self._center_dialog_on_main_window(dialog)
        
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
        self.categories_scrollable = ctk.CTkScrollableFrame(list_frame, height=200)
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
                               height=38,
                               width=80,
                               font=ctk.CTkFont(size=13, weight="bold"),
                               fg_color=("#4CAF50", "#2E7D32"),
                               hover_color=("#388E3C", "#1B5E20"),
                               text_color=("white", "white"),
                               corner_radius=8)
        add_btn.pack(side="right")
        
        # 按钮框架
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        close_btn = ctk.CTkButton(btn_frame, 
                                 text="关闭",
                                 command=dialog.destroy,
                                 height=38,
                                 width=80,
                                 font=ctk.CTkFont(size=13, weight="bold"),
                                 fg_color=("#f44336", "#d32f2f"),
                                 hover_color=("#d32f2f", "#b71c1c"),
                                 text_color=("white", "white"),
                                 corner_radius=8)
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
                                      width=70,
                                      height=32,
                                      font=ctk.CTkFont(size=12, weight="bold"),
                                      fg_color="#9E9E9E",
                                      corner_radius=6)  # 灰色表示禁用
        else:
            # 其他分类可以删除
            delete_btn = ctk.CTkButton(item_frame,
                                      text="删除",
                                      command=lambda: self.delete_category(category, item_frame),
                                      width=70,
                                      height=32,
                                      font=ctk.CTkFont(size=12, weight="bold"),
                                      fg_color="#f44336",
                                      hover_color="#d32f2f",
                                      text_color="white",
                                      corner_radius=6)
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
            if self.controller.asset_manager.remove_category(category):
                # 从UI中删除
                item_frame.destroy()
                if category in self.category_widgets:
                    del self.category_widgets[category]
                
                # 刷新主界面 - 确保下拉框同步更新
                self.update_category_combo()
                self.show_status(f"已删除分类: {category}", "success")
            else:
                self.show_status("删除分类失败", "error")

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
        dialog.geometry("500x550")  # 增加高度以适应内容并保持美观
        dialog.resizable(False, False)  # 设置为不可由用户自由调整大小
        dialog.transient(self.controller.root)
        dialog.grab_set()
        
        # 确保对话框始终位于主窗口的视觉中心
        self._center_dialog_on_main_window(dialog)
        
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
        
        # 获取分类列表（排除'全部'分类）
        category_list = [cat for cat in self.controller.asset_manager.categories if cat != "全部"]
            
        # 创建分类选择框，设置为可编辑状态，允许用户直接输入自定义分类
        category_combo = ctk.CTkComboBox(form_frame, variable=category_var, 
                                       values=category_list,
                                       height=35, font=ctk.CTkFont(size=13),
                                       state="normal")  # 设置为可编辑状态
        category_combo.pack(fill="x", pady=(0, 5))
        
        # 封面图片
        ctk.CTkLabel(form_frame, text="封面图片:", 
                    font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", pady=(10, 5))
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
        
        # 按钮框架
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=20, side="bottom")  # 固定在底部
        
        # 创建导入按钮
        import_button = ctk.CTkButton(btn_frame, text="导入", width=80, height=38,
                               font=ctk.CTkFont(size=13, weight="bold"),
                               fg_color=("#4CAF50", "#2E7D32"),
                               hover_color=("#388E3C", "#1B5E20"),
                               text_color=("white", "white"),
                               corner_radius=8)
        import_button.pack(side="left", padx=5)
        
        ctk.CTkButton(btn_frame, text="取消", command=dialog.destroy,
                     width=80, height=38,
                     font=ctk.CTkFont(size=13, weight="bold"),
                     fg_color=("#f44336", "#d32f2f"),
                     hover_color=("#d32f2f", "#b71c1c"),
                     text_color=("white", "white"),
                     corner_radius=8).pack(side="right", padx=5)
        
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
                # 福导入按钮（名称为空时）
                import_button.configure(state="disabled")
        
        # 绑定名称变量的变化事件
        name_var.trace("w", check_name_duplicate)
        
        # 初始化导入按钮状态
        check_name_duplicate()  # 检查初始名称状态
        
        def finalize_import():
            # 检查是否有名称重复错误
            if name_error_label.cget("text"):
                return  # 如果有错误，不执行导入操作
            
            # 获取分类
            category = category_var.get().strip()
            if not category:
                self.show_status("请输入分类名称", "error")
                return
            
            # 如果输入的分类不在现有分类列表中，则添加为新分类
            if category not in self.controller.asset_manager.categories:
                # 添加新分类
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
            
            if self.controller.asset_manager.add_resource(name_var.get(), path, category, 
                                             cover_var.get(), readme_var.get()):
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

    def browse_cover_image(self, cover_var):
        """浏览封面图片"""
        from tkinter import filedialog
        file = filedialog.askopenfilename(
            title="选择封面图片",
            filetypes=[("图片文件", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if file:
            cover_var.set(file)

    # browse_file 方法已被 DialogUtils 替代，移除冗余代码

    def create_simple_layout(self, assets):
        """创建简单的4列布局 - 优化少量资产的显示效果"""
        # 卡片参数
        card_width = 180
        card_height = 220
        card_margin = 15
        cards_per_row = 4  # 固定4列
        
        # 先隐藏滚动区域，避免绘制痕迹
        self.asset_scrollable.pack_forget()
        
        # 清空现有显示
        for widget in self.asset_scrollable.winfo_children():
            widget.destroy()
        
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
        
        # 预创建所有卡片组件（不显示）
        card_containers = []
        cards = []
        
        # 创建资产卡片容器和卡片对象
        current_row = None
        row_containers = []
        
        for i, asset in enumerate(assets):
            if i % cards_per_row == 0:
                current_row = ctk.CTkFrame(self.asset_scrollable, fg_color="transparent")
                row_containers.append(current_row)
            
            # 创建固定尺寸的卡片容器
            card_container = ctk.CTkFrame(current_row, 
                                        fg_color="transparent", 
                                        width=card_width, 
                                        height=card_height)
            card_container.pack_propagate(False)  # 防止容器自适应内容大小
            
            # 创建卡片（此时不添加到容器中）
            card = AssetCard(card_container, asset, self.controller, self.image_utils)
            
            card_containers.append((current_row, card_container, i % cards_per_row))
            cards.append(card)
        
        # 批量布局所有组件
        for i, (row, container, col_index) in enumerate(card_containers):
            if col_index == 0:
                row.pack(fill="x", padx=10, pady=8)
            container.pack(side="left", padx=card_margin//2, pady=5)
        
        # 批量添加卡片到容器
        for card, (_, container, _) in zip(cards, card_containers):
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
        
        # 重新显示滚动区域
        self.asset_scrollable.pack(fill="both", expand=True, padx=10, pady=10)

    def _center_dialog_on_main_window(self, dialog):
        """将对话框居中显示在主窗口上"""
        # 等待窗口更新
        dialog.update_idletasks()
        
        # 获取主窗口的位置和尺寸
        main_window = self.controller.root
        main_window.update_idletasks()
        
        main_x = main_window.winfo_x()
        main_y = main_window.winfo_y()
        main_width = main_window.winfo_width()
        main_height = main_window.winfo_height()
        
        # 获取对话框的尺寸
        dialog_width = dialog.winfo_width()
        dialog_height = dialog.winfo_height()
        
        # 计算对话框应该出现的位置（主窗口的视觉中心）
        dialog_x = main_x + (main_width - dialog_width) // 2
        dialog_y = main_y + (main_height - dialog_height) // 2
        
        # 设置对话框位置
        dialog.geometry(f"+{dialog_x}+{dialog_y}")