# 配置管理器使用指南

## 概述

配置管理器是一个用于管理 JSON 配置文件的工具类，具有以下特性：

1. **自动创建默认配置**：首次运行时自动创建带有默认值的配置文件
2. **版本控制**：配置文件包含版本号，便于跟踪和管理
3. **自动迁移**：软件升级时自动迁移旧版本配置，保留用户数据并填充新字段
4. **用户数据保护**：配置文件存储在用户的个人数据目录中，避免软件升级时数据丢失

## 配置文件存储位置

配置文件现在存储在用户的个人数据目录中，具体位置如下：

- **Windows**: `C:\Users\<用户名>\AppData\Roaming\UnrealManagerTools\`
- **macOS**: `~/Library/Application Support/UnrealManagerTools/`
- **Linux**: `~/.config/UnrealManagerTools/`

这样做的好处是每次升级或替换软件时，都会自动读取用户的配置，不会丢失。

## 使用方法

### 1. 导入配置管理器

```python
from utils.config_manager import ConfigManager, get_user_config_dir
```

### 2. 定义默认配置

```python
# 定义默认配置（包含新字段）
DEFAULT_CONFIG = {
    "resources": [],
    "categories": ["默认"],
    "category_paths": {},
    "settings": {
        "auto_refresh": True,
        "show_preview": True,
        "max_recent_files": 10
    },
    "version": "1.0.0"  # 当前版本
}
```

### 3. 创建配置管理器实例

```python
# 获取用户配置目录
config_dir = get_user_config_dir()

# 创建配置管理器实例
config_manager = ConfigManager(
    config_file=os.path.join(config_dir, "ue_assets.json"),
    current_version="1.0.0",
    default_config=DEFAULT_CONFIG
)
```

### 4. 加载配置

```python
# 加载配置（自动处理迁移）
config = config_manager.load_config()
```

### 5. 保存配置

```python
# 修改配置
config["settings"]["auto_refresh"] = False

# 保存配置
config_manager.save_config(config)
```

## 版本迁移示例

假设我们从版本 1.0.0 升级到 1.1.0，需要添加新的配置字段：

```python
# 旧版本配置文件内容
{
    "resources": [],
    "categories": ["默认"],
    "version": "1.0.0"
}

# 新版本默认配置
DEFAULT_CONFIG = {
    "resources": [],
    "categories": ["默认"],
    "category_paths": {},  # 新增字段
    "settings": {          # 新增字段
        "auto_refresh": True,
        "show_preview": True,
        "max_recent_files": 10
    },
    "version": "1.1.0"     # 新版本号
}

# 迁移后的配置文件内容
{
    "resources": [],
    "categories": ["默认"],
    "category_paths": {},  # 自动添加
    "settings": {          # 自动添加
        "auto_refresh": True,
        "show_preview": True,
        "max_recent_files": 10
    },
    "version": "1.1.0"     # 自动更新
}
```

迁移过程会保留用户原有的数据，并自动填充新增的字段。

## 在项目中使用配置管理器

### 资产管理器中的使用

```python
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
```

### 项目管理器中的使用

```python
class ProjectManager:
    def __init__(self):
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
```

## 注意事项

1. **版本号格式**：请使用语义化版本号格式（如 1.0.0, 1.2.3）
2. **默认配置**：默认配置应包含所有可能的字段，新字段应有合理的默认值
3. **迁移逻辑**：配置管理器会自动保留旧配置中的数据，但复杂的迁移逻辑需要手动实现
4. **错误处理**：配置管理器会处理常见的文件读写错误，但建议在业务代码中添加适当的错误处理

## 常见问题

### 1. 如何添加新的配置字段？

只需在默认配置中添加新字段，并更新版本号即可。配置管理器会在下次加载时自动迁移。

### 2. 如何处理复杂的版本迁移？

对于复杂的版本迁移，可以在 `_migrate_config` 方法中添加特定版本的迁移逻辑：

```python
def _migrate_config(self, old_config: Dict[str, Any], old_version: str) -> Dict[str, Any]:
    # 创建新配置，基于默认配置
    new_config = self.default_config.copy()

    # 保留旧配置中的字段值
    for key, value in old_config.items():
        if key != "version":
            new_config[key] = value

    # 根据版本差异执行特定迁移逻辑
    if self._compare_versions(old_version, "1.1.0") < 0:
        # 从1.1.0之前版本迁移的特定逻辑
        # 例如：重新组织数据结构
        pass

    # 更新版本号
    new_config["version"] = self.current_version

    return new_config
```

### 3. 配置文件损坏怎么办？

如果配置文件损坏，配置管理器会自动创建新的默认配置文件，并输出错误信息。
