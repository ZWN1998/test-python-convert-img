# 苹果格式图片转换工具

一个简单易用的Python脚本，用于将苹果设备拍摄的HEIC/HEIF格式图片转换为JPG/PNG等通用格式。

## 功能特性

- ✅ 支持单个文件转换
- ✅ 支持目录批量转换
- ✅ 支持递归转换子目录
- ✅ 支持多种输出格式（JPEG/PNG/WEBP）
- ✅ 支持自定义输出质量
- ✅ 支持保留图片元数据
- ✅ 支持转换后删除原文件
- ✅ 清晰的转换进度显示
- ✅ 简单易用的命令行接口

## 安装依赖

在使用脚本之前，需要安装以下依赖库：

```bash
pip install pillow_heif pillow tqdm
```

如果遇到SSL证书问题，可以尝试使用国内镜像源：

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pillow_heif pillow tqdm
```

## 使用方法

### 基本用法

```bash
# 转换单个HEIC文件为JPG
python heic_converter.py input.heic

# 转换整个目录的HEIC文件
python heic_converter.py input_directory
```

### 命令行参数

| 参数 | 缩写 | 描述 | 默认值 |
|------|------|------|--------|
| `input` | - | 输入文件或目录路径 | 必填 |
| `--output` | `-o` | 输出目录，默认为输入目录 | 输入目录 |
| `--format` | `-f` | 输出格式（JPEG/PNG/WEBP） | JPEG |
| `--quality` | `-q` | 输出质量（0-100） | 90 |
| `--delete` | `-d` | 转换后删除原文件 | False |
| `--recursive` | `-r` | 递归处理子目录 | False |
| `--help` | `-h` | 显示帮助信息 | - |

## 示例用法

### 1. 转换单个文件

```bash
# 转换为JPG格式（默认）
python heic_converter.py photo.heic

# 转换为PNG格式
python heic_converter.py photo.heic -f PNG

# 转换为WEBP格式并设置质量为85
python heic_converter.py photo.heic -f WEBP -q 85
```

### 2. 转换目录中的所有文件

```bash
# 转换当前目录下的所有HEIC文件
python heic_converter.py .

# 转换指定目录下的所有HEIC文件
python heic_converter.py ./photos

# 递归转换目录及其子目录下的所有HEIC文件
python heic_converter.py ./photos -r
```

### 3. 指定输出目录

```bash
# 将转换后的文件保存到output目录
python heic_converter.py photo.heic -o ./output

# 批量转换到指定目录
python heic_converter.py ./photos -o ./converted -r
```

### 4. 转换后删除原文件

```bash
# 转换后删除原HEIC文件
python heic_converter.py photo.heic -d

# 批量转换并删除原文件
python heic_converter.py ./photos -d -r
```

## 注意事项

1. **依赖安装**：确保已正确安装所有依赖库
2. **文件权限**：确保脚本有读取输入文件和写入输出目录的权限
3. **备份文件**：在使用`-d`参数删除原文件前，建议先备份重要图片
4. **转换质量**：JPEG格式建议使用80-95的质量值，PNG格式为无损压缩，质量值无效
5. **转换速度**：转换大量或大尺寸图片时，可能需要较长时间，请耐心等待
6. **元数据保留**：默认会保留图片的EXIF元数据（如拍摄时间、位置等）

## 输出示例

```
$ python heic_converter.py ./photos -r -o ./converted
找到 156 个HEIC/HEIF文件
转换进度: 100%|████████████████████████████████| 156/156 [00:12<00:00, 12.83it/s]
转换完成：成功 156 个，失败 0 个
```

## 系统要求

- Python 3.7 或更高版本
- Windows/macOS/Linux 系统
- 足够的磁盘空间用于存储转换后的文件

## 常见问题

### Q: 为什么转换失败？
A: 可能的原因包括：
- 输入文件不是有效的HEIC/HEIF格式
- 缺少依赖库
- 文件权限不足
- 磁盘空间不足

### Q: 转换后的图片质量如何？
A: 可以通过`-q`参数调整输出质量，默认值为90，建议根据实际需求调整。

### Q: 支持哪些输出格式？
A: 当前支持JPEG、PNG和WEBP三种格式。

## 许可证

本项目采用MIT许可证，您可以自由使用、修改和分发。

## 贡献

欢迎提交Issue和Pull Request来改进这个工具！

## 更新日志

### v1.0.0
- 初始版本
- 支持HEIC/HEIF到JPEG/PNG/WEBP的转换
- 支持单个文件和批量转换
- 支持递归转换子目录
- 支持自定义输出质量
- 支持删除原文件

## 联系方式

如有问题或建议，欢迎通过以下方式联系：
- 创建GitHub Issue
- 发送邮件至：your-email@example.com

---

**祝您使用愉快！** 📸