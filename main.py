import gradio as gr
from rapidocr import RapidOCR
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import random


def draw_boxes(image, boxes, txts, scores):
    if isinstance(image, np.ndarray):
        img = image.copy()
    else:
        img = np.array(image)
    
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    elif img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    elif img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    pil_img = Image.fromarray(img)
    overlay = Image.new('RGBA', pil_img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    
    try:
        font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 20)
        small_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 16)
    except:
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", 20)
            small_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", 16)
        except:
            font = ImageFont.load_default()
            small_font = ImageFont.load_default()
    
    colors = [
        (255, 99, 71), (30, 144, 255), (50, 205, 50), (255, 165, 0),
        (147, 112, 219), (255, 20, 147), (0, 191, 255), (255, 215, 0)
    ]
    
    for idx, (box, txt, score) in enumerate(zip(boxes, txts, scores)):
        box = box.astype(np.int32)
        points = [(int(box[i][0]), int(box[i][1])) for i in range(len(box))]
        
        color = colors[idx % len(colors)]
        fill_color = (*color, 60)
        draw.polygon(points, fill=fill_color, outline=(*color, 200))
        
        min_x = int(np.min(box[:, 0]))
        min_y = int(np.min(box[:, 1]))
        
        text_label = f"{txt} ({score:.2f})"
        bbox = draw.textbbox((0, 0), text_label, font=small_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        label_y = max(min_y - text_height - 5, 0)
        draw.rectangle(
            [(min_x, label_y), (min_x + text_width + 10, label_y + text_height + 5)],
            fill=(*color, 200)
        )
        draw.text((min_x + 5, label_y), text_label, fill=(255, 255, 255, 255), font=small_font)
    
    pil_img = Image.alpha_composite(pil_img.convert('RGBA'), overlay)
    result = np.array(pil_img.convert('RGB'))
    
    return result


def ocr_image(image):
    if image is None:
        return None, "请上传图片", None, ""
    
    engine = RapidOCR()
    result = engine(image)
    
    if result is None or not result.txts:
        return image, "未检测到文字", None, ""
    
    vis_image = draw_boxes(image, result.boxes, result.txts, result.scores)
    
    full_text = "\n".join(result.txts)
    
    detailed_result = []
    for i, (text, score) in enumerate(zip(result.txts, result.scores), 1):
        detailed_result.append(f"[{i}] {text} | 置信度: {score:.4f}")
    
    detailed_output = "\n".join(detailed_result)
    
    elapse_info = f"总耗时: {result.elapse:.3f}秒"
    if result.elapse_list:
        elapse_info += f"\n检测: {result.elapse_list[0]:.3f}秒 | 分类: {result.elapse_list[1]:.3f}秒 | 识别: {result.elapse_list[2]:.3f}秒"
    
    return vis_image, full_text, detailed_output, elapse_info


def main():
    with gr.Blocks(title="OCR 测试验证") as demo:
        gr.Markdown("# OCR 文字识别测试")
        gr.Markdown("上传图片进行文字识别，查看检测框和识别结果")
        
        with gr.Row():
            with gr.Column(scale=1):
                image_input = gr.Image(type="numpy", label="上传图片")
                submit_btn = gr.Button("开始识别", variant="primary", size="lg")
                
                gr.Examples(
                    examples=[["vis_result.jpg"]] if __name__ == "__main__" else [],
                    inputs=image_input
                )
            
            with gr.Column(scale=1):
                image_output = gr.Image(type="numpy", label="识别结果可视化（带边框）")
        
        with gr.Row():
            with gr.Column():
                text_output = gr.Textbox(label="识别文本", lines=10)
            
            with gr.Column():
                detail_output = gr.Textbox(label="详细信息（含置信度）", lines=10)
        
        with gr.Row():
            elapse_output = gr.Textbox(label="识别耗时", lines=2)
        
        submit_btn.click(
            fn=ocr_image,
            inputs=[image_input],
            outputs=[image_output, text_output, detail_output, elapse_output]
        )
    
    demo.launch(server_name="0.0.0.0", server_port=7860)


if __name__ == "__main__":
    main()
