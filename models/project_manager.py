import os
import json
import time
from datetime import datetime
from typing import List, Dict, Optional
from utils.config_manager import ConfigManager, get_user_config_dir

# 定义默认项目配置
DEFAULT_PROJECTS_CONFIG = {
    "recent_projects": [],
    "last_updated": "",
    "settings": {
        "auto_scan": True,
        "scan_paths": ["C:\\"],
        "exclude_paths": [
            "C:\\Windows", "C:\\Program Files", "C:\\Program Files (x86)",
            "C:\\ProgramData\\Epic\\EpicGamesLauncher\\VaultCache",
            "AppData\\Roaming", "AppData\\Local", 
            "Documents\\Visual Studio Code", "Documents\\GitHub",
            ".vs", ".vscode", "node_modules", ".git", "__pycache__",
            "Temp", "$Recycle.Bin", "System Volume Information",
            # UE引擎相关排除路径
            "Epic Games\\UE_", "Unreal Engine", "Templates", "Samples"
        ],
        "max_projects": 50
    },
    "version": "1.0.0"
}

class ProjectManager:
    """虚幻引擎工程管理器"""
    
    def __init__(self):
        self.projects = []
        # 获取用户配置目录
        config_dir = get_user_config_dir()
            
        self.config_file = os.path.join(config_dir, "ue_projects.json")
        # 创建配置管理器
        self.config_manager = ConfigManager(
            config_file=self.config_file,
            current_version="1.0.0",
            default_config=DEFAULT_PROJECTS_CONFIG
        )
        # 加载配置
        self.config = self.config_manager.load_config()
        self.recent_projects = self.config.get("recent_projects", [])
    
    def load_config(self):
        """加载配置文件"""
        try:
            self.config = self.config_manager.load_config()
            self.recent_projects = self.config.get('recent_projects', [])
        except Exception as e:
            print(f"加载配置失败: {e}")
            self.recent_projects = []

    def save_config(self):
        """保存配置文件"""
        try:
            # 更新配置数据
            self.config["recent_projects"] = self.recent_projects
            self.config["last_updated"] = datetime.now().isoformat()
            
            # 保存配置
            return self.config_manager.save_config(self.config)
        except Exception as e:
            print(f"保存配置失败: {e}")
            return False
    
    def get_running_ue_processes(self) -> List[Dict]:
        """获取当前运行的虚幻引擎进程"""
        running_processes = []
        
        try:
            # 尝试导入psutil来获取进程信息
            import psutil
            
            # 查找可能的虚幻引擎相关进程
            ue_process_names = [
                'UE4Editor.exe', 'UnrealEditor.exe', 'UE5Editor.exe',
                'UE4Editor-Win64-Debug.exe', 'UE4Editor-Win64-Development.exe',
                'UnrealEditor-Win64-Debug.exe', 'UnrealEditor-Win64-Development.exe'
            ]
            
            for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
                try:
                    # 检查进程名称是否匹配
                    if proc.info['name'] in ue_process_names:
                        # 获取进程的命令行参数，通常包含工程路径
                        cmdline = proc.info['cmdline']
                        project_path = None
                        
                        if cmdline and len(cmdline) > 1:
                            # 查找命令行中的.uproject文件
                            for arg in cmdline:
                                if arg.endswith('.uproject'):
                                    project_path = arg
                                    break
                        
                        running_processes.append({
                            'pid': proc.info['pid'],
                            'name': proc.info['name'],
                            'exe': proc.info['exe'],
                            'project_path': project_path,
                            'project_name': os.path.splitext(os.path.basename(project_path))[0] if project_path else '未知项目'
                        })
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    # 忽略无法访问的进程
                    pass
                    
        except ImportError:
            print("未安装psutil库，无法获取运行中的虚幻引擎进程")
        except Exception as e:
            print(f"获取运行进程时出错: {e}")
        
        return running_processes
    
    def _is_ue_engine_path(self, path_lower: str) -> bool:
        """
        检查是否为UE引擎的安装目录、模板或示例目录
        
        Args:
            path_lower: 小写的路径字符串
            
        Returns:
            如果是UE引擎目录则返回true
        """
        # 检查是否是在Program Files下的Epic Games官方安装目录
        if 'program files' in path_lower and 'epic games' in path_lower:
            # Epic Games官方安装的UE引擎目录
            if any(pattern in path_lower for pattern in ['\\ue_', 'unreal engine']):
                return True
        
        # 检查是否包含明显的引擎特征目录（只在引擎安装目录下才算）
        engine_feature_dirs = ['templates', 'samples', 'featurepacks']
        if any(feature in path_lower for feature in engine_feature_dirs):
            # 进一步检查这些目录是否在引擎安装目录下
            if any(engine_pattern in path_lower for engine_pattern in ['epic games\\ue_', 'program files\\epic games', 'program files\\unreal engine']):
                return True
        
        # 检查是否是Engine目录下的内容（引擎源码或安装目录）
        if 'engine\\content' in path_lower or 'engine\\plugins' in path_lower:
            return True
        
        return False
    
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
        
        # 获取排除路径设置，并确保包含用户路径的常见干扰目录
        config_exclude_paths = self.config.get("settings", {}).get("exclude_paths", [])
        
        # 基础排除路径（总是应用）
        base_exclude_paths = [
            'appdata\\roaming',    # AppData\Roaming 目录
            'appdata\\local',      # AppData\Local 目录  
            'temp',                 # 临时文件目录
            '$recycle.bin',         # 回收站
            'system volume information',  # 系统信息
            'windows',              # Windows 系统目录
            'program files',        # 程序安装目录（任意驱动器）
            'program files (x86)',  # 32位程序安装目录（任意驱动器）
            'programdata\\epic\\epicgameslauncher\\vaultcache',  # Epic 缓存目录
            '.vs',                  # Visual Studio 缓存
            '.vscode',              # VS Code 缓存
            'node_modules',         # Node.js 模块
            '.git',                 # Git 仓库
            '__pycache__',          # Python 缓存
            # 用户文档目录下的常见干扰路径
            'documents\\visual studio code',  # VS Code 用户数据
            'documents\\github',             # GitHub Desktop
            'documents\\windowspowershell',  # PowerShell 配置
            # VS Code 历史记录和缓存
            'user\\history',        # VS Code 历史记录
            'user\\workspaceStorage', # VS Code 工作区存储
            'extensions',           # VS Code 扩展
            # 其他开发工具缓存
            '.nuget',               # NuGet 包缓存
            'node_cache',           # Node 缓存
            'npm-cache',            # NPM 缓存
        ]
        
        # UE引擎相关排除路径（只针对明确的引擎安装目录）
        engine_exclude_patterns = [
            'epic games\\ue_',              # Epic Games\UE_x.xx 引擎安装目录
            'program files\\epic games',    # Program Files下的Epic Games目录
            'program files\\unreal engine', # Program Files下的Unreal Engine目录
            'engine\\content',              # 引擎内容目录
            'engine\\plugins',             # 引擎插件目录
        ]
        base_exclude_paths.extend(engine_exclude_patterns)
        
        # 合并配置文件中的排除路径和基础排除路径
        exclude_paths = base_exclude_paths.copy()
        for path in config_exclude_paths:
            # 将配置文件中的路径转换为小写并添加到排除列表
            exclude_paths.append(path.lower().replace('\\', '\\'))
        
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
                    root_lower = root.lower().replace('\\', '\\')
                    should_skip = False
                    
                    # 更精确的路径匹配
                    for excluded in exclude_paths:
                        # 检查路径是否包含排除关键词
                        if excluded in root_lower:
                            should_skip = True
                            print(f"跳过目录 (匹配排除规则 '{excluded}'): {root}")
                            break
                        
                        # 特别检查用户目录下的特定路径
                        if 'users\\' in root_lower:
                            # 检查是否是用户目录下的系统/缓存文件夹
                            user_relative_path = root_lower.split('users\\', 1)[-1]
                            if '\\' in user_relative_path:
                                user_folder = user_relative_path.split('\\', 1)[-1]
                                if any(exc in user_folder for exc in ['appdata', 'documents\\visual studio code', 'documents\\github']):
                                    should_skip = True
                                    print(f"跳过用户目录下的系统文件夹: {root}")
                                    break
                    
                    # 特殊检查：UE引擎安装目录和模板
                    if not should_skip:
                        # 检查是否是UE引擎的模板或示例目录
                        if self._is_ue_engine_path(root_lower):
                            should_skip = True
                            print(f"跳过UE引擎模板/示例目录: {root}")
                    
                    if should_skip:
                        dirs.clear()  # 不深入这些目录
                        continue
                    
                    for file in files:
                        if file.lower().endswith('.uproject'):
                            project_path = os.path.join(root, file)
                            
                            # 再次检查完整路径是否包含屏蔽关键词
                            project_path_lower = project_path.lower().replace('\\', '\\')
                            is_excluded = False
                            
                            for excluded in exclude_paths:
                                if excluded in project_path_lower:
                                    is_excluded = True
                                    print(f"排除工程文件 (匹配规则 '{excluded}'): {project_path}")
                                    break
                            
                            # 额外检查：排除明显的临时文件或缓存文件
                            if not is_excluded:
                                # 检查文件名是否包含可疑特征
                                filename_lower = file.lower()
                                suspicious_patterns = ['temp', 'cache', 'backup', 'copy', 'test']
                                
                                # 检查路径中是否包含版本控制相关目录
                                path_segments = project_path_lower.split(os.sep)
                                if any(segment in ['.git', '.svn', '.hg', 'node_modules'] for segment in path_segments):
                                    is_excluded = True
                                    print(f"排除版本控制目录中的工程: {project_path}")
                            
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
        # 如果还没有工程列表，先进行搜索
        if not self.projects:
            return self.refresh_projects()
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
        projects = self.search_ue_projects(progress_callback)
        self.projects = projects  # 确保更新内部工程列表
        return projects