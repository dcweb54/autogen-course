import os
from pathlib import Path


from moviepy import ImageClip

def pan_and_zoom(image_path: str, duration: float = 5, output_path: str = "pan_zoom.mp4"):
    """
    Creates a video from an image with a pan and zoom effect.

    Args:
        image_path: Path to the input image.
        duration: Duration of the output video in seconds.
        output_path: Path to save the resulting video.
    """
    # Load image
    clip = ImageClip(image_path, duration=duration)

    # Apply zoom-in effect: scale from 1x to 1.2x
    clip = clip.resized(lambda t: 1 + 0.2 * t / duration)

    # Apply pan effect: move from left to right
    clip = clip.with_position(lambda t: ('center', -50 * t / duration))  # vertical pan example

    # Export video
    clip.write_videofile(output_path, fps=24, codec="libx264")

# Example usage
if __name__ == "__main__":
    current_image = os.path.join(os.path.join(os.getcwd(),'images'),'1.jpg')
    current_work_dir = os.path.join(os.path.join(os.getcwd(),'moviepy-learning-material-output'),'pan_zoom.mp4')
    pan_and_zoom(current_image, duration=5, output_path=current_work_dir)
