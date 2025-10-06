# UE Asset Manager

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7%2B-blue.svg">
  <img src="https://img.shields.io/badge/Unreal%20Engine-4%2B%2F5-orange.svg">
  <img src="https://img.shields.io/badge/License-MIT-green.svg">
</p>

UE Asset Manager is a resource management tool designed specifically for Unreal Engine developers, **especially suitable for beginners learning Unreal Engine**. It helps developers efficiently organize, browse, and import UE project resources, making it an ideal assistant for beginners to manage learning materials and project resources.

## Features

- 📁 **Asset Management**: Add, edit, delete and categorize UE resources
- 🔍 **Search & Filter**: Quickly find resources by name and category
- 📂 **One-click Import**: Easily import resources to UE projects
- 📊 **Resource Preview**: Display resource cover images and basic information
- 📝 **Documentation Support**: Automatically generate and manage resource README documents
- 🎨 **Theme Switching**: Support light and dark theme switching to enhance user experience
- 🚀 **UI Optimization**: Preload data for fast page switching
- ⚙️ **Configuration Management**: JSON configuration file management with version control and automatic migration
- 💾 **User Data Protection**: Configuration files are stored in user's personal data directory to prevent data loss during software upgrades

## Project Structure

```
Ue_Asset_manger/
├── README.md            # Project documentation
├── main.py              # Main program entry
├── requirements.txt     # Dependencies list
├── 测试方案.md           # Test plan
├── docs/                # Documents and reports
│   └── *.md             # Various report files
├── scripts/             # Script files
│   ├── install_dependencies.py  # Install dependencies script
│   └── install_psutil.py        # Install psutil script
├── tests/               # Test files
│   └── test_*.py        # Various test files
├── models/              # Data models
│   ├── __init__.py      # Package initialization
│   ├── app_state.py     # Application state
│   ├── asset_manager.py # Asset manager
│   └── project_manager.py # Project manager
├── views/               # View components
│   ├── __init__.py      # Package initialization
│   ├── main_window.py   # Main window
│   ├── toolbar.py       # Toolbar
│   └── content/         # Content pages
│       ├── __init__.py           # Package initialization
│       ├── base_content.py       # Base content manager
│       ├── ue_asset_library.py   # Asset library page
│       ├── ue_projects.py        # UE projects page
│       ├── settings_content.py   # Settings page
│       └── about_content.py      # About page
├── widgets/             # Custom widgets
│   ├── __init__.py      # Package initialization
│   ├── asset_card.py    # Asset card component
│   └── search_entry.py  # Search entry component
└── utils/               # Utility functions
    ├── __init__.py      # Package initialization
    ├── dialog_utils.py  # Dialog utility class
    ├── file_utils.py    # File utility class
    ├── config_manager.py # Configuration manager
    └── image_utils.py   # Image utility class
```

## Installation & Usage

### Method 1: Download Executable (Recommended for General Users)

1. Visit the project's GitHub [Releases](https://github.com/Awfp1314/Ue_Asset_manger/releases) page (no official release yet)
2. Download the latest version of `UE资源管理器_Windows_x64.zip`
3. Extract the downloaded ZIP file
4. Run `UE资源管理器.exe` to start using the application

### Method 2: Run from Source Code (For Developers)

#### Prerequisites

- Install Python 3.7 or higher
- Git is recommended for version control

#### Installation Steps

1. **Clone the repository**

```bash
git clone https://github.com/Awfp1314/Ue_Asset_manger.git
cd Ue_Asset_manger
```

2. **Install dependencies**

```bash
# Install dependencies using Python script
python scripts/install_dependencies.py

# Or install directly via pip
# Using default source:
pip install -r requirements.txt

# Using domestic mirror sources (recommended for users in China):
# Tsinghua University mirror
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ -r requirements.txt

# Alibaba Cloud mirror
pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

# Douban mirror
pip install -i https://pypi.douban.com/simple/ -r requirements.txt

# USTC mirror
pip install -i https://mirrors.ustc.edu.cn/pypi/web/simple/ -r requirements.txt
```

3. **Run the application**

```bash
python main.py
```

## Usage Guide

### Start the Application

```bash
python main.py
```

### Asset Management

#### Add Asset

1. Click the "Add Asset" button
2. Fill in the asset name and select the resource path
3. Select or create a category
4. Optional: Upload a cover image
5. Optional: Check to create a README document
6. Click "Save" to complete the addition

#### Manage Categories

1. Click the "Manage Categories" button
2. You can view, add and delete categories in the pop-up dialog

### Import Assets to UE Project

1. Make sure the UE project has been added
2. In the asset list, right-click on an asset card
3. Select the "Import to UE Project" option
4. Select the target UE project
5. Wait for the import to complete

### Project Management

1. Switch to the "UE Projects" page
2. Click the "Add Project" button
3. Browse and select the .uproject file
4. Click "OK" to complete the addition

### Configuration Management

This project uses a new configuration manager that supports version control and automatic migration:

1. **Automatic default configuration creation**: Automatically creates configuration files with default values on first run
2. **Version control**: Configuration files contain version numbers for tracking and management
3. **Automatic migration**: Automatically migrates old version configurations during software upgrades, preserving user data and filling new fields
4. **User data protection**: Configuration files are stored in the user's personal data directory (Windows: AppData\Roaming\UnrealManagerTools) to prevent data loss during software upgrades or replacements

For detailed usage, please refer to [Configuration Manager Usage Guide](docs/config_manager_usage.md).

## Development and Contribution

We warmly welcome developers to modify and contribute to the project! Whether it's fixing bugs, adding new features, or improving the user interface, we greatly appreciate your help.

### Package as Executable

If you want to package the project as an executable, you can use the packaging script provided by the project:

```bash
python package.py
```

This script will:

1. Install all necessary dependencies
2. Package the project as a single executable using PyInstaller
3. Create a ZIP archive containing all necessary files for easy upload to GitHub Releases

The packaged files will be located in the `dist` directory, and the ZIP archive file will be in the project root directory.

### Contribution Steps

1. Fork this repository
2. Create your feature branch
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit your changes
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. Push to the branch
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details

## Acknowledgments

- Thank all developers who have contributed to the project
- This project uses the CustomTkinter library to provide a modern UI interface
- Special thanks to the Unreal Engine community for their support and feedback

## Contact

If you have any questions or suggestions, please feel free to contact the project maintainers.

---

# 虚幻引擎资源管理器

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7%2B-blue.svg">
  <img src="https://img.shields.io/badge/Unreal%20Engine-4%2B%2F5-orange.svg">
  <img src="https://img.shields.io/badge/License-MIT-green.svg">
</p>

UE 资源管理器是一个专为虚幻引擎开发者设计的资产管理工具，**特别适合虚幻引擎新手学习和使用**。它帮助开发者高效地组织、浏览和导入 UE 项目资源，是初学者管理学习资料和项目资源的理想助手。

## 功能特性

- 📁 **资产管理**: 添加、编辑、删除和分类管理 UE 资源
- 🔍 **搜索过滤**: 根据名称和分类快速查找资源
- 📂 **一键导入**: 将资源便捷地导入到 UE 项目
- 📊 **资源预览**: 显示资源封面图片和基本信息
- 📝 **文档支持**: 自动生成和管理资源 README 文档
- 🎨 **主题切换**: 支持明暗主题切换，提升用户体验
- 🚀 **界面优化**: 预加载数据，实现快速页面切换
- ⚙️ **配置管理**: 支持版本控制和自动迁移的 JSON 配置文件管理
- 💾 **用户数据保护**: 配置文件存储在用户的个人数据目录中，避免软件升级时数据丢失

## 项目结构

```
Ue_Asset_manger/
├── README.md            # 项目说明文档
├── main.py              # 主程序入口
├── requirements.txt     # 依赖包列表
├── 测试方案.md           # 测试方案
├── docs/                # 文档和报告
│   └── *.md             # 各种报告文件
├── scripts/             # 脚本文件
│   ├── install_dependencies.py  # 安装依赖脚本
│   └── install_psutil.py        # 安装psutil脚本
├── tests/               # 测试文件
│   └── test_*.py        # 各种测试文件
├── models/              # 数据模型
│   ├── __init__.py      # 包初始化
│   ├── app_state.py     # 应用状态
│   ├── asset_manager.py # 资产管理器
│   └── project_manager.py # 项目管理器
├── views/               # 视图组件
│   ├── __init__.py      # 包初始化
│   ├── main_window.py   # 主窗口
│   ├── toolbar.py       # 工具栏
│   └── content/         # 内容页面
│       ├── __init__.py           # 包初始化
│       ├── base_content.py       # 基础内容管理器
│       ├── ue_asset_library.py   # 资产库页面
│       ├── ue_projects.py        # UE项目页面
│       ├── settings_content.py   # 设置页面
│       └── about_content.py      # 关于页面
├── widgets/             # 自定义组件
│   ├── __init__.py      # 包初始化
│   ├── asset_card.py    # 资产卡片组件
│   └── search_entry.py  # 搜索输入框组件
└── utils/               # 工具函数
    ├── __init__.py      # 包初始化
    ├── dialog_utils.py  # 对话框工具类
    ├── file_utils.py    # 文件工具类
    ├── config_manager.py # 配置管理器
    └── image_utils.py   # 图像工具类
```

## 安装与使用

### 方法一：直接下载可执行文件（推荐给普通用户）

1. 访问项目的 GitHub [Releases](https://github.com/Awfp1314/Ue_Asset_manger/releases) 页面（目前尚未发布正式版本）
2. 下载最新版本的 `UE资源管理器_Windows_x64.zip` 文件
3. 解压下载的 ZIP 文件
4. 运行 `UE资源管理器.exe` 即可开始使用

### 方法二：从源代码运行（适合开发者）

#### 前提条件

- 安装 Python 3.7 或更高版本
- 推荐安装 Git 用于版本控制

#### 安装步骤

1. **克隆仓库**

```bash
git clone https://github.com/Awfp1314/Ue_Asset_manger.git
cd Ue_Asset_manger
```

2. **安装依赖**

```bash
# 使用Python脚本安装依赖
python scripts/install_dependencies.py

# 或直接通过pip安装
# 使用默认源：
pip install -r requirements.txt

# 使用国内镜像源（推荐国内用户使用）：
# 清华大学镜像源
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ -r requirements.txt

# 阿里云镜像源
pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

# 豆瓣镜像源
pip install -i https://pypi.douban.com/simple/ -r requirements.txt

# 中科大镜像源
pip install -i https://mirrors.ustc.edu.cn/pypi/web/simple/ -r requirements.txt
```

3. **运行程序**

```bash
python main.py
```

## 使用指南

### 启动程序

```bash
python main.py
```

### 资产管理

#### 添加资产

1. 点击"添加资产"按钮
2. 填写资产名称、选择资源路径
3. 选择或创建分类
4. 可选：上传封面图片
5. 可选：勾选创建 README 文档
6. 点击"保存"完成添加

#### 管理分类

1. 点击"管理分类"按钮
2. 在弹出的对话框中可以查看、添加和删除分类

### 导入资产到 UE 项目

1. 确保已添加 UE 项目
2. 在资产列表中，右键点击一个资产卡片
3. 选择"导入到 UE 项目"选项
4. 选择目标 UE 项目
5. 等待导入完成

### 项目管理

1. 切换到"UE 项目"页面
2. 点击"添加项目"按钮
3. 浏览并选择.uproject 文件
4. 点击"确定"按钮完成添加

### 配置管理

本项目使用了新的配置管理器，支持版本控制和自动迁移功能：

1. **自动创建默认配置**：首次运行时自动创建带有默认值的配置文件
2. **版本控制**：配置文件包含版本号，便于跟踪和管理
3. **自动迁移**：软件升级时自动迁移旧版本配置，保留用户数据并填充新字段
4. **用户数据保护**：配置文件存储在用户的个人数据目录中（Windows: AppData\Roaming\UnrealManagerTools），避免软件升级或替换时数据丢失

详细使用方法请参考 [配置管理器使用指南](docs/config_manager_usage.md)。

## 开发和贡献

我们非常欢迎开发者对项目进行修改和贡献！无论是修复 bug、添加新功能，还是改进用户界面，我们都非常感谢您的帮助。

### 打包为可执行文件

如果您想将项目打包为可执行文件，可以使用项目提供的打包脚本：

```bash
python package.py
```

此脚本将：

1. 安装所有必要的依赖
2. 使用 PyInstaller 打包项目为单个可执行文件
3. 创建包含所有必要文件的 ZIP 归档，便于发布到 GitHub Releases

打包后的文件将位于 `dist` 目录中，ZIP 归档文件位于项目根目录。

### 贡献步骤

1. Fork 本仓库
2. 创建您的特性分支
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. 提交您的更改
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. 推送到分支
   ```bash
   git push origin feature/AmazingFeature
   ```
5. 开启一个 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 LICENSE 文件

## 鸣谢

- 感谢所有为项目做出贡献的开发者
- 本项目使用了 CustomTkinter 库提供现代化的 UI 界面
- 特别感谢虚幻引擎社区的支持和反馈

## 联系方式

如有任何问题或建议，请随时联系项目维护者。

---

**让我们一起学习虚幻引擎，创造精彩内容！**

**Let's learn Unreal Engine together and create amazing content!**
