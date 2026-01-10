import dspy
import os
import json
import uuid

lm = dspy.LM('ollama_chat/llama3.1:latest', api_base='https://k38wbq5ylygc.share.zrok.io', api_key='')
dspy.configure(lm=lm)

class GenerateScript(dspy.Signature):
    """Generate a rich multi-segment video script on a topic."""
    topic = dspy.InputField()
    script = dspy.OutputField(desc="List of segments with narration")

# class AddVisualIdeas(dspy.Signature):
#     """Add detailed visual directions for each segment to match narration context."""
#     script = dspy.InputField()
#     visuals = dspy.OutputField(desc="Segments enriched with visual ideas")


class AddVisualIdeas(dspy.Signature):
    """Add detailed structured visual directions for each narration segment."""
    script = dspy.InputField()
    visuals = dspy.OutputField(desc="""
        For each segment, output structured visual details:
        - Setting (location/environment)
        - Characters (who is in the shot)
        - Action (what is happening)
        - Emotion (tone/feeling of the scene)
    """)

class CompileFinalJSON(dspy.Signature):
    """Combine script and visuals into final structured JSON."""
    script = dspy.InputField()
    visuals = dspy.InputField()
    final_json = dspy.OutputField(desc="Video content package for automation")


generate_script = dspy.Predict(GenerateScript)
add_visuals = dspy.Predict(AddVisualIdeas)
compile_json = dspy.Predict(CompileFinalJSON)


def video_content_agent(topic: str):
    # Step 1: Generate script
    script = generate_script(topic=topic).script

    # Step 2: Add visual directions
    visuals = add_visuals(script=script).visuals

    # Step 3: Compile into final JSON
    final = compile_json(
        script=script,
        visuals=visuals
    ).final_json

    return final



result = generate_script(topic="Overcoming self-doubt for young professionals")

print(result)

# random_filename = str(uuid.uuid4())

# # print(random_filename[1:5])
# current_file = __file__.split("\\")[-1].split(".")[0]

# current_dir = os.path.join(os.getcwd(),'dspy-use-cases','output',f'{current_file}-{random_filename[1:5]}.json')

# with open(current_dir,'w') as f:
#     f.write(result)