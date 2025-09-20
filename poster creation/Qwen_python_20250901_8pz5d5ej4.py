from PIL import Image, ImageDraw, ImageFont
import os

# === CONFIGURATION ===
width_post, height_post = 1080, 1350   # Feed
width_story, height_story = 1080, 1920  # Story

# Hindi font (your local font)
hindi_font_path = r"C:\Users\Admin\AppData\Local\Microsoft\Windows\Fonts\TiroDevanagariHindi-Italic.ttf"

# English font (fallback: DejaVuSans or Arial)
try:
    english_font_large = ImageFont.truetype("DejaVuSans.ttf", 58)
    english_font_small = ImageFont.truetype("DejaVuSans.ttf", 46)
except IOError:
    try:
        english_font_large = ImageFont.truetype("arial.ttf", 58)
        english_font_small = ImageFont.truetype("arial.ttf", 46)
    except IOError:
        # Pillow fallback (basic)
        english_font_large = ImageFont.load_default()
        english_font_small = ImageFont.load_default()

# Background
bg_image_path = "paper_bg.png"  # Optional
os.makedirs("bilingual/feed", exist_ok=True)
os.makedirs("bilingual/story", exist_ok=True)

# Load Hindi font
if not os.path.exists(hindi_font_path):
    print(f"❌ Hindi font not found: {hindi_font_path}")
    exit()

try:
    hindi_font = ImageFont.truetype(hindi_font_path, 60)
    title_font = ImageFont.truetype(hindi_font_path, 80)
    footer_font = ImageFont.truetype(hindi_font_path, 46)
    small_font = ImageFont.truetype(hindi_font_path, 40)
    swipe_font = ImageFont.truetype(hindi_font_path, 60)
except Exception as e:
    print(f"❌ Font load error: {e}")
    exit()


# === Background helper ===
def get_bg(w, h):
    if os.path.exists(bg_image_path):
        try:
            bg = Image.open(bg_image_path).convert("RGB")
            return bg.resize((w, h))
        except:
            pass
    return Image.new("RGB", (w, h), (254, 250, 255))


# === Text Wrap for Hindi & English ===
def draw_wrapped_line(draw, text, font, max_width, x, y, fill, line_spacing=10):
    words = text.split()
    line = ""
    final_y = y
    for word in words:
        test = f"{line} {word}".strip()
        w = draw.textbbox((0,0), test, font=font)[2] - draw.textbbox((0,0), test, font=font)[0]
        if w <= max_width:
            line = test
        else:
            if line:
                bbox = draw.textbbox((0,0), line, font=font)
                lx = x + (max_width - (bbox[2]-bbox[0])) // 2
                draw.text((lx, final_y), line, font=font, fill=fill)
                final_y += bbox[3] - bbox[1] + line_spacing
            line = word
    if line:
        bbox = draw.textbbox((0,0), line, font=font)
        lx = x + (max_width - (bbox[2]-bbox[0])) // 2
        draw.text((lx, final_y), line, font=font, fill=fill)
        final_y += bbox[3] - bbox[1] + 40
    return final_y


# === Bilingual Quotes (Hindi + English) ===
bilingual_quotes = [
    {
        "hindi": "जीवन में हर कोई आपके साथ नहीं होगा, लेकिन अगर आप खुद पर विश्वास रखेंगे, तो कोई भी आपको रोक नहीं सकता।",
        "english": "Not everyone will support you in life, but if you believe in yourself, no one can stop you."
    },
    {
        "hindi": "मुश्किलें तो आएंगी, लेकिन हर मुश्किल के बाद एक सबक और ताकत मिलती है।",
        "english": "Challenges will come, but after every struggle, you gain strength and wisdom."
    },
    {
        "hindi": "बस चलते रहो, धीरे-धीरे सही दिशा में, और एक दिन आप खुद को उस मंज़िल पर पाएंगे जहाँ पहुँचने का सपना आपने कभी सोचा भी नहीं था।",
        "english": "Just keep walking, slowly in the right direction, and one day you’ll reach a destination you never even dreamed of."
    }
]

titles = ["भाग 1: विश्वास", "भाग 2: मुश्किलें", "भाग 3: मंज़िल"]
colors = [(75, 0, 130), (0, 70, 100), (100, 0, 70)]


# === Generate Bilingual Posts ===
for i, (quote, title, color) in enumerate(zip(bilingual_quotes, titles, colors), 1):
    # --- Feed Version ---
    img = get_bg(width_post, height_post)
    draw = ImageDraw.Draw(img)

    # Title
    try:
        bbox_t = draw.textbbox((0,0), title, font=title_font)
        tx = (width_post - (bbox_t[2]-bbox_t[0])) // 2
        ty = 160
        draw.text((tx, ty), title, font=title_font, fill=color)
    except:
        draw.text((400, 160), title, font=title_font, fill=color)

    # Hindi Text
    hy = ty + 130
    hy = draw_wrapped_line(draw, quote["hindi"], hindi_font, 960, 60, hy, (40, 20, 100), 25)

    # English Text (with proper font)
    try:
        ey = draw_wrapped_line(draw, quote["english"], english_font_large, 960, 60, hy, (60, 60, 60), 25)
    except:
        # Fallback: smaller font
        try:
            temp_font = ImageFont.truetype("arial.ttf", 50) if os.path.exists("arial.ttf") else ImageFont.load_default()
            draw_wrapped_line(draw, quote["english"], temp_font, 960, 60, hy, (60, 60, 60), 25)
        except:
            draw.text((100, hy), "English text not available", font=small_font, fill=(100,100,100))

    # Swipe hint
    if i < 3:
        try:
            draw.text((width_post//2 - 120, height_post - 180), "स्वाइप करें →", font=swipe_font, fill=(160,160,160))
        except:
            draw.text((width_post//2 - 100, height_post - 180), "Swipe →", font=english_font_small, fill=(160,160,160))

    # Footer
    handle = "@PreranaSrot"
    hashtag = "#प्रेरणास्रोत #Motivation"
    draw.text((60, height_post - 100), handle, font=footer_font, fill=(90, 90, 90))
    draw.text((60, height_post - 60), hashtag, font=small_font, fill=(100, 100, 100))

    img.save(f"bilingual/feed/part_{i}.png", "PNG")

    # --- Story Version (1080x1920) ---
    story = get_bg(width_story, height_story)
    d = ImageDraw.Draw(story)

    # Title
    try:
        st_bbox = d.textbbox((0,0), title, font=title_font)
        st_x = (width_story - (st_bbox[2]-st_bbox[0])) // 2
        st_y = 300
        d.text((st_x, st_y), title, font=title_font, fill=color)
    except:
        d.text((400, 300), title, font=title_font, fill=color)

    # Hindi
    h_sy = st_y + 140
    h_sy = draw_wrapped_line(d, quote["hindi"], hindi_font, 960, 60, h_sy, (40, 20, 100), 30)

    # English
    try:
        draw_wrapped_line(d, quote["english"], english_font_large, 960, 60, h_sy, (70, 70, 70), 30)
    except:
        try:
            temp_font = ImageFont.truetype("arial.ttf", 52)
            draw_wrapped_line(d, quote["english"], temp_font, 960, 60, h_sy, (70, 70, 70), 30)
        except:
            d.text((100, h_sy), "Translation not available", font=small_font, fill=(100,100,100))

    # Footer
    d.text((60, height_story - 120), "@PreranaSrot", font=footer_font, fill=(80,80,80))
    d.text((60, height_story - 70), "#प्रेरणास्रोत #MotivationDaily", font=small_font, fill=(90,90,90))

    # Swipe hint
    if i < 3:
        try:
            d.text((width_story//2 - 120, height_story - 200), "स्वाइप करें →", font=swipe_font, fill=(170,170,170))
        except:
            d.text((width_story//2 - 80, height_story - 200), "Swipe →", font=english_font_small, fill=(170,170,170))

    story.save(f"bilingual/story/story_{i}.png", "PNG")
    print(f"✅ Bilingual Post {i} generated (feed & story)")

print("\n🎉 All bilingual posters created!")
print("📁 Check: 'bilingual/feed/' and 'bilingual/story/'")
print("💡 Perfect for reaching Hindi + English audiences!")