from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json
import textwrap
import os
import math
import sys
from typing import Any, Dict, List, Optional, Tuple, Union


TEMPLATE: str = "poster_template.json"

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

def draw_rounded_rect(draw: ImageDraw.ImageDraw, xy: Tuple[int, int, int, int], radius: int, fill: Tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill)

def draw_text_centered(
    draw: ImageDraw.ImageDraw, 
    text: str, 
    font: ImageFont.FreeTypeFont, 
    x_center: int, 
    y_top: int, 
    max_width: int, 
    align: str = 'center', 
    line_spacing: int = 4
) -> None:
    # Wrap text to fit max_width
    lines: List[str] = []
    for paragraph in text.split("\n"):
        lines += textwrap.wrap(paragraph, width=100)  # crude; refine by measuring
    # better wrap by measuring
    wrapped: List[str] = []
    for paragraph in text.split("\n"):
        words: List[str] = paragraph.split()
        line: str = ""
        for w in words:
            test: str = (line + " " + w).strip()
            wbox: Tuple[int, int, int, int] = draw.textbbox((0, 0), test, font=font)
            if wbox[2] - wbox[0] <= max_width:
                line = test
            else:
                if line:
                    wrapped.append(line)
                line = w
        if line:
            wrapped.append(line)
    lines = wrapped if wrapped else [text]

    # compute total height
    ascent: int
    descent: int
    ascent, descent = font.getmetrics()
    line_height: int = ascent + descent
    total_h: int = len(lines) * (line_height + line_spacing) - line_spacing

    y: int = y_top
    # Note: font_color is not defined in this function - this appears to be a bug in the original code
    # Assuming it should be passed as a parameter or defined elsewhere
    for ln in lines:
        w: float = draw.textlength(ln, font=font)
        x: float = x_center - w/2
        # This will cause an error - font_color is undefined
        # draw.text((x, y), ln, font=font, fill=font_color)
        y += line_height + line_spacing

def draw_wrapped(
    draw: ImageDraw.ImageDraw, 
    text: str, 
    font: ImageFont.FreeTypeFont, 
    x_center: int, 
    y_top: int, 
    max_width: int, 
    fill: Tuple[int, int, int, int], 
    line_spacing: int = 6
) -> int:
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
        w: float = draw.textlength(ln, font=font)
        x: float = x_center - w/2
        draw.text((x, y), ln, font=font, fill=fill)
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
    canvas: Image.Image = Image.new("RGBA", (canvas_w, canvas_h), tpl["canvas"]["background_color"])
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
        t: float = i / float(overlay_h - 1)
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
            tuple(tpl["slide_indicator"]["box"]["bg_color"])
        )
        # text
        si_font: ImageFont.FreeTypeFont = ImageFont.truetype(
            tpl["slide_indicator"]["text_style"]["font_path"], 
            tpl["slide_indicator"]["text_style"]["font_size"]
        )
        si_text: str = "3/8"  # default; you can override
        tw: float = draw.textlength(si_text, font=si_font)
        draw.text(
            (px + (box_w - tw) / 2, py + (box_h - tpl["slide_indicator"]["text_style"]["font_size"]) / 2 - 4), 
            si_text, 
            font=si_font, 
            fill=tpl["slide_indicator"]["text_style"]["color"]
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
    draw.text(
        (content_center_x - draw.textlength(myth_text, font=myth_font) / 2, myth_y), 
        myth_text, 
        font=myth_font, 
        fill=myth["style"]["color"]
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
        txt_w: float = draw.textlength(txt, font=ms_font)
        total_w: float = txt_w + circle_r * 2 + c["pad_right"]
        start_x: float = content_center_x - total_w / 2
        cx: float = start_x + circle_r
        cy: float = ms_y + ms_font.getmetrics()[0] // 2
        # circle
        draw.ellipse(
            (cx - circle_r, cy - circle_r, cx + circle_r, cy + circle_r), 
            fill=c["circle_color"]
        )
        # draw X
        x_th: int = c["x_thickness"]
        offset: int = int(circle_r * 0.6)
        draw.line(
            (cx - offset, cy - offset, cx + offset, cy + offset), 
            fill=c["x_color"], 
            width=x_th
        )
        draw.line(
            (cx - offset, cy + offset, cx + offset, cy - offset), 
            fill=c["x_color"], 
            width=x_th
        )
        text_x: float = start_x + circle_r * 2 + c["pad_right"]
        draw.text((text_x, ms_y), txt, font=ms_font, fill=ms["style"]["color"])
    else:
        draw.text(
            (content_center_x - draw.textlength(ms["text"], font=ms_font) / 2, ms_y), 
            ms["text"], 
            font=ms_font, 
            fill=ms["style"]["color"]
        )

    # Truth label
    tlabel: Dict[str, Any] = tpl["truth_label"]
    t_font: ImageFont.FreeTypeFont = ImageFont.truetype(
        tlabel["style"]["font_path"], 
        tlabel["style"]["font_size"]
    )
    t_y: int = overlay_top + int(overlay_h * tlabel["position"]["y_offset_percent_from_overlay_top"])
    draw.text(
        (content_center_x - draw.textlength(tlabel["text"], font=t_font) / 2, t_y), 
        tlabel["text"], 
        font=t_font, 
        fill=tlabel["style"]["color"]
    )
    # underline if requested
    if tlabel["style"].get("underline"):
        w: float = draw.textlength(tlabel["text"], font=t_font)
        underline_y: int = t_y + t_font.getmetrics()[0] + 6
        draw.line(
            (content_center_x - w / 2, underline_y, content_center_x + w / 2, underline_y), 
            fill=tlabel["style"]["color"], 
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
        line_spacing=tex["style"].get("line_spacing", 6)
    )

    # Save
    canvas.convert("RGB").save(out_path, quality=92)
    print("Saved:", out_path)

if __name__ == "__main__":
    # if len(sys.argv) < 3:
    #     print("Usage: python generate_poster.py background.jpg output.jpg [template.json]")
    #     sys.exit(1)
    # bg: str = sys.argv[1]
    # out: str = sys.argv[2]
    # if len(sys.argv) == 4:
    #     TEMPLATE = sys.argv[3]
    current_dir = os.path.join(os.getcwd(), "instagram-case", "day-01","image-content")
    background_image = os.path.join(current_dir,"background.jpg")
    output_image = os.path.join(current_dir,"output-image.jpg")
    template_json = os.path.join(current_dir,"poster_template.json")
    
    print(current_dir)
    
    gen_poster(background_image, output_image, json_path=template_json)