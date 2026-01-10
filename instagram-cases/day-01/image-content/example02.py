from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json
import textwrap
import os
import math
import sys
from typing import Any, Dict, List, Optional, Tuple, Union

TEMPLATE: str = "poster_template.json"

def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color string to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        # Handle short hex like #FFF
        hex_color = ''.join([c*2 for c in hex_color])
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def hex_to_rgba(hex_color: str) -> Tuple[int, int, int, int]:
    """Convert hex color string to RGBA tuple with full opacity"""
    rgb = hex_to_rgb(hex_color)
    return rgb + (255,)

def normalize_color(color: Union[str, List[int], Tuple[int, ...]]) -> Tuple[int, ...]:
    """Convert color to PIL-compatible format"""
    if isinstance(color, str):
        if color.startswith('#'):
            # Hex color - convert to RGB or RGBA
            if len(color) == 9 or (len(color) == 7 and color.count('#') == 1):
                # Handle RGBA hex if needed, but typically we use RGB
                return hex_to_rgb(color)
            else:
                return hex_to_rgb(color)
        else:
            # Assume it's a named color or invalid - return black
            return (0, 0, 0)
    elif isinstance(color, (list, tuple)):
        # Ensure all values are integers
        return tuple(int(c) for c in color)
    else:
        # Fallback to black
        return (0, 0, 0)

def load_template(path: str = TEMPLATE) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def fit_cover(bg: Image.Image, target_w: int, target_h: int) -> Image.Image:
    # Resize cropping to fill target (cover)
    bw, bh = bg.size
    scale: float = max(target_w / bw, target_h / bh)
    new_w: int = int(bw * scale)
    new_h: int = int(bh * scale)
    bg = bg.resize((new_w, new_h), Image.LANCZOS)
    left: int = (new_w - target_w) // 2
    top: int = (new_h - target_h) // 2
    return bg.crop((left, top, left + target_w, top + target_h))

def draw_rounded_rect(draw: ImageDraw.ImageDraw, xy: Tuple[int, int, int, int], radius: int, fill: Tuple[int, ...]) -> None:
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill)

def draw_wrapped(
    draw: ImageDraw.ImageDraw, 
    text: str, 
    font: ImageFont.FreeTypeFont, 
    x_center: int, 
    y_top: int, 
    max_width: int, 
    fill: Union[str, List[int], Tuple[int, ...]], 
    line_spacing: int = 6
) -> int:
    # Normalize fill color
    normalized_fill = normalize_color(fill)
    
    # measure and wrap with draw.textbbox
    words: List[str] = text.split()
    lines: List[str] = []
    cur: str = ""
    for w in words:
        test: str = (cur + " " + w).strip()
        bbox: Tuple[int, int, int, int] = draw.textbbox((0, 0), test, font=font)
        wtest: int = bbox[2] - bbox[0]
        if wtest <= max_width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)

    ascent: int
    descent: int
    ascent, descent = font.getmetrics()
    lh: int = ascent + descent
    y: int = y_top
    for ln in lines:
        bbox = draw.textbbox((0, 0), ln, font=font)
        w = bbox[2] - bbox[0]
        x = x_center - w/2
        draw.text((x, y), ln, font=font, fill=normalized_fill)
        y += lh + line_spacing
    return y  # return y after drawing

def gen_poster(
    bg_path: str, 
    out_path: str, 
    json_path: str = TEMPLATE, 
    overrides: Optional[Dict[str, Any]] = None
) -> None:
    tpl: Dict[str, Any] = load_template(json_path)
    canvas_w: int = tpl["canvas"]["width"]
    canvas_h: int = tpl["canvas"]["height"]

    # Create base
    canvas: Image.Image = Image.new("RGBA", (canvas_w, canvas_h), normalize_color(tpl["canvas"]["background_color"]))
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(canvas)

    # Load and place background image (top area)
    img_area_h: int = int(canvas_h * tpl["image_area"]["height_percent"])
    bg: Image.Image = Image.open(bg_path).convert("RGBA")
    bg_fitted: Image.Image = fit_cover(bg, canvas_w, img_area_h)
    canvas.paste(bg_fitted, (0, 0))

    # Draw bottom gradient overlay (from bottom of image downward)
    overlay_h: int = int(canvas_h * tpl["bottom_overlay"]["height_percent"])
    grad: Image.Image = Image.new("RGBA", (canvas_w, overlay_h), (0, 0, 0, 0))
    gdraw: ImageDraw.ImageDraw = ImageDraw.Draw(grad)
    r1, g1, b1, a1 = tpl["bottom_overlay"]["gradient"]["from_rgba"]
    r2, g2, b2, a2 = tpl["bottom_overlay"]["gradient"]["to_rgba"]
    for i in range(overlay_h):
        t: float = i / float(overlay_h - 1) if overlay_h > 1 else 0.0
        a: int = int(a1 * (1 - t) + a2 * (t))
        gdraw.line([(0, i), (canvas_w, i)], fill=(r1, g1, b1, a))
    canvas.paste(grad, (0, img_area_h), grad)

    # Draw slide indicator
    if tpl["slide_indicator"]["enabled"]:
        box_w: int = tpl["slide_indicator"]["box"]["width"]
        box_h: int = tpl["slide_indicator"]["box"]["height"]
        margin_x: int
        margin_y: int
        margin_x, margin_y = tpl["slide_indicator"]["margin"]
        px: int = canvas_w - box_w - margin_x
        py: int = margin_y
        # rounded rect
        draw_rounded_rect(
            draw, 
            (px, py, px + box_w, py + box_h), 
            tpl["slide_indicator"]["box"]["corner_radius"], 
            normalize_color(tpl["slide_indicator"]["box"]["bg_color"])
        )
        # text
        si_font: ImageFont.FreeTypeFont = ImageFont.truetype(
            tpl["slide_indicator"]["text_style"]["font_path"], 
            tpl["slide_indicator"]["text_style"]["font_size"]
        )
        si_text: str = "3/8"  # default; you can override
        bbox = draw.textbbox((0, 0), si_text, font=si_font)
        tw = bbox[2] - bbox[0]
        draw.text(
            (px + (box_w - tw) / 2, py + (box_h - tpl["slide_indicator"]["text_style"]["font_size"]) / 2 - 4), 
            si_text, 
            font=si_font, 
            fill=normalize_color(tpl["slide_indicator"]["text_style"]["color"])
        )

    # Overlay top-of-overlay coords
    overlay_top: int = img_area_h
    left_margin: int = int(canvas_w * tpl["margins"]["left_percent"])
    right_margin: int = int(canvas_w * tpl["margins"]["right_percent"])
    content_center_x: int = canvas_w // 2
    max_text_w: int = canvas_w - left_margin - right_margin

    # Myth label
    myth: Dict[str, Any] = tpl["myth_label"]
    myth_font: ImageFont.FreeTypeFont = ImageFont.truetype(
        myth["style"]["font_path"], 
        myth["style"]["font_size"]
    )
    myth_y: int = overlay_top + int(overlay_h * myth["position"]["y_offset_percent_from_overlay_top"])
    myth_text: str = myth["text"]
    bbox = draw.textbbox((0, 0), myth_text, font=myth_font)
    myth_width = bbox[2] - bbox[0]
    draw.text(
        (content_center_x - myth_width / 2, myth_y), 
        myth_text, 
        font=myth_font, 
        fill=normalize_color(myth["style"]["color"])
    )

    # Myth statement with X icon
    ms: Dict[str, Any] = tpl["myth_statement"]
    ms_font: ImageFont.FreeTypeFont = ImageFont.truetype(
        ms["style"]["font_path"], 
        ms["style"]["font_size"]
    )
    ms_y: int = overlay_top + int(overlay_h * ms["position"]["y_offset_percent_from_overlay_top"])
    # draw icon circle + X if enabled
    if ms.get("icon", {}).get("draw_x_icon", False):
        c: Dict[str, Any] = ms["icon"]["x_icon"]
        circle_r: int = c["circle_radius"]
        # compute where to draw: left of text center
        # text width:
        txt: str = ms["text"]
        # Remove the ✖ symbol for width calculation if it's part of the text
        clean_txt = txt.replace("✖", "").strip()
        if clean_txt:
            bbox = draw.textbbox((0, 0), clean_txt, font=ms_font)
            txt_w = bbox[2] - bbox[0]
        else:
            txt_w = 0
        total_w: float = txt_w + circle_r * 2 + c["pad_right"]
        start_x: float = content_center_x - total_w / 2
        cx: float = start_x + circle_r
        cy: float = ms_y + ms_font.getmetrics()[0] // 2
        # circle
        draw.ellipse(
            (cx - circle_r, cy - circle_r, cx + circle_r, cy + circle_r), 
            fill=normalize_color(c["circle_color"])
        )
        # draw X
        x_th: int = c["x_thickness"]
        offset: int = int(circle_r * 0.6)
        draw.line(
            (cx - offset, cy - offset, cx + offset, cy + offset), 
            fill=normalize_color(c["x_color"]),
            width=x_th
        )
        draw.line(
            (cx - offset, cy + offset, cx + offset, cy - offset), 
            fill=normalize_color(c["x_color"]),
            width=x_th
        )
        text_x: float = start_x + circle_r * 2 + c["pad_right"]
        draw.text((text_x, ms_y), txt, font=ms_font, fill=normalize_color(ms["style"]["color"]))
    else:
        bbox = draw.textbbox((0, 0), ms["text"], font=ms_font)
        ms_width = bbox[2] - bbox[0]
        draw.text(
            (content_center_x - ms_width / 2, ms_y), 
            ms["text"], 
            font=ms_font, 
            fill=normalize_color(ms["style"]["color"])
        )

    # Truth label
    tlabel: Dict[str, Any] = tpl["truth_label"]
    t_font: ImageFont.FreeTypeFont = ImageFont.truetype(
        tlabel["style"]["font_path"], 
        tlabel["style"]["font_size"]
    )
    t_y: int = overlay_top + int(overlay_h * tlabel["position"]["y_offset_percent_from_overlay_top"])
    bbox = draw.textbbox((0, 0), tlabel["text"], font=t_font)
    t_width = bbox[2] - bbox[0]
    draw.text(
        (content_center_x - t_width / 2, t_y), 
        tlabel["text"], 
        font=t_font, 
        fill=normalize_color(tlabel["style"]["color"])
    )
    # underline if requested
    if tlabel["style"].get("underline"):
        padding = 4
        underline_y: int = t_y + t_font.getmetrics()[0] + 6
        draw.line(
            (content_center_x - t_width / 2 - padding, underline_y, 
             content_center_x + t_width / 2 + padding, underline_y), 
            fill=normalize_color(tlabel["style"]["color"]), 
            width=3
        )

    # Truth explanation (wrapped)
    tex: Dict[str, Any] = tpl["truth_explanation"]
    tex_font: ImageFont.FreeTypeFont = ImageFont.truetype(
        tex["style"]["font_path"], 
        tex["style"]["font_size"]
    )
    tex_y: int = overlay_top + int(overlay_h * tex["position"]["y_offset_percent_from_overlay_top"])
    draw_wrapped(
        draw, 
        tex["text"], 
        tex_font, 
        content_center_x, 
        tex_y, 
        int(canvas_w * tex["style"]["max_width_percent"]), 
        fill=tex["style"]["color"], 
        line_spacing=tex["style"].get("line_spacing", 8)  # Increased default line spacing
    )

    # Save
    canvas.convert("RGB").save(out_path, quality=92)
    print("Saved:", out_path)

if __name__ == "__main__":
    current_dir = os.path.join(os.getcwd(), "instagram-case", "day-01","image-content")
    background_image = os.path.join(current_dir,"background.jpg")
    output_image = os.path.join(current_dir,"output-image-01.jpg")
    template_json = os.path.join(current_dir,"poster_template.json")
    
    print(current_dir)
    
    gen_poster(background_image, output_image, json_path=template_json)