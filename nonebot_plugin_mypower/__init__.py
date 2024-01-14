import os
import random
from io import BytesIO
from PIL import Image
from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageSegment

# 命令触发
my_superpower = on_command('我的超能力', priority=10, block=True)

@my_superpower.handle()
async def _():
    folders = ['超能力', '但是', '主义', '万圣节']
    selected_images = []

    # 从四个文件夹中依次选择图片
    for folder in folders:
        folder_path = os.path.join(os.path.dirname(__file__), folder)
        images = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        if images:
            selected_image_path = random.choice(images)
            selected_images.append(selected_image_path)
        else:
            await my_superpower.send(f"No images found in {folder}.")
            return

    # 读取第一张图片以确定宽度
    first_image = Image.open(selected_images[0])
    total_width = first_image.width

    # 计算总高度并调整图片大小
    total_height = 0
    images_to_join = []
    for img_path in selected_images:
        img = Image.open(img_path)
        if img.width != total_width:
            new_height = int(total_width * img.height / img.width)
            img = img.resize((total_width, new_height), Image.Resampling.LANCZOS)
        total_height += img.height
        images_to_join.append(img)

    # 创建新图像
    new_image = Image.new('RGB', (total_width, total_height), (255, 255, 255))
    current_height = 0
    for img in images_to_join:
        new_image.paste(img, (0, current_height))
        current_height += img.height

    # 将图片转换为字节流
    img_byte_arr = BytesIO()
    new_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    # 发送图片
    try:
        await my_superpower.send(MessageSegment.image(img_byte_arr))
    except Exception as e:
        await my_superpower.send(f"图片发送失败: {e}")
