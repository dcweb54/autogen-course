import dspy
import os
import json
import uuid

# test case -02
lm = dspy.LM('ollama_chat/llama3.1:latest', api_base='https://ll4zmdtj81cb.share.zrok.io', api_key='')
dspy.configure(lm=lm)


class GenerateScript(dspy.Signature):
    """Generate a rich multi-segment video script on a topic."""
    topic = dspy.InputField()
    script = dspy.OutputField(desc="List of segments with narration")

class AddStructuredVisuals(dspy.Signature):
    """Add structured visuals for each segment with clear fields."""
    script = dspy.InputField()
    visuals = dspy.OutputField(desc="""
        For each segment, return:
        - setting (location/environment)
        - characters (who is in the shot)
        - action (what happens in the shot)
        - graphics (on-screen overlays or animations)
        - transition (camera or editing effect)
    """)

class CompileFinalJSON(dspy.Signature):
    """Combine script and visuals into automation-ready JSON."""
    script = dspy.InputField()
    visuals = dspy.InputField()
    final_json = dspy.OutputField(desc="Video content package with narration + visuals")

generate_script = dspy.Predict(GenerateScript)
add_visuals = dspy.Predict(AddStructuredVisuals)
compile_json = dspy.Predict(CompileFinalJSON)

def video_content_agent(topic: str):
    # Step 1: Generate the narration script
    script = generate_script(topic=topic).script

    # Step 2: Enrich script with structured visuals
    visuals = add_visuals(script=script).visuals

    # Step 3: Compile into final JSON
    final = compile_json(
        script=script,
        visuals=visuals
    ).final_json

    return final


result = video_content_agent(topic="Overcoming self-doubt for young professionals")


random_filename = str(uuid.uuid4())

# print(random_filename[1:5])
current_file = __file__.split("\\")[-1].split(".")[0]

current_dir = os.path.join(os.getcwd(),'dspy-use-cases','output',f'{current_file}-{random_filename[1:5]}.json')

with open(current_dir,'w') as f:
    f.write(result)