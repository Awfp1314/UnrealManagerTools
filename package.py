import os
import shutil
import sys
import subprocess
import platform
from pathlib import Path

# 确保中文正常显示
os.environ['PYTHONIOENCODING'] = 'utf-8'

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# 在桌面创建统一的打包目录
PACKAGING_DIR = os.path.join(os.path.expanduser('~'), 'Desktop', 'UE_Asset_Manager_Packaging')

# 输出目录（修改到统一打包目录内，避免污染源代码和桌面）
OUTPUT_DIR = os.path.join(PACKAGING_DIR, 'dist')
BUILD_DIR = os.path.join(PACKAGING_DIR, 'build')

# 检查是否安装了PyInstaller
def check_pyinstaller():
    try:
        import PyInstaller
        return True
    except ImportError:
        print("PyInstaller未安装，正在尝试安装...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
        return True

def clear_old_files():
    """清理旧的打包文件"""
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
        print(f"已清理旧的输出目录: {OUTPUT_DIR}")
    
    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)
        print(f"已清理旧的构建目录: {BUILD_DIR}")
    
    # 提示用户统一打包目录的位置
    print(f"所有打包文件将位于: {PACKAGING_DIR}")
    
    # 清理.spec文件（保留在项目目录中，因为PyInstaller需要在项目根目录生成）
    spec_file = os.path.join(PROJECT_ROOT, 'ue_asset_manager.spec')
    if os.path.exists(spec_file):
        os.remove(spec_file)
        print(f"已清理旧的spec文件: {spec_file}")

def create_icon_file():
    """创建应用图标（修改到统一打包目录内，避免污染源代码和桌面）"""
    # 确保打包目录存在
    os.makedirs(PACKAGING_DIR, exist_ok=True)
    icon_path = os.path.join(PACKAGING_DIR, 'app_icon.ico')
    
    # 如果没有图标文件，创建一个简单的SVG图标并转换为ico
    if not os.path.exists(icon_path):
        print("正在创建应用图标...")
        
        # 首先创建SVG图标
        svg_content = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <rect width="256" height="256" fill="#1A1A1A"/>
  <path d="M168,40H88A24,24,0,0,0,64,64V208a24,24,0,0,0,24,24h80a24,24,0,0,0,24-24V64A24,24,0,0,0,168,40Zm8,168a8,8,0,0,1-8,8H88a8,8,0,0,1-8-8V64a8,8,0,0,1,8-8h80a8,8,0,0,1,8,8Zm-16-120V176H96V88Z" fill="#4F46E5"/>
  <path d="M160,96H96v64h64Z" fill="#7C3AED"/>
  <path d="M112,112h32v32H112Z" fill="#C4B5FD"/>
</svg>
        '''
        
        svg_path = os.path.join(PACKAGING_DIR, 'app_icon.svg')
        with open(svg_path, 'w', encoding='utf-8') as f:
            f.write(svg_content.strip())
        
        # 尝试使用pillow转换SVG为ICO
        try:
            from PIL import Image, ImageDraw
            
            # 创建一个临时的PNG图像
            img = Image.new('RGBA', (256, 256), color='#1A1A1A')
            draw = ImageDraw.Draw(img)
            
            # 绘制简单的图标
            draw.rectangle([48, 48, 208, 208], fill='#4F46E5')
            draw.rectangle([64, 64, 192, 176], fill='#7C3AED')
            draw.rectangle([80, 80, 144, 144], fill='#C4B5FD')
            
            # 保存为ICO
            img.save(icon_path)
            print(f"已创建应用图标: {icon_path}")
            
            # 清理临时SVG文件
            if os.path.exists(svg_path):
                os.remove(svg_path)
        except Exception as e:
            print(f"创建图标失败: {e}")
            # 如果失败，使用默认图标
            icon_path = None
    
    return icon_path

def package_as_exe():
    """使用PyInstaller打包为可执行文件"""
    check_pyinstaller()
    clear_old_files()
    
    # 获取图标路径
    icon_path = create_icon_file()
    
    # 构建PyInstaller命令
    cmd = [
        'pyinstaller',
        '--onefile',  # 打包成单个文件
        '--windowed',  # 无控制台窗口
        '--name', 'UE资源管理器',
        '--distpath', OUTPUT_DIR,  # 指定输出目录
        '--workpath', BUILD_DIR,   # 指定构建目录
        '--add-data', f'{os.path.join(PROJECT_ROOT, "ue_assets.json")};.',
        '--add-data', f'{os.path.join(PROJECT_ROOT, "ue_projects.json")};.',
    ]
    
    # 添加图标
    if icon_path and os.path.exists(icon_path):
        cmd.extend(['--icon', icon_path])
    
    # 添加主程序文件
    cmd.append(os.path.join(PROJECT_ROOT, 'main.py'))
    
    print(f"开始打包应用程序...")
    print(f"执行命令: {' '.join(cmd)}")
    
    try:
        # 执行打包命令
        subprocess.run(cmd, check=True, cwd=PROJECT_ROOT)
        
        # 复制必要的数据文件到输出目录
        if os.path.exists(OUTPUT_DIR):
            # 检查是否有ue_assets.json文件，如果没有则创建空文件
            assets_file = os.path.join(PROJECT_ROOT, 'ue_assets.json')
            if not os.path.exists(assets_file):
                with open(assets_file, 'w', encoding='utf-8') as f:
                    f.write('{"resources": [], "categories": []}')
                print(f"已创建空的资产数据文件: {assets_file}")
            
            # 检查是否有ue_projects.json文件，如果没有则创建空文件
            projects_file = os.path.join(PROJECT_ROOT, 'ue_projects.json')
            if not os.path.exists(projects_file):
                with open(projects_file, 'w', encoding='utf-8') as f:
                    f.write('{"projects": []}')
                print(f"已创建空的项目数据文件: {projects_file}")
            
            print(f"\n应用程序打包成功！")
            print(f"可执行文件位置: {os.path.join(OUTPUT_DIR, 'UE资源管理器.exe' if platform.system() == 'Windows' else 'UE资源管理器')}")
            print(f"所有打包文件都位于: {PACKAGING_DIR}")
            print(f"\n使用说明:")
            print(f"1. 运行UE资源管理器.exe即可启动程序")
            print(f"2. 首次运行时会自动创建必要的数据文件")
            print(f"3. 注意：请确保ue_assets.json和ue_projects.json文件与可执行文件在同一目录下")
    except subprocess.CalledProcessError as e:
        print(f"打包失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"发生错误: {e}")
        sys.exit(1)

def create_release_archive():
    """创建发布归档文件"""
    try:
        # 确保输出目录存在
        if not os.path.exists(OUTPUT_DIR):
            print("输出目录不存在，先运行打包命令")
            package_as_exe()
            
        # 创建归档文件（修改到统一打包目录内，避免污染源代码和桌面）
        archive_name = f"UE资源管理器_{platform.system()}_{platform.architecture()[0]}"
        archive_path = os.path.join(PACKAGING_DIR, archive_name)
        
        # 复制可执行文件
        exe_name = 'UE资源管理器.exe' if platform.system() == 'Windows' else 'UE资源管理器'
        exe_path = os.path.join(OUTPUT_DIR, exe_name)
        
        if os.path.exists(exe_path):
            # 创建临时目录用于归档
            temp_dir = os.path.join(PROJECT_ROOT, 'temp_release')
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            os.makedirs(temp_dir)
            
            # 复制文件到临时目录
            shutil.copy2(exe_path, os.path.join(temp_dir, exe_name))
            
            # 复制数据文件
            data_files = ['ue_assets.json', 'ue_projects.json']
            for data_file in data_files:
                src_path = os.path.join(PROJECT_ROOT, data_file)
                if os.path.exists(src_path):
                    shutil.copy2(src_path, os.path.join(temp_dir, data_file))
                else:
                    # 创建空数据文件
                    with open(os.path.join(temp_dir, data_file), 'w', encoding='utf-8') as f:
                        if data_file == 'ue_assets.json':
                            f.write('{"resources": [], "categories": []}')
                        else:
                            f.write('{"projects": []}')
            
            # 复制README文件
            readme_path = os.path.join(PROJECT_ROOT, 'README.md')
            if os.path.exists(readme_path):
                shutil.copy2(readme_path, os.path.join(temp_dir, 'README.md'))
            
            # 创建ZIP归档
            shutil.make_archive(archive_path, 'zip', temp_dir)
            
            # 清理临时目录
            shutil.rmtree(temp_dir)
            
            print(f"\n发布归档文件创建成功: {archive_path}.zip")
            print(f"这个ZIP文件包含了所有必要的文件，可以直接上传到GitHub的Release页面")
            print(f"所有打包文件都位于: {PACKAGING_DIR}")
        else:
            print(f"可执行文件不存在: {exe_path}")
    except Exception as e:
        print(f"创建归档文件失败: {e}")

def main():
    """主函数"""
    print("===== UE资源管理器打包工具 =====")
    
    # 检查是否有--check参数
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        print("运行依赖检查模式...")
        
        # 检查requirements.txt是否存在
        requirements_path = os.path.join(PROJECT_ROOT, 'requirements.txt')
        if not os.path.exists(requirements_path):
            print("错误: 未找到requirements.txt文件")
            sys.exit(1)
            
        # 检查依赖
        print("\n正在检查项目依赖...")
        try:
            # 使用pip check检查依赖
            result = subprocess.run([sys.executable, '-m', 'pip', 'check'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("[OK] 所有依赖都已正确安装！")
                print("依赖检查通过！")
                sys.exit(0)
            else:
                print(f"[ERROR] 发现依赖问题:\n{result.stdout}")
                print("尝试安装requirements.txt中的依赖...")
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_path])
                print("依赖安装成功！")
                sys.exit(0)
        except Exception as e:
            print(f"[ERROR] 依赖检查或安装失败: {e}")
            sys.exit(1)
    
    # 完整打包流程
    # 首先安装所有依赖
    print("\n正在安装项目依赖...")
    try:
        requirements_path = os.path.join(PROJECT_ROOT, 'requirements.txt')
        if os.path.exists(requirements_path):
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_path])
            print("依赖安装成功！")
        else:
            print("未找到requirements.txt文件，跳过依赖安装")
    except Exception as e:
        print(f"依赖安装失败: {e}")
        print("继续尝试打包...")
    
    # 打包成可执行文件
    package_as_exe()
    
    # 创建发布归档文件
    create_release_archive()
    
    print("\n===== 打包完成 =====")
    print("您现在可以:")
    print("1. 将生成的ZIP文件上传到GitHub的Release页面")
    print("2. 在README.md中添加下载链接")
    print("3. 告诉用户如何下载和使用您的程序")
    print(f"所有打包文件都位于: {PACKAGING_DIR}")

if __name__ == '__main__':
    main()