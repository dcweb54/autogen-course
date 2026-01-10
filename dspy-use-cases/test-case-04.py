import dspy
import json
import os
import uuid

#  test case 04
# lm = dspy.LM("openai/gpt-4o-mini", api_key="YOUR_OPENAI_API_KEY",baseur)
lm = dspy.LM('ollama_chat/llama3.1:latest', api_base='http://localhost:11434', api_key='')
dspy.configure(lm=lm)

class GenerateSegments(dspy.Signature):
    """Expand a topic into structured video segments."""
    topic = dspy.InputField()
    segments = dspy.OutputField(desc="""
        List of segments, each with:
        - id
        - title
        - description
    """)

class AddNarration(dspy.Signature):
    """Add narration lines for each segment."""
    segments = dspy.InputField()
    narration = dspy.OutputField(desc="""
        For each segment, provide a narration script (host lines).
    """)

class AddVisuals(dspy.Signature):
    """Add structured visuals + Pixabay keyword suggestions for each segment."""
    narration = dspy.InputField()
    visuals = dspy.OutputField(desc="""
        For each segment, provide:
        - settings: {setting, characters, action}
        - graphics: {visual, pixabay_keywords, alt_keywords}
        - transition
    """)

class CompileJSON(dspy.Signature):
    """Combine narration + visuals into one final JSON package."""
    narration = dspy.InputField()
    visuals = dspy.InputField()
    final_json = dspy.OutputField(desc="List of segments with narration + visuals in JSON")

generate_segments = dspy.Predict(GenerateSegments)
add_narration = dspy.Predict(AddNarration)
add_visuals = dspy.Predict(AddVisuals)
compile_json = dspy.Predict(CompileJSON)

def video_content_agent(topic: str):
    # Step 1: Generate segment breakdown
    segments = generate_segments(topic=topic).segments

    # Step 2: Add narration
    narration = add_narration(segments=segments).narration

    # Step 3: Add structured visuals
    visuals = add_visuals(narration=narration).visuals

    # Step 4: Merge into final JSON
    final = compile_json(
        narration=narration,
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