from PIL import Image, ImageDraw, ImageFont
import os

# === CONFIGURATION ===
width, height = 1080, 1350
font_path = r"C:\Users\Admin\AppData\Local\Microsoft\Windows\Fonts\TiroDevanagariHindi-Italic.ttf"
output_dir = "./instagram_carousel/"
os.makedirs(output_dir, exist_ok=True)

# Create folder for output
bg_image_path = "paper_bg.png"  # Optional: download from subtlepatterns.com

# Check font
if not os.path.exists(font_path):
    print(f"❌ Font not found: {font_path}")
    exit()

try:
    title_font = ImageFont.truetype(font_path, 80)
    para_font = ImageFont.truetype(font_path, 58)
    footer_font = ImageFont.truetype(font_path, 46)
except Exception as e:
    print(f"❌ Font load error: {e}")
    exit()


# === Function: Wrap text ===
def draw_wrapped_text(draw, text, font, max_width, start_y, fill=(0, 0, 0), line_spacing=30):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}".strip()
        w = draw.textbbox((0, 0), test_line, font=font)[2] - draw.textbbox((0, 0), test_line, font=font)[0]
        if w <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    y = start_y
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_w = bbox[2] - bbox[0]
        x = (width - line_w) // 2
        draw.text((x, y), line, font=font, fill=fill)
        y += bbox[3] - bbox[1] + line_spacing
    return y


# === Motivational Paragraph (Split into 3 parts) ===
full_text = (
    "जीवन में हर कोई आपके साथ नहीं होगा, "
    "लेकिन अगर आप खुद पर विश्वास रखेंगे, "
    "तो कोई भी आपको रोक नहीं सकता। "
    "मुश्किलें तो आएंगी, लेकिन हर मुश्किल के बाद "
    "एक सबक और ताकत मिलती है। "
    "बस चलते रहो, धीरे-धीरे सही दिशा में, "
    "और एक दिन आप खुद को उस मंज़िल पर पाएंगे "
    "जहाँ पहुँचने का सपना आपने कभी सोचा भी नहीं था।"
)

parts = [
    "जीवन में हर कोई आपके साथ नहीं होगा, लेकिन अगर आप खुद पर विश्वास रखेंगे, तो कोई भी आपको रोक नहीं सकता।",
    "मुश्किलें तो आएंगी, लेकिन हर मुश्किल के बाद एक सबक और ताकत मिलती है।",
    "बस चलते रहो, धीरे-धीरे सही दिशा में, और एक दिन आप खुद को उस मंज़िल पर पाएंगे जहाँ पहुँचने का सपना आपने कभी सोचा भी नहीं था।"
]

titles = [
    "भाग 1: विश्वास",
    "भाग 2: मुश्किलें",
    "भाग 3: मंज़िल"
]

colors = [
    (75, 0, 130),   # Purple
    (0, 70, 100),   # Deep Blue
    (100, 0, 70)    # Maroon
]

# === Generate Each Post ===
for i, (text, title, color) in enumerate(zip(parts, titles, colors), 1):
    # Create background
    if os.path.exists(bg_image_path):
        bg = Image.open(bg_image_path).convert("RGB")
        bg = bg.resize((width, height))
    else:
        # Fallback gradient-like soft color
        bg = Image.new("RGB", (width, height), (252, 248, 255))
    draw = ImageDraw.Draw(bg)

    # Title
    bbox_title = draw.textbbox((0, 0), title, font=title_font)
    title_x = (width - (bbox_title[2] - bbox_title[0])) // 2
    title_y = 180
    draw.text((title_x, title_y), title, font=title_font, fill=color)

    # Paragraph
    final_y = draw_wrapped_text(
        draw=draw,
        text=text,
        font=para_font,
        max_width=960,
        start_y=title_y + 130,
        fill=(40, 40, 40),
        line_spacing=35
    )

    # Footer
    handle = "@PreranaSrot"
    hashtag = "#प्रेरणास्रोत"
    footer_text = f"{handle} • {hashtag}"
    bbox_footer = draw.textbbox((0, 0), footer_text, font=footer_font)
    footer_x = (width - (bbox_footer[2] - bbox_footer[0])) // 2
    footer_y = height - 100
    draw.text((footer_x, footer_y), footer_text, font=footer_font, fill=(80, 80, 80))

    # Decorative line
    draw.line([(300, footer_y - 40), (width - 300, footer_y - 40)], fill=(200, 190, 220), width=2)

    # Save
    filename = f"{output_dir}motivation_post_{i}.png"
    bg.save(filename, "PNG")
    print(f"✅ Part {i} saved: {filename}")

print(f"\n🎉 All 3 posts generated in folder: '{output_dir}'")
print("💡 Upload as a carousel on Instagram for full impact!")