# case 07

import dspy

class GenerateAutoSegments(dspy.Signature):
    """Automatically create structured segments from a topic with tone detection."""
    topic = dspy.InputField()
    segments = dspy.OutputField(desc="""
        List of segments, each with:
        - id
        - title
        - description
        - tone (inspiring, reflective, motivational, calm, energetic, etc.)
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

class AddVoiceover(dspy.Signature):
    """Add TTS voice suggestions matching tone for each segment."""
    narration = dspy.InputField()
    voiceover = dspy.OutputField(desc="""
        For each segment, provide:
        - voice_style (calm, energetic, warm, authoritative)
        - language
        - TTS_voice_id or settings for automated voice generation
    """)

class CompileJSON(dspy.Signature):
    """Combine narration, visuals, audio, and voiceover into final JSON."""
    narration = dspy.InputField()
    visuals = dspy.InputField()
    audio = dspy.InputField()
    voiceover = dspy.InputField()
    final_json = dspy.OutputField(desc="Full multi-modal, tone-aware, TTS-ready video JSON")

generate_auto_segments = dspy.Predict(GenerateAutoSegments)
add_narration = dspy.Predict(AddNarration)
add_visuals = dspy.Predict(AddVisuals)
add_audio = dspy.Predict(AddAudio)
add_voiceover = dspy.Predict(AddVoiceover)
compile_json = dspy.Predict(CompileJSON)

def tts_ready_video_agent(topic: str):
    # Step 1: Generate segments with tone
    segments = generate_auto_segments(topic=topic).segments

    # Step 2: Add narration matching the tone
    narration = add_narration(segments=segments).narration

    # Step 3: Add structured visuals with tone-aware styles
    visuals = add_visuals(narration=narration).visuals

    # Step 4: Add tone-aware music and SFX
    audio = add_audio(visuals=visuals).audio

    # Step 5: Add TTS voiceover suggestions
    voiceover = add_voiceover(narration=narration).voiceover

    # Step 6: Compile final JSON
    final = compile_json(
        narration=narration,
        visuals=visuals,
        audio=audio,
        voiceover=voiceover
    ).final_json

    return final


print(tts_ready_video_agent(topic="Overcoming self-doubt for young professionals"))
