from PIL import ImageDraw, ImageFont
from typing import Tuple, Union, List

def draw_rounded_rect(draw: ImageDraw.ImageDraw, xy: Tuple[int, int, int, int], 
                     radius: int, fill: Tuple[int, ...]) -> None:
    draw.rounded_rectangle(xy, radius=radius, fill=fill)

def draw_text_centered(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont,
                      x_center: int, y: int, fill: Tuple[int, ...]) -> float:
    """Draw single line text centered horizontally"""
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    x = x_center - width / 2
    draw.text((x, y), text, font=font, fill=fill)
    return width

def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, 
              max_width: int, line_spacing: int = 6) -> List[str]:
    """Wrap text to fit max_width"""
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        test_line = (current_line + " " + word).strip()
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

def draw_wrapped_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont,
                     x_center: int, y_top: int, max_width: int, 
                     fill: Tuple[int, ...], line_spacing: int = 6) -> int:
    """Draw wrapped text and return final y position"""
    lines = wrap_text(draw, text, font, max_width, line_spacing)
    ascent, descent = font.getmetrics()
    line_height = ascent + descent
    
    y = y_top
    for line in lines:
        draw_text_centered(draw, line, font, x_center, y, fill)
        y += line_height + line_spacing
    return y