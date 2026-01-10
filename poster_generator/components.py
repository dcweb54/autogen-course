from PIL import ImageDraw, ImageFont
from typing import Dict, Any, Tuple
from .config import normalize_color
from .draw_utils import draw_rounded_rect, draw_text_centered

def draw_slide_indicator(draw: ImageDraw.ImageDraw, canvas_w: int, canvas_h: int, 
                        config: Dict[str, Any]) -> None:
    """Draw slide indicator in top-right corner"""
    if not config["enabled"]:
        return
        
    box_w = config["box"]["width"]
    box_h = config["box"]["height"]
    margin_x, margin_y = config["margin"]
    px = canvas_w - box_w - margin_x
    py = margin_y
    
    # Background box
    draw_rounded_rect(
        draw, (px, py, px + box_w, py + box_h),
        config["box"]["corner_radius"],
        normalize_color(config["box"]["bg_color"])
    )
    
    # Text
    font = ImageFont.truetype(config["text_style"]["font_path"], 
                             config["text_style"]["font_size"])
    draw_text_centered(
        draw, "3/8", font, 
        px + box_w // 2, 
        py + (box_h - config["text_style"]["font_size"]) // 2 - 4,
        normalize_color(config["text_style"]["color"])
    )

def draw_myth_label(draw: ImageDraw.ImageDraw, overlay_top: int, overlay_h: int,
                   content_center_x: int, config: Dict[str, Any]) -> int:
    """Draw myth label and return its y position"""
    font = ImageFont.truetype(config["style"]["font_path"], config["style"]["font_size"])
    y = overlay_top + int(overlay_h * config["position"]["y_offset_percent_from_overlay_top"])
    draw_text_centered(draw, config["text"], font, content_center_x, y,
                      normalize_color(config["style"]["color"]))
    return y

def draw_myth_statement_with_icon(draw: ImageDraw.ImageDraw, overlay_top: int, overlay_h: int,
                                 content_center_x: int, canvas_w: int, config: Dict[str, Any]) -> int:
    """Draw myth statement with optional X icon"""
    font = ImageFont.truetype(config["style"]["font_path"], config["style"]["font_size"])
    y = overlay_top + int(overlay_h * config["position"]["y_offset_percent_from_overlay_top"])
    
    if config.get("icon", {}).get("draw_x_icon", False):
        icon_config = config["icon"]["x_icon"]
        circle_r = icon_config["circle_radius"]
        
        # Calculate text width without icon
        clean_text = config["text"].replace("✖", "").strip()
        bbox = draw.textbbox((0, 0), clean_text or " ", font=font)
        text_width = bbox[2] - bbox[0]
        
        total_width = text_width + circle_r * 2 + icon_config["pad_right"]
        start_x = content_center_x - total_width / 2
        circle_x = start_x + circle_r
        circle_y = y + font.getmetrics()[0] // 2
        
        # Draw circle
        draw.ellipse(
            (circle_x - circle_r, circle_y - circle_r, 
             circle_x + circle_r, circle_y + circle_r),
            fill=normalize_color(icon_config["circle_color"])
        )
        
        # Draw X
        offset = int(circle_r * 0.6)
        thickness = icon_config["x_thickness"]
        x_color = normalize_color(icon_config["x_color"])
        draw.line((circle_x - offset, circle_y - offset, 
                  circle_x + offset, circle_y + offset), 
                 fill=x_color, width=thickness)
        draw.line((circle_x - offset, circle_y + offset, 
                  circle_x + offset, circle_y - offset), 
                 fill=x_color, width=thickness)
        
        # Draw text
        text_x = start_x + circle_r * 2 + icon_config["pad_right"]
        draw.text((text_x, y), config["text"], font=font, 
                 fill=normalize_color(config["style"]["color"]))
    else:
        draw_text_centered(draw, config["text"], font, content_center_x, y,
                          normalize_color(config["style"]["color"]))
    return y

def draw_truth_label_with_underline(draw: ImageDraw.ImageDraw, overlay_top: int, overlay_h: int,
                                   content_center_x: int, config: Dict[str, Any]) -> int:
    """Draw truth label with optional underline"""
    font = ImageFont.truetype(config["style"]["font_path"], config["style"]["font_size"])
    y = overlay_top + int(overlay_h * config["position"]["y_offset_percent_from_overlay_top"])
    color = normalize_color(config["style"]["color"])
    
    # Draw text
    bbox = draw.textbbox((0, 0), config["text"], font=font)
    width = bbox[2] - bbox[0]
    x = content_center_x - width / 2
    draw.text((x, y), config["text"], font=font, fill=color)
    
    # Draw underline if requested
    if config["style"].get("underline"):
        underline_y = y + font.getmetrics()[0] + 6
        padding = 4
        draw.line((x - padding, underline_y, x + width + padding, underline_y),
                 fill=color, width=3)
    return y