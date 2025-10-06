import json
import os
from datetime import datetime
from utils.config_manager import ConfigManager, get_user_config_dir

# 定义默认资源配置
DEFAULT_ASSETS_CONFIG = {
    "resources": [],
    "categories": ["默认"],
    "category_paths": {},
    "settings": {
        "auto_refresh": True,
        "show_preview": True,
        "max_recent_files": 10
    },
    "version": "1.0.0"
}

class AssetManager:
    def __init__(self):
        # 获取用户配置目录
        config_dir = get_user_config_dir()
        
        self.data_file = os.path.join(config_dir, "ue_assets.json")
        # 创建配置管理器
        self.config_manager = ConfigManager(
            config_file=self.data_file,
            current_version="1.0.0",
            default_config=DEFAULT_ASSETS_CONFIG
        )
        # 加载配置
        self.config = self.config_manager.load_config()
        self.categories = ["全部"] + self.config.get("categories", ["默认"])
        self.category_paths = self.config.get("category_paths", {})
        self.resources = self.config.get("resources", [])
    
    def load_data(self):
        """加载数据"""
        try:
            self.config = self.config_manager.load_config()
            self.resources = self.config.get('resources', [])
            # 加载自定义分类
            custom_cats = self.config.get('categories', [])
            for cat in custom_cats:
                if cat not in self.categories and cat != "全部":
                    self.categories.append(cat)
            
            # 加载分类路径
            self.category_paths = self.config.get('category_paths', {})
        except Exception as e:
            # 用日志记录替代控制台输出
            import logging
            logging.error(f"加载数据失败: {e}")
            self.resources = []

    def save_data(self):
        """保存数据"""
        try:
            # 更新配置数据
            self.config["resources"] = self.resources
            self.config["categories"] = [cat for cat in self.categories if cat != "全部"]
            self.config["category_paths"] = self.category_paths
            
            # 保存配置
            return self.config_manager.save_config(self.config)
        except Exception as e:
            import logging
            logging.error(f"保存数据失败: {str(e)}")
            return False

    def get_resources(self):
        """获取所有资源"""
        return self.resources

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
            return self.save_data()
        return False

    def add_category_path(self, category, path):
        """为分类添加路径"""
        if category not in self.category_paths:
            self.category_paths[category] = []
        
        if path not in self.category_paths[category]:
            self.category_paths[category].append(path)
            return self.save_data()
        return False

    def remove_category_path(self, category, path):
        """从分类中移除路径"""
        if category in self.category_paths and path in self.category_paths[category]:
            self.category_paths[category].remove(path)
            return self.save_data()
        return False

    def get_category_paths(self, category):
        """获取分类的路径列表"""
        return self.category_paths.get(category, [])

    def is_path_conflict(self, category, path):
        """检查路径是否与其他分类冲突"""
        for cat, paths in self.category_paths.items():
            if cat != category and path in paths:
                return True
        return False

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