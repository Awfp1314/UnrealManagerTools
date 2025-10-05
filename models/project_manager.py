import os
import json
import time
from datetime import datetime
from typing import List, Dict, Optional

class ProjectManager:
    """虚幻引擎工程管理器"""
    
    def __init__(self):
        self.projects = []
        self.recent_projects = []
        self.config_file = "ue_projects.json"
        self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.recent_projects = data.get('recent_projects', [])
        except Exception as e:
            print(f"加载配置失败: {e}")
            self.recent_projects = []
    
    def save_config(self):
        """保存配置文件"""
        try:
            data = {
                'recent_projects': self.recent_projects,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置失败: {e}")
    
    def search_ue_projects(self, progress_callback=None) -> List[Dict]:
        """搜索系统中的UE工程文件"""
        projects = []
        
        try:
            # 尝试导入psutil，如果失败则使用备用方案
            import psutil
            partitions = psutil.disk_partitions()
        except ImportError:
            print("未安装psutil库，使用备用方案")
            # 备用方案：只搜索常见的磁盘驱动器
            import string
            partitions = []
            for letter in string.ascii_uppercase:
                drive = f"{letter}:\\"
                if os.path.exists(drive):
                    partitions.append(type('Partition', (), {'mountpoint': drive, 'opts': '', 'fstype': 'NTFS'})())
        
        # 定义需要屏蔽的目录（不是真正的工程目录）
        excluded_paths = [
            'appdata\\roaming',  # 屏蔽 AppData\Roaming 目录
            'appdata\\local',    # 屏蔽 AppData\Local 目录  
            'temp',               # 临时文件目录
            '$recycle.bin',       # 回收站
            'system volume information',  # 系统信息
            'windows',            # Windows 系统目录
            'program files',      # 程序安装目录
            'programdata\\epic\\epicgameslauncher\\vaultcache',  # Epic 缓存目录
            '.vs',                # Visual Studio 缓存
            '.vscode',            # VS Code 缓存
            'node_modules',       # Node.js 模块
            '.git',               # Git 仓库
            '__pycache__',        # Python 缓存
        ]
        
        total_partitions = len(partitions)
        
        for i, partition in enumerate(partitions):
            try:
                # 跳过网络驱动器和光驱
                if hasattr(partition, 'opts') and 'cdrom' in partition.opts:
                    continue
                if hasattr(partition, 'fstype') and partition.fstype == '':
                    continue
                    
                drive = partition.mountpoint
                print(f"正在搜索磁盘: {drive}")
                
                # 搜索该磁盘下的.uproject文件
                for root, dirs, files in os.walk(drive):
                    # 检查是否在屏蔽路径列表中
                    root_lower = root.lower()
                    should_skip = False
                    
                    for excluded in excluded_paths:
                        if excluded in root_lower:
                            should_skip = True
                            break
                    
                    if should_skip:
                        dirs.clear()  # 不深入这些目录
                        continue
                    
                    for file in files:
                        if file.lower().endswith('.uproject'):
                            project_path = os.path.join(root, file)
                            
                            # 再次检查完整路径是否包含屏蔽关键词
                            project_path_lower = project_path.lower()
                            is_excluded = False
                            
                            for excluded in excluded_paths:
                                if excluded in project_path_lower:
                                    is_excluded = True
                                    break
                            
                            if not is_excluded:
                                # 获取文件信息
                                try:
                                    stat = os.stat(project_path)
                                    project_info = {
                                        'name': os.path.splitext(file)[0],
                                        'path': project_path,
                                        'dir': root,
                                        'size': stat.st_size,
                                        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                                        'created': datetime.fromtimestamp(stat.st_ctime).isoformat()
                                    }
                                    projects.append(project_info)
                                    print(f"找到UE工程: {project_path}")
                                except Exception as e:
                                    print(f"获取文件信息失败 {project_path}: {e}")
                    
                    # 限制搜索深度，避免过深递归
                    if root.count(os.sep) - drive.count(os.sep) > 6:
                        dirs.clear()
                
                # 更新进度
                if progress_callback:
                    progress_callback((i + 1) / total_partitions)
                    
            except (PermissionError, OSError) as e:
                print(f"无法访问磁盘 {partition.mountpoint}: {e}")
                continue
        
        # 按修改时间排序
        projects.sort(key=lambda x: x['modified'], reverse=True)
        self.projects = projects
        return projects
    
    def get_projects(self) -> List[Dict]:
        """获取所有工程"""
        return self.projects
    
    def get_recent_projects(self) -> List[Dict]:
        """获取最近打开的工程"""
        # 过滤掉不存在的工程
        valid_recent = []
        for project in self.recent_projects:
            if os.path.exists(project.get('path', '')):
                valid_recent.append(project)
        
        # 如果有变化，更新列表
        if len(valid_recent) != len(self.recent_projects):
            self.recent_projects = valid_recent
            self.save_config()
        
        return self.recent_projects
    
    def add_recent_project(self, project: Dict):
        """添加到最近打开列表"""
        # 移除重复项
        self.recent_projects = [p for p in self.recent_projects if p.get('path') != project.get('path')]
        
        # 添加到开头
        project['last_opened'] = datetime.now().isoformat()
        self.recent_projects.insert(0, project)
        
        # 保持最多10个最近项目
        self.recent_projects = self.recent_projects[:10]
        
        # 保存配置
        self.save_config()
    
    def open_project(self, project: Dict):
        """打开工程"""
        project_path = project.get('path', '')
        if os.path.exists(project_path):
            try:
                # 添加到最近打开列表
                self.add_recent_project(project)
                
                # 使用系统默认程序打开.uproject文件
                os.startfile(project_path)
                return True
            except Exception as e:
                print(f"打开工程失败: {e}")
                return False
        else:
            print(f"工程文件不存在: {project_path}")
            return False
    
    def get_project_info(self, project_path: str) -> Optional[Dict]:
        """获取工程详细信息"""
        try:
            if not os.path.exists(project_path):
                return None
            
            # 读取.uproject文件内容
            with open(project_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
            
            # 提取基本信息
            info = {
                'engine_version': content.get('EngineAssociation', '未知'),
                'description': content.get('Description', ''),
                'category': content.get('Category', ''),
                'company': content.get('CompanyName', ''),
                'homepage': content.get('Homepage', ''),
                'plugins': len(content.get('Plugins', [])),
                'modules': len(content.get('Modules', []))
            }
            
            return info
        except Exception as e:
            print(f"读取工程信息失败: {e}")
            return None
    
    def refresh_projects(self, progress_callback=None):
        """刷新工程列表"""
        return self.search_ue_projects(progress_callback)