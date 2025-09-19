from moviepy import ImageClip
import os


def pan_and_zoom(
    image_path: str,
    duration: float = 5,
    output_path: str = "pan_zoom.mp4",
    zoom_factor: float = 1.2,
    fps: int = 24,
):
    """
    Creates a Ken Burns effect video from a single image.

    Args:
        image_path: Path to the input image.
        duration: Duration of the output video.
        output_path: Path to save the resulting video.
        zoom_factor: Final zoom scale (e.g., 1.2 = 20% zoom in).
        fps: Frames per second of the output video.
    """
    # Load image clip
    clip = ImageClip(image_path)

    # Calculate size zooming
    w, h = clip.size
    final_w, final_h = int(w * zoom_factor), int(h * zoom_factor)

    # Apply resize (zoom) and position (pan) over time
    def zoom_pos(t):
        # Linear interpolation for size
        scale = 1 + (zoom_factor - 1) * (t / duration)
        new_w, new_h = int(w * scale), int(h * scale)
        # Calculate position to keep it centered (pan slightly)
        x = (w - new_w) // 2
        y = (h - new_h) // 2
        return (x, y)

    clip = (
        clip.resized(lambda t: 1 + (zoom_factor - 1) * t / duration)
        .with_position(lambda t: ("center", "center"))
        .with_duration(duration)
    )

    clip.write_videofile(
        output_path,
        fps=fps,
        codec="libx264",
        preset="ultrafast",
        threads=8,
        ffmpeg_params=["-crf", "25"],
    )


# Example usage
if __name__ == "__main__":
    current_image = os.path.join(os.path.join(os.getcwd(), "images"), "1.jpg")
    current_work_dir = os.path.join(
        os.path.join(os.getcwd(), "moviepy-learning-material-output"), "pan_zoom01.mp4"
    )

    pan_and_zoom(
        current_image, duration=5, output_path=current_work_dir, zoom_factor=1.2
    )
