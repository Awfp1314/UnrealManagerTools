from PIL import Image, ImageTk, ImageDraw
import customtkinter as ctk
import os

class ImageUtils:
    def __init__(self):
        self.thumbnail_cache = {}

    def load_thumbnail(self, cover_path, size):
        """加载缩略图"""
        if cover_path and os.path.exists(cover_path):
            try:
                # 检查缓存
                cache_key = f"{cover_path}_{size[0]}_{size[1]}"
                if cache_key in self.thumbnail_cache:
                    return self.thumbnail_cache[cache_key]
                
                img = Image.open(cover_path)
                
                # 创建圆角矩形缩略图
                img = self.create_rounded_thumbnail(img, size)
                
                # 使用CTkImage来避免警告
                ctk_image = ctk.CTkImage(light_image=img, dark_image=img, size=size)
                self.thumbnail_cache[cache_key] = ctk_image
                return ctk_image
            except Exception as e:
                import logging
                logging.error(f"加载缩略图错误: {e}")
        
        # 返回默认图片
        default_img = self.create_default_thumbnail(size)
        return ctk.CTkImage(light_image=default_img, dark_image=default_img, size=size)

    def create_rounded_thumbnail(self, img, size):
        """创建圆角矩形缩略图"""
        img = img.resize(size, Image.LANCZOS)
        
        # 创建圆角遮罩
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        
        # 绘制圆角矩形
        radius = 10
        draw.rounded_rectangle([(0, 0), size], radius=radius, fill=255)
        
        # 应用圆角
        result = Image.new('RGBA', size, (0, 0, 0, 0))
        result.putalpha(mask)
        result.paste(img, (0, 0), mask)
        
        return result

    def create_default_thumbnail(self, size):
        """创建更精美的默认缩略图"""
        width, height = size
        img = Image.new('RGBA', size, color='#2b2b2b')
        draw = ImageDraw.Draw(img)
        
        # 绘制背景渐变
        for i in range(height):
            ratio = i / height
            r = int(43 + (33 - 43) * ratio)
            g = int(43 + (33 - 43) * ratio)
            b = int(43 + (33 - 43) * ratio)
            draw.line([(0, i), (width, i)], fill=(r, g, b))
        
        # 绘制文件夹图标
        folder_color = (100, 150, 255)  # 蓝色文件夹
        icon_size = min(size) // 2
        
        # 文件夹主体
        x1 = (width - icon_size) // 2
        y1 = (height - icon_size) // 2
        x2 = x1 + icon_size
        y2 = y1 + icon_size
        
        # 绘制文件夹底部
        folder_bottom = [(x1, y1 + icon_size//3), (x2, y2)]
        draw.rounded_rectangle(folder_bottom, radius=5, fill=folder_color)
        
        # 绘制文件夹顶部（标签部分）
        folder_top = [(x1 + icon_size//6, y1), (x2 - icon_size//6, y1 + icon_size//3)]
        draw.rounded_rectangle(folder_top, radius=3, fill=folder_color)
        
        # 添加一些细节线条
        draw.line([(x1 + icon_size//3, y1 + icon_size//3), 
                  (x2 - icon_size//3, y1 + icon_size//3)], 
                  fill=(80, 130, 235), width=2)
        
        # 添加文件图标在文件夹上方
        file_size = icon_size // 3
        file_x = x1 + icon_size//2 - file_size//2
        file_y = y1 + icon_size//4
        draw.rectangle([file_x, file_y, file_x + file_size, file_y + file_size//1.5], 
                      fill=(200, 200, 200), outline=(150, 150, 150), width=1)
        
        # 添加文件折角
        draw.polygon([(file_x + file_size*0.7, file_y), 
                     (file_x + file_size, file_y), 
                     (file_x + file_size, file_y + file_size*0.3)], 
                     fill=(180, 180, 180))
        
        return img

    def clear_cache(self):
        """清除缩略图缓存"""
        self.thumbnail_cache.clear()