#!/usr/bin/env python3
"""
苹果格式图片转换工具
支持将HEIC/HEIF格式转换为JPG/PNG等通用格式
"""

import os
import argparse
from pathlib import Path
from PIL import Image
import pillow_heif

# 注册HEIF插件
pillow_heif.register_heif_opener()

def convert_heic_to_image(input_path, output_path, format="JPEG", quality=90, delete_original=False):
    """
    将HEIC/HEIF图片转换为指定格式
    
    Args:
        input_path (Path): 输入文件路径
        output_path (Path): 输出文件路径
        format (str): 输出格式，默认为JPEG
        quality (int): 输出质量，0-100，默认为90
        delete_original (bool): 是否删除原文件，默认为False
    """
    try:
        # 打开HEIC文件
        with Image.open(input_path) as img:
            # 转换并保存
            img.save(output_path, format=format, quality=quality, exif=img.info.get('exif'))
        
        # 删除原文件（如果需要）
        if delete_original:
            input_path.unlink()
        
        return True
    except Exception as e:
        print(f"转换失败 {input_path}: {e}")
        return False

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='苹果HEIC/HEIF图片转换工具')
    parser.add_argument('input', type=str, help='输入文件或目录')
    parser.add_argument('-o', '--output', type=str, help='输出目录，默认为输入目录')
    parser.add_argument('-f', '--format', type=str, default='JPEG', choices=['JPEG', 'PNG', 'WEBP'], help='输出格式')
    parser.add_argument('-q', '--quality', type=int, default=90, help='输出质量，0-100')
    parser.add_argument('-d', '--delete', action='store_true', help='转换后删除原文件')
    parser.add_argument('-r', '--recursive', action='store_true', help='递归处理子目录')
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    
    # 确定输出目录
    if args.output:
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = input_path.parent if input_path.is_file() else input_path
    
    # 收集所有HEIC文件
    heic_files = []
    if input_path.is_file():
        if input_path.suffix.lower() in ['.heic', '.heif']:
            heic_files.append(input_path)
    else:
        pattern = '**/*' if args.recursive else '*'
        for ext in ['.heic', '.heif']:
            heic_files.extend(input_path.glob(f'{pattern}{ext}'))
            heic_files.extend(input_path.glob(f'{pattern}{ext.upper()}'))
    
    if not heic_files:
        print("未找到HEIC/HEIF文件")
        return
    
    print(f"找到 {len(heic_files)} 个HEIC/HEIF文件")
    
    # 转换文件
    success_count = 0
    print("开始转换...")
    for i, heic_file in enumerate(heic_files):
        # 确定输出文件名
        if args.output:
            # 如果指定了输出目录，保持原文件名
            output_filename = heic_file.name.replace(heic_file.suffix, f'.{args.format.lower()}')
            output_path = output_dir / output_filename
        else:
            # 如果未指定输出目录，替换原文件后缀
            output_path = heic_file.with_suffix(f'.{args.format.lower()}')
        
        # 转换文件
        if convert_heic_to_image(heic_file, output_path, args.format, args.quality, args.delete):
            success_count += 1
        
        # 显示转换进度
        if (i + 1) % 10 == 0 or (i + 1) == len(heic_files):
            print(f"转换进度: {i + 1}/{len(heic_files)}")
    
    print(f"转换完成：成功 {success_count} 个，失败 {len(heic_files) - success_count} 个")

if __name__ == "__main__":
    main()