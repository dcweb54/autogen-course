from PIL import Image, ImageDraw, ImageFont
import os

# === CONFIGURATION ===
width_post, height_post = 1080, 1350      # Feed post
width_story, height_story = 1080, 1920    # Story

font_path = r"C:\Users\Admin\AppData\Local\Microsoft\Windows\Fonts\TiroDevanagariHindi-Italic.ttf"
logo_image_path = "logo.png"  # Optional: your logo (64x64 transparent PNG)
bg_image_path = "paper_bg.png"  # Optional background

# Create output folders
os.makedirs("carousel_posts", exist_ok=True)
os.makedirs("instagram_stories", exist_ok=True)
os.makedirs("weekly_series/feed", exist_ok=True)
os.makedirs("weekly_series/story", exist_ok=True)

# Load font
if not os.path.exists(font_path):
    print(f"❌ Font not found: {font_path}")
    exit()

try:
    title_font = ImageFont.truetype(font_path, 80)
    para_font = ImageFont.truetype(font_path, 58)
    footer_font = ImageFont.truetype(font_path, 46)
    small_font = ImageFont.truetype(font_path, 40)
    swipe_font = ImageFont.truetype(font_path, 60)  # For swipe hint
except Exception as e:
    print(f"❌ Font error: {e}")
    exit()


# === Text Wrap Function ===
def draw_wrapped_text(draw, text, font, max_width, start_y, fill=(0,0,0), line_spacing=30):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}".strip()
        w = draw.textbbox((0,0), test_line, font=font)[2] - draw.textbbox((0,0), test_line, font=font)[0]
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
        bbox = draw.textbbox((0,0), line, font=font)
        x = (width_post - (bbox[2]-bbox[0])) // 2 if max_width == 960 else (width_story - (bbox[2]-bbox[0])) // 2
        draw.text((x, y), line, font=font, fill=fill)
        y += bbox[3] - bbox[1] + line_spacing
    return y


# === Add Background ===
def get_background(w, h, use_image=True):
    if use_image and os.path.exists(bg_image_path):
        bg = Image.open(bg_image_path).convert("RGB")
        return bg.resize((w, h))
    else:
        return Image.new("RGB", (w, h), (253, 247, 255))


# === Part 1: 3-Part Carousel with Swipe Hint & Logo ===
parts = [
    "जीवन में हर कोई आपके साथ नहीं होगा, लेकिन अगर आप खुद पर विश्वास रखेंगे, तो कोई भी आपको रोक नहीं सकता।",
    "मुश्किलें तो आएंगी, लेकिन हर मुश्किल के बाद एक सबक और ताकत मिलती है।",
    "बस चलते रहो, धीरे-धीरे सही दिशा में, और एक दिन आप खुद को उस मंज़िल पर पाएंगे जहाँ पहुँचने का सपना आपने कभी सोचा भी नहीं था।"
]

titles = ["भाग 1: विश्वास", "भाग 2: मुश्किलें", "भाग 3: मंज़िल"]
colors = [(75, 0, 130), (0, 70, 100), (100, 0, 70)]

for i, (text, title, color) in enumerate(zip(parts, titles, colors), 1):
    # --- Feed Post (1080x1350) ---
    img_post = get_background(width_post, height_post)
    draw_post = ImageDraw.Draw(img_post)

    # Title
    bbox_t = draw_post.textbbox((0,0), title, font=title_font)
    tx = (width_post - (bbox_t[2]-bbox_t[0])) // 2
    ty = 180
    draw_post.text((tx, ty), title, font=title_font, fill=color)

    # Text
    py = draw_wrapped_text(draw_post, text, para_font, 960, ty + 130, (40,40,40), 35)

    # Swipe hint (only on part 1 & 2)
    if i < 3:
        swipe_text = "स्वाइप करें →"
        sw_bbox = draw_post.textbbox((0,0), swipe_text, font=swipe_font)
        sw_x = (width_post - (sw_bbox[2]-sw_bbox[0])) // 2
        sw_y = py + 30
        draw_post.text((sw_x, sw_y), swipe_text, font=swipe_font, fill=(150, 150, 150))

    # Footer
    footer = f"@PreranaSrot • #प्रेरणास्रोत"
    fbbox = draw_post.textbbox((0,0), footer, font=footer_font)
    fx = (width_post - (fbbox[2]-fbbox[0])) // 2
    fy = height_post - 100
    draw_post.text((fx, fy), footer, font=footer_font, fill=(80,80,80))

    # Logo (text or image)
    logo_text = "🌸 प्रेरणास्रोत"
    lx = 50
    ly = height_post - 90
    draw_post.text((lx, ly), logo_text, font=small_font, fill=(100, 50, 120))

    img_post.save(f"carousel_posts/motivation_post_{i}.png", "PNG")

    # --- Story Version (1080x1920) ---
    img_story = get_background(width_story, height_story)
    draw_story = ImageDraw.Draw(img_story)

    # Title (higher)
    bbox_t_s = draw_story.textbbox((0,0), title, font=title_font)
    tx_s = (width_story - (bbox_t_s[2]-bbox_t_s[0])) // 2
    ty_s = 300
    draw_story.text((tx_s, ty_s), title, font=title_font, fill=color)

    # Text
    py_s = draw_wrapped_text(draw_story, text, para_font, 960, ty_s + 140, (40,40,40), 40)

    # Swipe hint
    if i < 3:
        draw_story.text((width_story//2 - 100, py_s + 50), "स्वाइप करें →", font=swipe_font, fill=(160,160,160))

    # Footer
    draw_story.text((50, height_story - 120), "@PreranaSrot", font=footer_font, fill=(90,90,90))
    draw_story.text((50, height_story - 70), "#प्रेरणास्रोत", font=small_font, fill=(100,100,100))

    # Logo
    draw_story.text((50, 50), "🌸", font=swipe_font, fill=(255, 100, 150))

    img_story.save(f"instagram_stories/story_part_{i}.png", "PNG")
    print(f"✅ Generated Post & Story Part {i}")


# === Part 2: Weekly Series (Day 1 to Day 7) ===
weekly_quotes = [
    "खुद पर विश्वास रखो, तुम सब कुछ हासिल कर सकते हो।",
    "हर सुबह एक नई शुरुआत का मौका है।",
    "मेहनत कभी अकार्थ नहीं जाती।",
    "डर के आगे जीत है।",
    "सकारात्मक रहो, जीवन खुद तुम्हारे अनुकूल हो जाएगा।",
    "छोटे कदम भी मंज़िल तक ले जाते हैं।",
    "आज का प्रयास, कल की सफलता की नींव है।"
]

for day in range(1, 8):
    quote = weekly_quotes[day-1]
    day_title = f"दिन {day}: प्रेरणा"

    # --- Feed ---
    img = get_background(width_post, height_post)
    draw = ImageDraw.Draw(img)

    # Title
    bbox = draw.textbbox((0,0), day_title, font=title_font)
    x = (width_post - (bbox[2]-bbox[0])) // 2
    draw.text((x, 200), day_title, font=title_font, fill=(80, 0, 100))

    # Quote
    draw_wrapped_text(draw, quote, para_font, 960, 350, (40,40,40), 35)

    # Footer
    draw.text((50, height_post - 100), "@PreranaSrot", font=footer_font, fill=(80,80,80))
    draw.text((50, height_post - 60), f"Day {day}/7 • #प्रेरणास्रोत", font=small_font, fill=(100,100,100))

    img.save(f"weekly_series/feed/day_{day}.png", "PNG")

    # --- Story ---
    story = get_background(width_story, height_story)
    d = ImageDraw.Draw(story)

    d.text((width_story//2 - 150, 400), day_title, font=title_font, fill=(80, 0, 100))
    draw_wrapped_text(d, quote, para_font, 960, 550, (40,40,40), 45)
    d.text((50, height_story - 100), "@PreranaSrot • #प्रेरणास्रोत", font=footer_font, fill=(90,90,90))

    story.save(f"weekly_series/story/day_{day}.png", "PNG")

print("\n🎉 All content generated!")
print("📁 Check folders: 'carousel_posts/', 'instagram_stories/', 'weekly_series/'")
print("💡 Tip: Post daily for 7 days to build audience!")