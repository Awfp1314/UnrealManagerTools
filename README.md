# UE 资源管理器 / UE Asset Manager

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7%2B-blue.svg">
  <img src="https://img.shields.io/badge/Unreal%20Engine-4%2B%2F5-orange.svg">
  <img src="https://img.shields.io/badge/License-MIT-green.svg">
</p>

## 项目介绍 / Project Introduction

UE 资源管理器是一个专为虚幻引擎开发者设计的资产管理工具，**特别适合虚幻引擎新手学习和使用**。它帮助开发者高效地组织、浏览和导入 UE 项目资源，是初学者管理学习资料和项目资源的理想助手。

UE Asset Manager is a resource management tool designed specifically for Unreal Engine developers, **especially suitable for beginners learning Unreal Engine**. It helps developers efficiently organize, browse, and import UE project resources, making it an ideal assistant for beginners to manage learning materials and project resources.

## 功能特性 / Features

- 📁 **资产管理 / Asset Management**: 添加、编辑、删除和分类管理 UE 资源 / Add, edit, delete and categorize UE resources
- 🔍 **搜索过滤 / Search & Filter**: 根据名称和分类快速查找资源 / Quickly find resources by name and category
- 📂 **一键导入 / One-click Import**: 将资源便捷地导入到 UE 项目 / Easily import resources to UE projects
- 📊 **资源预览 / Resource Preview**: 显示资源封面图片和基本信息 / Display resource cover images and basic information
- 📝 **文档支持 / Documentation Support**: 自动生成和管理资源 README 文档 / Automatically generate and manage resource README documents
- 🎨 **主题切换 / Theme Switching**: 支持明暗主题切换，提升用户体验 / Support light and dark theme switching to enhance user experience
- 🚀 **界面优化 / UI Optimization**: 预加载数据，实现快速页面切换 / Preload data for fast page switching

## 项目结构 / Project Structure

```
Ue_Asset_manger/
├── README.md            # 项目说明文档 / Project documentation
├── main.py              # 主程序入口 / Main program entry
├── requirements.txt     # 依赖包列表 / Dependencies list
├── ue_assets.json       # 资产数据文件 / Asset data file
├── ue_projects.json     # 项目数据文件 / Project data file
├── 测试方案.md           # 测试方案 / Test plan
├── docs/                # 文档和报告 / Documents and reports
│   └── *.md             # 各种报告文件 / Various report files
├── scripts/             # 脚本文件 / Script files
│   ├── install_dependencies.py  # 安装依赖脚本 / Install dependencies script
│   └── install_psutil.py        # 安装psutil脚本 / Install psutil script
├── tests/               # 测试文件 / Test files
│   └── test_*.py        # 各种测试文件 / Various test files
├── models/              # 数据模型 / Data models
│   ├── __init__.py      # 包初始化 / Package initialization
│   ├── app_state.py     # 应用状态 / Application state
│   ├── asset_manager.py # 资产管理器 / Asset manager
│   └── project_manager.py # 项目管理器 / Project manager
├── views/               # 视图组件 / View components
│   ├── __init__.py      # 包初始化 / Package initialization
│   ├── main_window.py   # 主窗口 / Main window
│   ├── toolbar.py       # 工具栏 / Toolbar
│   └── content/         # 内容页面 / Content pages
│       ├── __init__.py           # 包初始化 / Package initialization
│       ├── base_content.py       # 基础内容管理器 / Base content manager
│       ├── ue_asset_library.py   # 资产库页面 / Asset library page
│       ├── ue_projects.py        # UE项目页面 / UE projects page
│       ├── settings_content.py   # 设置页面 / Settings page
│       └── about_content.py      # 关于页面 / About page
├── widgets/             # 自定义组件 / Custom widgets
│   ├── __init__.py      # 包初始化 / Package initialization
│   ├── asset_card.py    # 资产卡片组件 / Asset card component
│   └── search_entry.py  # 搜索输入框组件 / Search entry component
└── utils/               # 工具函数 / Utility functions
    ├── __init__.py      # 包初始化 / Package initialization
    ├── dialog_utils.py  # 对话框工具类 / Dialog utility class
    ├── file_utils.py    # 文件工具类 / File utility class
    └── image_utils.py   # 图像工具类 / Image utility class
```

## 安装与使用 / Installation & Usage

### 方法一：直接下载可执行文件（推荐给普通用户）

1. 访问项目的 GitHub [Releases](https://github.com/Awfp1314/Ue_Asset_manger/releases) 页面（目前尚未发布正式版本）
2. 下载最新版本的 `UE资源管理器_Windows_x64.zip` 文件
3. 解压下载的 ZIP 文件
4. 运行 `UE资源管理器.exe` 即可开始使用

### 方法二：从源代码运行（适合开发者）

#### 前提条件 / Prerequisites

- 安装 Python 3.7 或更高版本 / Install Python 3.7 or higher
- 推荐安装 Git 用于版本控制 / Git is recommended for version control

#### 安装步骤 / Installation Steps

1. **克隆仓库 / Clone the repository**

```bash
# 中文 / Chinese
git clone https://github.com/Awfp1314/Ue_Asset_manger.git
cd Ue_Asset_manger

# 英文 / English
git clone https://github.com/Awfp1314/Ue_Asset_manger.git
cd Ue_Asset_manger
```

2. **安装依赖 / Install dependencies**

```bash
# 使用Python脚本安装依赖 / Install dependencies using Python script
python scripts/install_dependencies.py

# 或直接通过pip安装 / Or install directly via pip
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

3. **运行程序 / Run the application**

```bash
python main.py
```

## 使用指南 / Usage Guide

### 启动程序 / Start the Application

```bash
python main.py
```

### 资产管理 / Asset Management

#### 添加资产 / Add Asset

1. 点击"添加资产"按钮 / Click the "Add Asset" button
2. 填写资产名称、选择资源路径 / Fill in the asset name and select the resource path
3. 选择或创建分类 / Select or create a category
4. 可选：上传封面图片 / Optional: Upload a cover image
5. 可选：勾选创建 README 文档 / Optional: Check to create a README document
6. 点击"保存"完成添加 / Click "Save" to complete the addition

#### 管理分类 / Manage Categories

1. 点击"管理分类"按钮 / Click the "Manage Categories" button
2. 在弹出的对话框中可以查看、添加和删除分类 / You can view, add and delete categories in the pop-up dialog

### 导入资产到 UE 项目 / Import Assets to UE Project

1. 确保已添加 UE 项目 / Make sure the UE project has been added
2. 在资产列表中，右键点击一个资产卡片 / In the asset list, right-click on an asset card
3. 选择"导入到 UE 项目"选项 / Select the "Import to UE Project" option
4. 选择目标 UE 项目 / Select the target UE project
5. 等待导入完成 / Wait for the import to complete

### 项目管理 / Project Management

1. 切换到"UE 项目"页面 / Switch to the "UE Projects" page
2. 点击"添加项目"按钮 / Click the "Add Project" button
3. 浏览并选择.uproject 文件 / Browse and select the .uproject file
4. 点击"确定"按钮完成添加 / Click "OK" to complete the addition

## 为新手准备的学习提示 / Learning Tips for Beginners

- **资源分类 / Resource Categorization**: 根据学习阶段或资源类型（如材质、蓝图、模型等）创建分类，便于查找和管理 / Create categories based on learning stages or resource types (such as materials, blueprints, models, etc.) for easy finding and management
- **文档记录 / Documentation**: 为重要资源创建 README 文档，记录学习心得和使用方法 / Create README documents for important resources to record learning experiences and usage methods
- **定期整理 / Regular Organization**: 定期整理资源库，删除不需要的资源，更新资源信息 / Regularly organize the resource library, delete unnecessary resources, and update resource information

## 开发和贡献 / Development and Contribution

我们非常欢迎开发者对项目进行修改和贡献！无论是修复 bug、添加新功能，还是改进用户界面，我们都非常感谢您的帮助。

We warmly welcome developers to modify and contribute to the project! Whether it's fixing bugs, adding new features, or improving the user interface, we greatly appreciate your help.

### 打包为可执行文件 / Package as Executable

如果您想将项目打包为可执行文件，可以使用项目提供的打包脚本：

```bash
python package.py
```

此脚本将：

1. 安装所有必要的依赖
2. 使用 PyInstaller 打包项目为单个可执行文件
3. 创建包含所有必要文件的 ZIP 归档，便于发布到 GitHub Releases

打包后的文件将位于 `dist` 目录中，ZIP 归档文件位于项目根目录。

### 贡献步骤 / Contribution Steps

1. Fork 本仓库 / Fork this repository
2. 创建您的特性分支 / Create your feature branch
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. 提交您的更改 / Commit your changes
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. 推送到分支 / Push to the branch
   ```bash
   git push origin feature/AmazingFeature
   ```
5. 开启一个 Pull Request / Open a Pull Request

## 许可证 / License

本项目采用 MIT 许可证 - 详见 LICENSE 文件 / This project is licensed under the MIT License - see the LICENSE file for details

## 鸣谢 / Acknowledgments

- 感谢所有为项目做出贡献的开发者 / Thank all developers who have contributed to the project
- 本项目使用了 CustomTkinter 库提供现代化的 UI 界面 / This project uses the CustomTkinter library to provide a modern UI interface
- 特别感谢虚幻引擎社区的支持和反馈 / Special thanks to the Unreal Engine community for their support and feedback

## 联系方式 / Contact

如有任何问题或建议，请随时联系项目维护者。

If you have any questions or suggestions, please feel free to contact the project maintainers.

---

**让我们一起学习虚幻引擎，创造精彩内容！**

**Let's learn Unreal Engine together and create amazing content!**
