"""
Helper script to generate realistic synthetic receipt images for testing.
Creates:
1. data/sample_receipt.png (Clear dinner receipt with meal & alcohol items)
2. data/sample_blurry_receipt.png (Severely blurred receipt to test blurriness detection)
"""

import os
from PIL import Image, ImageDraw, ImageFilter


def create_receipt_images(output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    clear_path = os.path.join(output_dir, "sample_receipt.png")
    blurry_path = os.path.join(output_dir, "sample_blurry_receipt.png")

    # Dimensions
    width, height = 480, 680
    bg_color = (255, 255, 255)
    text_color = (20, 20, 20)
    line_color = (180, 180, 180)

    # 1. Create Base Clear Receipt
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Header
    draw.text((140, 30), "TRATTORIA ROMANA", fill=text_color)
    draw.text((155, 55), "123 Main Street, Suite 4", fill=(100, 100, 100))
    draw.text((170, 75), "Tel: (555) 019-2834", fill=(100, 100, 100))

    draw.line([(30, 105), (450, 105)], fill=line_color, width=1)

    # Metadata
    draw.text((35, 120), "Date: 2026-11-20", fill=text_color)
    draw.text((320, 120), "Time: 19:42", fill=text_color)
    draw.text((35, 145), "Server: Marco B.", fill=text_color)
    draw.text((320, 145), "Table: 14", fill=text_color)

    draw.line([(30, 175), (450, 175)], fill=line_color, width=2)

    # Items Header
    draw.text((35, 190), "ITEM", fill=text_color)
    draw.text((390, 190), "PRICE", fill=text_color)
    draw.line([(30, 215), (450, 215)], fill=line_color, width=1)

    # Items
    items = [
        ("1  Grilled Salmon Entree", "$32.00"),
        ("1  Side Caesar Salad", "$8.00"),
        ("1  Chianti Classico Red Wine", "$14.00"),
        ("1  Sparkling Mineral Water", "$4.00"),
        ("1  Traditional Tiramisu", "$9.00"),
    ]

    y = 230
    for item, price in items:
        draw.text((35, y), item, fill=text_color)
        draw.text((390, y), price, fill=text_color)
        y += 35

    draw.line([(30, y + 10), (450, y + 10)], fill=line_color, width=1)
    y += 25

    # Totals
    draw.text((250, y), "Subtotal:", fill=text_color)
    draw.text((390, y), "$67.00", fill=text_color)
    y += 30

    draw.text((250, y), "Tax (8.5%):", fill=text_color)
    draw.text((390, y), "$5.70", fill=text_color)
    y += 30

    draw.text((250, y), "Tip / Gratuity:", fill=text_color)
    draw.text((390, y), "$12.00", fill=text_color)
    y += 35

    draw.line([(240, y), (450, y)], fill=text_color, width=2)
    y += 10

    draw.text((250, y), "TOTAL:", fill=(0, 0, 0))
    draw.text((385, y), "$84.70", fill=(0, 0, 0))

    # Footer
    y += 60
    draw.line([(30, y), (450, y)], fill=line_color, width=1)
    draw.text((130, y + 20), "THANK YOU FOR DINING WITH US!", fill=(90, 90, 90))

    # Save Clear Image
    img.save(clear_path, "PNG")
    print(f"[✓] Generated clear receipt: {clear_path}")

    # 2. Create Severely Blurry Receipt
    blurry_img = img.filter(ImageFilter.GaussianBlur(radius=7))
    blurry_img.save(blurry_path, "PNG")
    print(f"[✓] Generated blurry receipt: {blurry_path}")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_dir = os.path.join(base_dir, "data")
    create_receipt_images(target_dir)
