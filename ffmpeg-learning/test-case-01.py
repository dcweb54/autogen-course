import os
from pathlib import Path


print(len("welcome"))
print(os.getcwd())
print(os.path.join(os.getcwd(), "ffmpeg-learning"))

print(__file__)

print(Path(__file__).parent)

print(len("welcome"))
