
import dspy
import json
import os
import uuid
#  test case 03
# lm = dspy.LM("openai/gpt-4o-mini", api_key="YOUR_OPENAI_API_KEY",baseur)
# http://localhost:11434
# https://ll4zmdtj81cb.share.zrok.io
lm = dspy.LM('ollama_chat/llama3.1:latest', api_base='https://ll4zmdtj81cb.share.zrok.io', api_key='')
dspy.configure(lm=lm)


# 1. Define signatures
class GenerateOutline(dspy.Signature):
    """Generate a structured outline for a video script on a given topic."""
    topic = dspy.InputField()
    outline = dspy.OutputField(desc="Numbered list of sections for the video")

class ExpandScenes(dspy.Signature):
    """Expand outline into detailed scenes with narration and visuals."""
    outline = dspy.InputField()
    scenes = dspy.OutputField(desc="Detailed scene breakdown with narration + visuals")

class AddBroll(dspy.Signature):
    """Suggest B-roll shots for each scene to enhance visuals."""
    scenes = dspy.InputField()
    broll = dspy.OutputField(desc="List of B-roll ideas matching each scene")

class WriteScript(dspy.Signature):
    """Convert detailed scenes + B-roll into JSON format for automation."""
    scenes = dspy.InputField()
    broll = dspy.InputField()
    script_json = dspy.OutputField(desc="Video script in JSON with scene breakdown, narration, visuals, and b-roll")

# 2. Create modules
generate_outline = dspy.Predict(GenerateOutline)
expand_scenes = dspy.Predict(ExpandScenes)
add_broll = dspy.Predict(AddBroll)
write_script = dspy.Predict(WriteScript)

# 3. Build pipeline
def create_video_script_json(topic: str):
    outline = generate_outline(topic=topic).outline
    scenes = expand_scenes(outline=outline).scenes
    broll = add_broll(scenes=scenes).broll
    script_json = write_script(scenes=scenes, broll=broll).script_json

    # Ensure JSON is valid Python dict
    try:
        return json.loads(script_json)
    except json.JSONDecodeError:
        return {"error": "Model did not return valid JSON", "raw_output": script_json}

# Example run
result = create_video_script_json("Overcoming self-doubt for young professionals")

random_filename = str(uuid.uuid4())

# print(random_filename[1:5])
current_file = __file__.split("\\")[-1].split(".")[0]

current_dir = os.path.join(os.getcwd(),'dspy-use-cases','output',f'{current_file}-{random_filename[1:5]}.json')

with open(current_dir,'w') as f:
    f.write(result)


