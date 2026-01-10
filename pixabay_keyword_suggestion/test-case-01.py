import os
import json
from pathlib import Path


def load_visual_txt():
    current_dir = os.path.join(os.getcwd(),'visual_generator','output-03.txt')
    if not os.path.exists(current_dir):
        print("not exit")
        return
    else:
        with open(current_dir,'r') as f:
            load = f.read()
        return load
    
    



result = json.loads(load_visual_txt())

# identify + action + setting

query = []

for visual in result['timeline']:
    # print(visual['identity cues'][0])
    # print(visual['actions'][0])
    # print(visual['settings'][0])
    query.append([visual['identity cues'][0],(visual['actions'][0]),visual['settings'][0]])
    
    
print(query)