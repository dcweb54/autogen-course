import os
from moviepy import VideoClip, ImageClip
from moviepy.video.fx.Resize import Resize
from moviepy.video.fx.FadeIn import FadeIn
from moviepy.video.fx.FadeOut import FadeOut
import numpy as np

current_image = os.path.join(os.path.join(os.getcwd(), "images"), "1.jpg")

current_output = os.path.join(os.path.join(os.getcwd(), "moviepy-learning-material-output", "sample03.mp4"))

# Create output directory if it doesn't exist
os.makedirs(os.path.dirname(current_output), exist_ok=True)

# Method 1: Ken Burns with animated resize using lambda function
def ken_burns_effect(image_path, duration=5, zoom_start=1.0, zoom_end=1.3):
    """Ken Burns effect using MoviePy 2.0 with_effects syntax"""
    # Load image and set duration
    clip = ImageClip(image_path).with_duration(duration)
    
    # Apply animated resize effect
    ken_burns_clip = clip.with_effects([
        Resize(lambda t: zoom_start + (zoom_end - zoom_start) * (t / duration))
    ])
    
    # Optional: Add fade in/out
    ken_burns_clip = ken_burns_clip.with_effects([
        FadeIn(1.0),  # 1 second fade in
        FadeOut(1.0)   # 1 second fade out
    ])
    
    return ken_burns_clip

# Method 2: Ken Burns with panning effect
def ken_burns_with_pan(image_path, duration=5, zoom_factor=1.2, pan_distance=100):
    """Ken Burns with both zoom and pan effects"""
    clip = ImageClip(image_path).with_duration(duration)
    
    # Create a custom transformation for combined zoom and pan
    def combined_effect(get_frame, t):
        frame = get_frame(t)
        
        # Calculate current zoom
        progress = t / duration
        current_zoom = 1 + (zoom_factor - 1) * progress
        
        # Calculate pan position
        pan_x = int(pan_distance * progress)
        pan_y = int(pan_distance * 0.5 * progress)  # Move diagonally
        
        # Apply effects using Resize fx
        from PIL import Image
        pil_img = Image.fromarray(frame)
        
        # Resize (zoom)
        new_width = int(pil_img.width * current_zoom)
        new_height = int(pil_img.height * current_zoom)
        resized = pil_img.resize((new_width, new_height), Image.LANCZOS)
        
        # Crop with pan offset
        left = pan_x
        top = pan_y
        right = min(left + clip.w, new_width)
        bottom = min(top + clip.h, new_height)
        
        cropped = resized.crop((left, top, right, bottom))
        
        # If cropped area is smaller, pad with black
        if cropped.size != (clip.w, clip.h):
            background = Image.new('RGB', (clip.w, clip.h), (0, 0, 0))
            background.paste(cropped, (0, 0))
            cropped = background
        
        return np.array(cropped)
    
    return clip.transform(combined_effect)

# Method 3: Simple resize with fixed dimensions (alternative approach)
def simple_resize_example(image_path, duration=5):
    """Examples of different resize operations"""
    clip = ImageClip(image_path)
    clip = clip.with_duration(duration)
    
    # 1. Fixed resolution
    resized_1 = clip.with_effects([Resize((460, 720))])
    
    # 2. Scale factor
    resized_2 = clip.with_effects([Resize(0.6)])
    
    # 3. Fixed width, auto height
    resized_3 = clip.with_effects([Resize(width=800)])
    
    # 4. Animated resize (Ken Burns)
    resized_4 = clip.with_effects([
        Resize(lambda t: 1 + 0.02 * t)  # Linear zoom
    ])
    
    return resized_4

# Usage examples
try:
    print("Creating Ken Burns effect...")
    
    # Method 1: Simple animated resize
    ken_burns_clip = ken_burns_effect(current_image, duration=8, zoom_end=1.5)
    
    # Write to file
    ken_burns_clip.write_videofile(
        current_output,
        fps=24,
        codec='libx264',
        audio_codec='aac',
        verbose=False,
        logger=None
    )
    
    print(f"Success! Video saved to: {current_output}")
    
except Exception as e:
    print(f"Error: {e}")
    print("Trying alternative method...")
    
    # Fallback to simpler method
    try:
        clip = ImageClip(current_image).with_duration(8)
        simple_ken_burns = clip.with_effects([
            Resize(lambda t: 1 + 0.05 * t)  # Simple linear zoom
        ])
        
        simple_ken_burns.write_videofile(
            current_output,
            fps=24,
            codec='libx264',
            audio_codec='aac',
            verbose=False,
            logger=None
        )
        print(f"Simple method worked! Video saved to: {current_output}")
    except Exception as e2:
        print(f"All methods failed: {e2}")
        
