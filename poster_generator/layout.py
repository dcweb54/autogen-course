from PIL import Image
from typing import Tuple

def fit_cover(bg: Image.Image, target_w: int, target_h: int) -> Image.Image:
    """Resize and crop image to fill target dimensions"""
    bw, bh = bg.size
    scale = max(target_w / bw, target_h / bh)
    new_w, new_h = int(bw * scale), int(bh * scale)
    bg = bg.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    return bg.crop((left, top, left + target_w, top + target_h))

def calculate_overlay_position(canvas_h: int, img_area_percent: float) -> Tuple[int, int]:
    """Calculate where overlay starts and its height"""
    img_area_h = int(canvas_h * img_area_percent)
    overlay_h = canvas_h - img_area_h
    return img_area_h, overlay_h

def get_content_center(canvas_w: int) -> int:
    """Get horizontal center for content"""
    return canvas_w // 2