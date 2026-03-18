#!/usr/bin/env python3
"""
苹果格式图片转换工具 - Web API版
使用Flask框架将HEIC/HEIF图片转换功能封装为REST API
"""

import os
import tempfile
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
from heic_converter import convert_heic_to_image

# 创建Flask应用
app = Flask(__name__)

# 配置上传文件大小限制（100MB）
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

# 允许的上传文件扩展名
ALLOWED_EXTENSIONS = {'heic', 'heif'}

# 允许的输出格式
ALLOWED_FORMATS = {'JPEG', 'PNG', 'WEBP'}

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """API根路径，返回帮助信息"""
    return jsonify({
        "message": "苹果HEIC/HEIF图片转换API",
        "endpoints": {
            "/convert": "POST - 转换HEIC/HEIF图片",
            "/": "GET - 查看API帮助"
        },
        "usage": {
            "method": "POST",
            "endpoint": "/convert",
            "form_data": {
                "file": "HEIC/HEIF图片文件",
                "format": "输出格式 (JPEG/PNG/WEBP，默认JPEG)",
                "quality": "输出质量 (0-100，默认90)"
            },
            "response": "转换后的图片文件"
        }
    })

@app.route('/convert', methods=['POST'])
def convert():
    """图片转换API端点"""
    try:
        # 检查是否有文件上传
        if 'file' not in request.files:
            return jsonify({"error": "没有文件上传"}), 400
        
        file = request.files['file']
        
        # 检查文件名是否为空
        if file.filename == '':
            return jsonify({"error": "没有选择文件"}), 400
        
        # 检查文件类型是否允许
        if not allowed_file(file.filename):
            return jsonify({"error": "不支持的文件类型，仅支持HEIC/HEIF格式"}), 400
        
        # 获取转换参数
        output_format = request.form.get('format', 'JPEG').upper()
        if output_format not in ALLOWED_FORMATS:
            return jsonify({"error": f"不支持的输出格式，仅支持{', '.join(ALLOWED_FORMATS)}"}), 400
        
        quality = request.form.get('quality', 90)
        try:
            quality = int(quality)
            if not (0 <= quality <= 100):
                raise ValueError()
        except ValueError:
            return jsonify({"error": "质量参数必须是0-100之间的整数"}), 400
        
        # 创建临时目录用于处理文件
        temp_dir = tempfile.mkdtemp()
        temp_dir_path = Path(temp_dir)
        
        try:
            # 保存上传的文件
            filename = secure_filename(file.filename)
            input_path = temp_dir_path / filename
            file.save(input_path)
            
            # 生成输出文件名
            output_filename = filename.rsplit('.', 1)[0] + f'.{output_format.lower()}'
            output_path = temp_dir_path / output_filename
            
            # 执行转换
            success = convert_heic_to_image(input_path, output_path, output_format, quality, delete_original=False)
            
            if not success:
                return jsonify({"error": "图片转换失败"}), 500
            
            # 返回转换后的文件
            return send_file(
                output_path,
                mimetype=f'image/{output_format.lower()}',
                as_attachment=True,
                attachment_filename=output_filename
            )
        finally:
            # 延迟删除临时目录，确保文件发送完成
            import shutil
            import threading
            
            def cleanup_temp_dir():
                try:
                    shutil.rmtree(temp_dir)
                except:
                    pass
            
            # 10秒后删除临时目录
            threading.Timer(10.0, cleanup_temp_dir).start()
            
    except Exception as e:
        return jsonify({"error": f"服务器内部错误: {str(e)}"}), 500

if __name__ == '__main__':
    # 启动Flask开发服务器
    app.run(host='0.0.0.0', port=5000, debug=True)
