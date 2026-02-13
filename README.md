# RapidOCR Demo

基于 RapidOCR 的文字识别演示应用，提供简洁易用的 Web 界面进行 OCR 测试验证。

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/WalleV/rapidocr-colab-demo/blob/master/main.ipynb)

## 功能特性

- 📤 图片上传和识别
- 🎨 彩色半透明检测框可视化
- 📊 置信度评分显示
- ⏱️ 识别耗时统计
- 🌐 Gradio Web 界面

## 快速开始

### 本地运行

1. 安装依赖：
```bash
uv sync
```

2. 运行应用：
```bash
uv run python main.py
```

3. 打开浏览器访问：http://localhost:7860

### Colab 运行

点击上方 "Open In Colab" 按钮，在 Google Colab 中一键运行。

## 项目结构

```
.
├── main.py           # 本地运行的主程序
├── main.ipynb        # Colab notebook 版本
├── pyproject.toml    # 项目依赖配置
└── README.md         # 项目说明
```

## 依赖说明

- `rapidocr-onnxruntime` - OCR 引擎
- `gradio` - Web UI 框架
- `opencv-python-headless` - 图像处理
- `pillow` - 图像绘制和字体渲染

## 使用说明

1. 上传待识别的图片
2. 点击"开始识别"按钮
3. 查看识别结果：
   - 左侧：原始图片输入
   - 右侧：带检测框的可视化结果
   - 下方：识别文本、详细信息和耗时统计

## License

MIT
