from moviepy import (
    VideoClip,
    VideoFileClip,
    ImageSequenceClip,
    ImageClip,
    TextClip,
    ColorClip,
    AudioFileClip,
    AudioClip,
    concatenate_videoclips
)

import os

# C:\Users\admin\projects\python-project\autogen-course\moviepy-learning-material\8928261-uhd_3840_2160_25fps.mp4

# Get the current working directory
current_dir = os.getcwd()
print(f"Current working directory: {current_dir}")

input_dir = os.path.join(current_dir, "moviepy-learning-material")
os.makedirs(input_dir, exist_ok=True) # exist_ok prevents error if folder already exists
print(f"Created directory: {input_dir}")


file_path = os.path.join(input_dir, "8928261-uhd_3840_2160_25fps.mp4")
print(f"File mp4: {file_path}")
#  make sure folder should be exist
# os.makedirs('moviepy-learning-material-output', exist_ok=True)


# Load video and audio clips
video = VideoFileClip(filename=file_path)
audio = AudioFileClip("audio.wav")



# Optionally scale audio volume (e.g. 80% = 0.8)
# if reduce_audio_volume != 1.0:
#     audio = audio * reduce_audio_volume

# If audio is longer than video, cut it; if shorter, video will have silence
# audio = audio.subclipped(0, video.duration)

# video.with_duration(audio.duration)

# Attach the audio to the video
video = video.with_audio(audio)

video = video.with_duration(audio.duration)


# output folder with file

output_dir = os.path.join(current_dir, "moviepy-learning-material-output")
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "sample01.mp4")

print(f"output path created {output_file}")



# Write final video
video.write_videofile(filename=output_file, fps=24, audio_codec="aac")