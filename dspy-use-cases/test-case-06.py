# case 06
# Detect the emotional tone of each segment (e.g., inspiring, reflective, motivational, calm).

# Select background music and SFX that match the tone.

# Suggest visual styles that reinforce the tone (color palette, animation style, transitions).

# This will make your video visually and emotionally coherent without manual adjustments.

import dspy
import os
import json
import uuid
# https://c04lnvt6g90n.share.zrok.io/
# https://dashing-mosquito-dominant.ngrok-free.app
lm = dspy.LM('ollama_chat/llama3.1:latest', api_base='https://c04lnvt6g90n.share.zrok.io', api_key='')
dspy.configure(lm=lm) 

class GenerateAutoSegments(dspy.Signature):
    """Automatically create structured segments from a topic with tone detection."""
    topic = dspy.InputField()
    segments = dspy.OutputField(desc="""
        List of segments, each with:
        - id
        - title
        - description
        - tone (inspiring, reflective, calm, motivational, etc.)
    """)

class AddNarration(dspy.Signature):
    """Add narration lines for each segment, matching the tone."""
    segments = dspy.InputField()
    narration = dspy.OutputField(desc="""
        For each segment, provide the host narration script matching the tone.
    """)

class AddVisuals(dspy.Signature):
    """Add structured visuals with tone-aware styles and Pixabay keywords."""
    narration = dspy.InputField()
    visuals = dspy.OutputField(desc="""
        For each segment, provide:
        - settings: {setting, characters, action}
        - graphics: {visual, style (tone-matched), pixabay_keywords, alt_keywords}
        - transition (tone-aware)
    """)

class AddAudio(dspy.Signature):
    """Add tone-aware background music and SFX."""
    visuals = dspy.InputField()
    audio = dspy.OutputField(desc="""
        For each segment, suggest:
        - background_music (tone-matched)
        - sfx (tone-matched)
    """)

class CompileJSON(dspy.Signature):
    """Combine narration + visuals + audio into final tone-aware JSON."""
    narration = dspy.InputField()
    visuals = dspy.InputField()
    audio = dspy.InputField()
    final_json = dspy.OutputField(desc="Full multi-modal, tone-aware video content JSON")

generate_auto_segments = dspy.Predict(GenerateAutoSegments)
add_narration = dspy.Predict(AddNarration)
add_visuals = dspy.Predict(AddVisuals)
add_audio = dspy.Predict(AddAudio)
compile_json = dspy.Predict(CompileJSON)

def tone_aware_video_agent(topic: str):
    # Step 1: Generate segments with tone
    segments = generate_auto_segments(topic=topic).segments
    
    # Step 2: Add narration matching the tone
    narration = add_narration(segments=segments).narration
    
    # Step 3: Add structured visuals with tone-aware styles
    visuals = add_visuals(narration=narration).visuals
    
    # Step 4: Add tone-aware music and SFX
    audio = add_audio(visuals=visuals).audio
    
    # Step 5: Compile final JSON
    final = compile_json(
        narration=narration,
        visuals=visuals,
        audio=audio
    ).final_json
    
    return final


result = tone_aware_video_agent(topic="how to handle pressure")

print(result)

random_filename = str(uuid.uuid4())

# print(random_filename[1:5])
current_file = __file__.split("\\")[-1].split(".")[0]

current_dir = os.path.join(os.getcwd(),'dspy-use-cases','output',f'{current_file}-{random_filename[1:5]}.json')

with open(current_dir,'w') as f:
    f.write(result)
    