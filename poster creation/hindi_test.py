from PIL import Image, ImageDraw, ImageFont

# Create image (Instagram post size: 1080x1350)
width, height = 1080, 1350
background_color = (220, 240, 255)  # Light blue background
image = Image.new("RGB", (width, height), background_color)
draw = ImageDraw.Draw(image)

font_path = r"c:\USERS\ADMIN\APPDATA\LOCAL\MICROSOFT\WINDOWS\FONTS\TIRODEVANAGARIHINDI-ITALIC.TTF"


# Load Hindi font (adjust size as needed)
try:
    font_large = ImageFont.truetype(font_path, 100)
    font_small = ImageFont.truetype(font_path, 60)
except IOError:
    print("Font not found! Please ensure 'NotoSansDevanagari.ttf' is in the directory.")
    exit()

# Hindi Text (example: "ज्ञान ही शक्ति है" = "Knowledge is Power")
title_text = "ज्ञान ही शक्ति है"
subtitle_text = "— फ्रांसिस बेकन"

# Center the main text
bbox_title = draw.textbbox((0, 0), title_text, font=font_large)
title_width = bbox_title[2] - bbox_title[0]
title_x = (width - title_width) // 2
title_y = height // 2 - 100

bbox_subtitle = draw.textbbox((0, 0), subtitle_text, font=font_small)
subtitle_width = bbox_subtitle[2] - bbox_subtitle[0]
subtitle_x = (width - subtitle_width) // 2
subtitle_y = height // 2 + 60

# Add text to image
draw.text((title_x, title_y), title_text, font=font_large, fill=(25, 25, 112))  # Dark blue
draw.text((subtitle_x, subtitle_y), subtitle_text, font=font_small, fill=(70, 70, 70))

# Optional: Add border or decorative line
line_y = subtitle_y + 80
draw.line([(200, line_y), (width - 200, line_y)], fill=(200, 220, 255), width=4)

# Add footer
footer_text = "प्रेरणा के शब्द | Follow for more 🌸"
font_footer = ImageFont.truetype(font_path, 45)
footer_bbox = draw.textbbox((0, 0), footer_text, font=font_footer)
footer_x = (width - footer_bbox[2] + footer_bbox[0]) // 2
footer_y = height - 120
draw.text((footer_x, footer_y), footer_text, font=font_footer, fill=(100, 100, 100))

# Save image
image.save("hindi_instagram_poster.png")
print("Poster saved as 'hindi_instagram_poster.png'")
image.show()  # Opens the image