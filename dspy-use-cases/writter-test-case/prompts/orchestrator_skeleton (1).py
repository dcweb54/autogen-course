import json
from typing import Dict, Any

# Existing helper stubs
def call_llm(system: str, user: str):
    # Replace with actual LLM API call
    # For demo, return a mock structured JSON plan
    return {
        "music_track": "assets/music/uplifting_background.mp3",
        "segments": [
            {"line_idx": 0, "start": 0, "end": 5, "volume": -12, "fade_in": 1, "fade_out": 1},
            {"line_idx": 1, "start": 5, "end": 11, "volume": -10, "fade_in": 0, "fade_out": 1},
            {"line_idx": 2, "start": 11, "end": 15, "volume": -12, "fade_in": 0, "fade_out": 0},
            {"line_idx": 3, "start": 15, "end": 20, "volume": -10, "fade_in": 0, "fade_out": 1},
            {"line_idx": 4, "start": 20, "end": 24, "volume": -8, "fade_in": 0, "fade_out": 2}
        ],
        "overall_volume": -6,
        "outro_fade": 3
    }

# LLM-driven Audio Planner Agent
def audio_planner_agent(manifest: Dict[str, Any], use_llm: bool = True) -> Dict[str, Any]:
    script = manifest.get('script', {})

    if use_llm:
        # Prepare system + user prompts
        system_prompt = """
        You are an Audio Planning Agent. Your task is to design a background music plan
        for a motivational short-form video.

        Guidelines:
        - Select a music track that matches the theme and tone of the script.
        - Split timeline into segments aligned with narration lines.
        - Suggest volume levels, fade-ins, fade-outs.
        - Ensure background does not overpower the voice narration.

        Return JSON as:
        {"music_track":..., "segments":[{"line_idx":...,"start":...,"end":...,"volume":...,"fade_in":...,"fade_out":...}],"overall_volume":...,"outro_fade":...}
        """

        user_prompt = json.dumps(script)
        audio_plan = call_llm(system_prompt, user_prompt)

    else:
        # Fallback to rule-based plan
        theme = script.get("theme", "general")
        track = "assets/music/uplifting_background.mp3" if "motivation" in theme.lower() else "assets/music/soft_focus.mp3"
        segments = []
        time_cursor = 0
        for idx, line in enumerate(script.get('lines', [])):
            seg = {
                "line_idx": idx,
                "start": time_cursor,
                "end": time_cursor + line.get("duration", 5),
                "volume": -12 if line.get("has_voice", True) else -3,
                "fade_in": 1,
                "fade_out": 1
            }
            segments.append(seg)
            time_cursor += line.get("duration", 5)
        audio_plan = {
            "music_track": track,
            "segments": segments,
            "overall_volume": -6,
            "outro_fade": 3
        }

    manifest['audio_plan'] = audio_plan
    manifest['status'] = 'audio_planned'
    return manifest

# Audio Producer remains mostly the same
def audio_producer_agent(manifest: Dict[str, Any]) -> Dict[str, Any]:
    audio_plan = manifest.get("audio_plan", {})
    voice_files = manifest.get("audio", {}).get("voice_files", [])

    # Store planned instructions (can be rendered later)
    mixed_output = "assets/final_mix.mp3"
    manifest['final_audio'] = {
        "music": audio_plan.get("music_track"),
        "segments": audio_plan.get("segments"),
        "voice_files": voice_files,
        "output": mixed_output
    }
    manifest['status'] = 'audio_done'
    return manifest
