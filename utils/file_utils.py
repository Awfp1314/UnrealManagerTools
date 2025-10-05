import os

class FileUtils:
    @staticmethod
    def get_folder_size(path):
        """计算文件夹大小"""
        if not os.path.exists(path):
            return "0 MB"
        
        try:
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    if os.path.exists(filepath):
                        total_size += os.path.getsize(filepath)
            
            size_mb = total_size / (1024 * 1024)
            if size_mb < 1024:
                return f"{size_mb:.1f} MB"
            else:
                return f"{size_mb/1024:.1f} GB"
        except:
            return "未知"

    @staticmethod
    def find_uproject_file(path):
        """查找.uproject文件"""
        if not os.path.exists(path):
            return None
            
        for file in os.listdir(path):
            if file.endswith('.uproject'):
                return os.path.join(path, file)
        return None