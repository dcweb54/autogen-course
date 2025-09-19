import os
from pathlib import Path
import shutil
import json



def handle_image():
    #  current directory
    current_dir = Path(os.path.join(os.getcwd(), "image_downloads"))
    # target directory
    target_dir = Path(os.path.join(os.getcwd(), "images"))

    for file in current_dir.iterdir():
        if file.is_file():
            new_name = "1.jpg"
            new_path = target_dir / new_name  # new folder + new name
            # file.rename(new_path)
            shutil.move(str(file), str(new_path))
            print(f"Moved + renamed {file.name} → {new_path}")
        


def handle_transcription_out():
    with open("output.json", "r", encoding="utf-8") as f:
        transcription = json.load(f)
    segments = transcription['segments']
    
    for segment in segments:
        # print(segment)
        yield segment
        
        
number_generator = handle_transcription_out()

# Iterate through the generator to get values
for num in number_generator:
  print(str(num['id']))
