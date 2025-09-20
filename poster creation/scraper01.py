# render_hindi.py

from PIL import Image, ImageDraw, ImageFont

# Hindi text: "नमस्ते दुनिया" = "Namaste Duniya" (Hello World)
hindi_text = "नमस्ते दुनिया "

# Choose a font (adjust path as needed)
try:
    # Option 1: Noto Sans Devanagari (downloaded)
    font_path = r"c:\USERS\ADMIN\APPDATA\LOCAL\MICROSOFT\WINDOWS\FONTS\TIRODEVANAGARIHINDI-ITALIC.TTF"
    font = ImageFont.truetype(font_path, 40)

except IOError:
    print("Noto Sans not found, trying system font...")

    try:
        # Option 2: Nirmala UI (Windows 10/11)
        font = ImageFont.truetype("Nirmala UI", 40)
    except IOError:
        try:
            # Option 3: Mangal
            font = ImageFont.truetype("Mangal", 40)
        except IOError:
            print("No Devanagari font found!")
            font = ImageFont.load_default()

# Create image
# c:\USERS\ADMIN\APPDATA\LOCAL\MICROSOFT\WINDOWS\FONTS\TIRODEVANAGARIHINDI-REGULAR.TTF c:\USERS\ADMIN\APPDATA\LOCAL\MICROSOFT\WINDOWS\FONTS\TIRODEVANAGARIHINDI-ITALIC.TTF
img = Image.new("RGB", (500, 150), "white")
draw = ImageDraw.Draw(img)
# c:\Windows\Fonts\APARAJ.TTF c:\Windows\Fonts\APARAJB.TTF c:\Windows\Fonts\APARAJBI.TTF c:\Windows\Fonts\APARAJI.TTF
# Draw text
draw.text((30, 50), hindi_text, font=font, fill="black")

# Save and show
img.save("hindi_text.png")
img.show()  # Opens the image