from PIL import Image, ImageDraw,ImageFont
from .config import load_template, normalize_color
from .layout import fit_cover, calculate_overlay_position, get_content_center
from .components import (
    draw_slide_indicator, draw_myth_label, draw_myth_statement_with_icon,
    draw_truth_label_with_underline
)
from .draw_utils import draw_wrapped_text

def create_gradient_overlay(canvas_w: int, overlay_h: int, gradient_config: dict) -> Image.Image:
    """Create gradient overlay for bottom section"""
    grad = Image.new("RGBA", (canvas_w, overlay_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(grad)
    
    r1, g1, b1, a1 = gradient_config["from_rgba"]
    r2, g2, b2, a2 = gradient_config["to_rgba"]
    
    for i in range(overlay_h):
        t = i / float(overlay_h - 1) if overlay_h > 1 else 0.0
        a = int(a1 * (1 - t) + a2 * t)
        draw.line([(0, i), (canvas_w, i)], fill=(r1, g1, b1, a))
    return grad

def gen_poster(bg_path: str, out_path: str, json_path: str = "poster_template.json") -> None:
    # Load configuration
    template = load_template(json_path)
    canvas_w = template["canvas"]["width"]
    canvas_h = template["canvas"]["height"]
    
    # Create base canvas
    canvas = Image.new("RGBA", (canvas_w, canvas_h), 
                      normalize_color(template["canvas"]["background_color"]))
    draw = ImageDraw.Draw(canvas)
    
    # Add background image
    img_area_h = int(canvas_h * template["image_area"]["height_percent"])
    bg = Image.open(bg_path).convert("RGBA")
    bg_fitted = fit_cover(bg, canvas_w, img_area_h)
    canvas.paste(bg_fitted, (0, 0))
    
    # Add gradient overlay
    overlay_top, overlay_h = calculate_overlay_position(canvas_h, template["image_area"]["height_percent"])
    gradient = create_gradient_overlay(canvas_w, overlay_h, template["bottom_overlay"]["gradient"])
    canvas.paste(gradient, (0, overlay_top), gradient)
    
    # Draw components
    content_center_x = get_content_center(canvas_w)
    
    draw_slide_indicator(draw, canvas_w, canvas_h, template["slide_indicator"])
    draw_myth_label(draw, overlay_top, overlay_h, content_center_x, template["myth_label"])
    draw_myth_statement_with_icon(draw, overlay_top, overlay_h, content_center_x, canvas_w, template["myth_statement"])
    draw_truth_label_with_underline(draw, overlay_top, overlay_h, content_center_x, template["truth_label"])
    
    # Draw truth explanation (wrapped text)
    explanation_config = template["truth_explanation"]
    explanation_font = ImageFont.truetype(
        explanation_config["style"]["font_path"], 
        explanation_config["style"]["font_size"]
    )
    explanation_y = overlay_top + int(overlay_h * explanation_config["position"]["y_offset_percent_from_overlay_top"])
    draw_wrapped_text(
        draw, explanation_config["text"], explanation_font,
        content_center_x, explanation_y,
        int(canvas_w * explanation_config["style"]["max_width_percent"]),
        normalize_color(explanation_config["style"]["color"]),
        explanation_config["style"].get("line_spacing", 8)
    )
    
    # Save result
    canvas.convert("RGB").save(out_path, quality=92)
    print(f"Saved: {out_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python main.py background.jpg output.jpg [template.json]")
        sys.exit(1)
    
    bg_path, out_path = sys.argv[1], sys.argv[2]
    template_path = sys.argv[3] if len(sys.argv) == 4 else "poster_template.json"
    gen_poster(bg_path, out_path, template_path)