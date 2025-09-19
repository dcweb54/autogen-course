from moviepy import ImageClip
from PIL import Image
import numpy as np

import os

current_image = os.path.join(os.path.join(os.getcwd(), "images"), "1.jpg")
current_output = os.path.join(
    os.path.join(os.getcwd(), "moviepy-learning-material-output", "sample02.mp4")
)

# Create an image clip from file
image_clip = ImageClip(current_image)

# Set duration for the image (for video creation)
image_clip = image_clip.with_duration(5)  # 5 seconds

# Resize image
resized = image_clip.resized(width=640)  # or .resize((width, height))


resized.write_videofile(
    current_output,
    fps=25,
    codec="libx264",
    preset="ultrafast",
    threads=8,
    ffmpeg_params=["-crf", "25"],
)

# Crop image
# cropped = image_clip.Crop(x1=100, y1=100, x2=400, y2=400)
