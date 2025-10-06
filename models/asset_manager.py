import json
import os
from datetime import datetime
import json

class AssetManager:
    def __init__(self):
        self.data_file = "ue_assets.json"
        self.categories = ["全部", "默认"]  # 添加默认分类
        self.category_paths = {}  # 存储每个分类的路径列表
        self.resources = []
        self.load_data()

    def load_data(self):
        """加载数据"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.resources = data.get('resources', [])
                    # 加载自定义分类
                    custom_cats = data.get('categories', [])
                    for cat in custom_cats:
                        if cat not in self.categories and cat != "全部":
                            self.categories.append(cat)
                    # 加载分类路径配置
                    self.category_paths = data.get('category_paths', {})
        except Exception as e:
            # 用日志记录替代控制台输出
            import logging
            logging.error(f"加载数据失败: {e}")
            self.resources = []
            self.category_paths = {}

    def save_data(self):
        """保存数据"""
        try:
            data = {
                "resources": self.resources,
                "categories": [cat for cat in self.categories if cat != "全部"],
                "category_paths": self.category_paths
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            import logging
            logging.error(f"保存数据失败: {str(e)}")
            return False

    def add_resource(self, name, path, category, cover, create_readme):
        """添加新资源"""
        doc_path = ""
        if create_readme:
            doc_path = os.path.join(path, "README.md")
            try:
                with open(doc_path, 'w', encoding='utf-8') as f:
                    f.write(f"# {name}\n\n资源描述...")
            except Exception as e:
                import logging
                logging.error(f"创建README失败: {e}")
        
        new_asset = {
            "name": name,
            "path": path,
            "category": category,
            "cover": cover,
            "doc": doc_path,
            "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.resources.append(new_asset)
        return self.save_data()

    def update_resource(self, resource, name, category, path, cover, create_readme):
        """更新资源信息"""
        doc_path = resource.get('doc', '')
        if create_readme and not doc_path:
            doc_path = os.path.join(path, "README.md")
            try:
                with open(doc_path, 'w', encoding='utf-8') as f:
                    f.write(f"# {name}\n\n资源描述...")
            except Exception as e:
                import logging
                logging.error(f"创建README失败: {e}")
        
        resource.update({
            'name': name,
            'category': category,
            'path': path,
            'cover': cover,
            'doc': doc_path
        })
        
        return self.save_data()

    def remove_resource(self, resource):
        """移除资源"""
        if resource in self.resources:
            self.resources.remove(resource)
            return self.save_data()
        return False

    def add_category(self, category_name):
        """添加新分类"""
        if category_name and category_name not in self.categories:
            self.categories.append(category_name)
            # 初始化该分类的路径列表
            if category_name not in self.category_paths:
                self.category_paths[category_name] = []
            return self.save_data()
        return False

    def remove_category(self, category_name):
        """移除分类"""
        if category_name in self.categories and category_name != "默认" and category_name != "全部":
            self.categories.remove(category_name)
            # 移除该分类的路径配置
            if category_name in self.category_paths:
                del self.category_paths[category_name]
            return self.save_data()
        return False

    def set_category_paths(self, category, paths):
        """设置分类的路径列表"""
        self.category_paths[category] = paths
        return self.save_data()

    def get_category_paths(self, category):
        """获取分类的路径列表"""
        return self.category_paths.get(category, [])

    def get_filtered_resources(self, current_category, search_term):
        """获取过滤后的资源列表"""
        filtered_assets = []
        for asset in self.resources:
            # 分类过滤
            if current_category != "全部":
                if asset.get('category') != current_category:
                    continue
            
            # 搜索过滤
            if search_term:
                search_in = asset.get('name', '').lower() + " " + asset.get('category', '').lower()
                if search_term not in search_in:
                    continue
            
            filtered_assets.append(asset)
        
        return filtered_assets

    def scan_category_paths(self, category):
        """扫描分类路径并返回新发现的文件夹列表"""
        paths = self.get_category_paths(category)
        new_folders = []
        
        # 获取所有已有的资源路径（全局检查，避免重复添加）
        existing_paths = set()
        for asset in self.resources:
            existing_paths.add(os.path.abspath(asset.get('path', '')))
        
        # 扫描每个路径
        for base_path in paths:
            if os.path.exists(base_path):
                try:
                    # 遍历路径下的所有直接子文件夹
                    for item in os.listdir(base_path):
                        item_path = os.path.join(base_path, item)
                        if os.path.isdir(item_path):
                            abs_path = os.path.abspath(item_path)
                            # 如果该文件夹不在已有的资源中，则为新发现
                            if abs_path not in existing_paths:
                                new_folders.append({
                                    'name': item,
                                    'path': abs_path,
                                    'category': category
                                })
                except Exception as e:
                    import logging
                    logging.error(f"扫描路径失败 {base_path}: {e}")
        
        return new_folders