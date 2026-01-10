import openai
import json

openai.api_key = "YOUR_OPENAI_API_KEY"

prompts = """"
You are a motivational scriptwriter.

Task:
- Create a short motivational script for the topic: "{topic}"
- Structure it as lines for TTS with these keys:
    - "idx": line number starting from 1
    - "text": the line content (include optional [pause] where appropriate)
    - "duration": approximate speaking time in seconds
- Keep sentences short, punchy, and TTS-friendly
- Total script duration ~15–20 seconds
- Output **ONLY JSON** with key "lines" as a list

Example output format:
{
    "lines": [
        {"idx":1, "text":"You feel stuck… like nothing moves? [pause]", "duration":4},
        {"idx":2, "text":"Like everyone is running, you are standing still? [pause]", "duration":4},
        {"idx":3, "text":"Action beats fear. Take one small step. [pause]", "duration":5},
        {"idx":4, "text":"Your mind is your power. Use it. [pause]", "duration":3}
    ]
}

"""


def generate_tts_ready_script(topic):
    prompt = f"""
    You are a motivational scriptwriter.
    Generate a short motivational script for the topic: "{topic}"
    Format it as JSON with key "lines":
    - "idx": line number starting from 1
    - "text": TTS-ready line (use [pause] where appropriate)
    - "duration": approximate seconds
    Total duration ~20 seconds.
    Output ONLY JSON.
    """

    response = openai.ChatCompletion.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
    )

    script_json = response.choices[0].message.content

    # Validate JSON
    try:
        script_data = json.loads(script_json)
        return script_data
    except:
        print("Error: Invalid JSON returned")
        return None


# Example usage
topic = "Overcoming self-doubt"
script = generate_tts_ready_script(topic)
print(json.dumps(script, indent=4))
