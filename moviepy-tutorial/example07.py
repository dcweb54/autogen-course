from PIL import ImageFont, ImageDraw, Image

# Create a blank image
img = Image.new('RGB', (400, 200), color = (255, 255, 255))
d = ImageDraw.Draw(img)

# Load a font (replace 'arial.ttf' with the actual path to your font file)
try:
    font = ImageFont.truetype("arial.ttf", 40)
except IOError:
    print("Font file not found. Please ensure the font is installed or provide the correct path.")
    # Fallback to default font if the specified font is not found
    font = ImageFont.load_default()

# Draw text
d.text((10,10), "Hello, Pillow!", fill=(0,0,0), font=font)

# Save the image
img.save("output.png")