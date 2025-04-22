# SnapText

SnapText 是一个批量截图文字处理工具，可以帮助你在图片上快速添加文字，特别适合需要批量处理图片的场景。

## 功能特点

- 🖼️ 灵活的截图功能
  - 支持区域截图
  - 支持导入已有图片
  - 支持高分辨率显示器

- 📝 强大的文字处理
  - 支持多个文字位置
  - 支持自定义字体和颜色
  - 支持批量数据导入（CSV格式）

- 🎨 现代化界面
  - 支持亮色/暗色主题
  - 简洁直观的操作流程
  - 实时预览效果

## 使用说明

1. **选择图片**
   - 点击"选择截图区域"进行屏幕截图
   - 或点击"导入已有图片"选择本地图片

2. **导入数据**
   - 准备CSV格式的文本数据
   - 点击"导入文本数据"选择CSV文件
   - CSV文件中每行对应一张图片的文字内容

3. **设置文字位置**
   - 设置需要添加文字的位置数量
   - 点击"选择所有文字位置"
   - 在图片上点击选择文字位置
   - 可以设置每个位置的字体和颜色

4. **生成图片**
   - 设置要处理的数据组数
   - 点击"生成带文字截图"
   - 选择保存位置
   - 等待处理完成

## CSV 文件格式

```csv
张三,25岁,工程师
李四,30岁,设计师
王五,28岁,产品经理
```

- 使用UTF-8编码保存文件
- 每行代表一组数据
- 数据之间用逗号分隔
- 数据顺序要与文字位置一一对应

## 系统要求

- Windows 10/11 64位
- macOS 10.14 或更高版本
- 屏幕分辨率：1280 x 720 或更高

## 下载安装

访问 [Releases](https://github.com/Kerepain/SnapText/releases) 页面下载最新版本：

- Windows: `SnapText.exe`
- macOS: `SnapText.app`

## 开发说明

### 环境配置

```bash
# 克隆仓库
git clone https://github.com/Kerepain/SnapText.git
cd SnapText

# 安装依赖
pip install -r requirements.txt
```

### 运行开发版本

```bash
python src/main.py
```

### 构建可执行文件

```bash
# Windows
pyinstaller SnapText.spec

# macOS
pyinstaller SnapText.spec
```

## 技术栈

- Python 3.9
- PyQt6
- Pillow
- pyautogui
- PyInstaller

## 版权和许可

Copyright (c) 2024 Kerepain

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。

## 贡献

欢迎提交问题和改进建议！如果您想贡献代码，请遵循以下步骤：

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 联系方式

如有任何问题或建议，请通过以下方式联系：

- 提交 Issue
- 发送邮件至：your-email@example.com 