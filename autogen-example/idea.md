Perfect — you’ve got a high-quality, context-aware, emotionally resonant output. Now, to **instruct your agent (human or AI) to consistently produce this kind of result**, you need a **clear, structured, repeatable instruction set** — almost like a *creative brief* or *prompt engineering template*.

Here’s how to instruct your agent in a **well-structured, professional, and scalable manner**:

---

## ✅ INSTRUCTION TEMPLATE FOR AGENTS:  
# “Generate Context-Aware Image Search Keywords from Transcript Segments”

---

### 🎯 GOAL  
Transform each transcript segment into **5 highly relevant, emotionally resonant, visually authentic Pexels-search-optimized keyword phrases** that reflect:
- The **literal scene** described
- The **emotional tone** (hope, fear, triumph, doubt, awe)
- The **narrative arc** (beginning, challenge, turning point, climax)
- The **symbolic or metaphorical meaning** (e.g., “backpack full of hope” → not literal backpack, but visual metaphor)

---

### 🧩 INPUT STRUCTURE (MUST BE PRESERVED)  
You will receive a JSON object with this structure:
```json
{
  "language": "string",
  "language_probability": number,
  "segments": [
    {
      "id": number,
      "text": "string",
      "start": number,
      "end": number,
      "duration": number,
      "words": [ { "word": "string", "start": number, "end": number, "duration": number }, ... ]
    },
    ...
  ]
}
```

---

### 🖋️ OUTPUT REQUIREMENTS  
1. **Preserve all original fields** — do NOT remove or alter `id`, `start`, `end`, `words`, etc.
2. **Add only one new field per segment**:  
   → `"image_keywords": [ "phrase 1", "phrase 2", ..., "phrase 5" ]`
3. Each phrase must be:
   - **Descriptive and vivid** — suitable for stock photo search (Pexels, Unsplash, etc.)
   - **Emotionally aligned** — match the mood of the segment
   - **Visually authentic** — suggest imagery that *looks like it belongs in the story*
   - **Symbolic when needed** — interpret metaphors visually (e.g., “hope” → warm light, sunrise, determined gaze)
   - **5 phrases per segment** — no more, no less
   - **Natural language** — no hashtags, no ALL CAPS, no robotic jargon

---

### 🎨 CREATIVE GUIDELINES (FOR AUTHENTICITY)

| Element          | Instruction                                                                 |
|------------------|-----------------------------------------------------------------------------|
| **Literal Scene** | Describe what you’d *actually see*: “steep rocky trail”, “lone hiker at dawn” |
| **Emotion**       | Embed feeling: “nervous beginner”, “determined underdog”, “weary but pushing” |
| **Symbolism**     | Translate metaphors: “backpack full of hope” → “sunlit backpack on trail at sunrise” |
| **Cinematic Tone**| Think like a film director: lighting, weather, framing, perspective          |
| **Avoid Clichés** | No “mountain climber victory flag” — aim for realism, subtlety, emotional truth |

---

### 📋 STEP-BY-STEP PROCESS FOR AGENTS

1. **Read the segment text carefully** — absorb the meaning, tone, and imagery.
2. **Identify key visual elements** — location, weather, objects, character state.
3. **Identify emotional subtext** — Is it hopeful? fearful? triumphant? lonely?
4. **Brainstorm literal + symbolic interpretations** — What does “doubt crept in” *look like* visually?
5. **Write 5 keyword phrases** — each should be a standalone, search-friendly, emotionally rich description.
6. **Review for authenticity** — Would this keyword return an image that *feels like this moment in the story*?
7. **Insert into JSON** — add `"image_keywords"` array to the segment, preserving all other fields.

---

### 🧪 EXAMPLE SEGMENT + OUTPUT (FOR TRAINING)

**Input Segment:**
> “Doubt crept in.”

**Bad Output (Generic):**  
❌ “sad person”, “thinking man”, “mountain climb”

**Good Output (Authentic & Contextual):**  
✅  
```json
"image_keywords": [
  "hiker sitting alone on rock looking down",
  "shadowed face showing inner struggle",
  "solitary figure against vast mountain",
  "moment of hesitation on cliff edge",
  "emotional low point during climb"
]
```

---

### 🛠️ OPTIONAL: ADDITIONAL INSTRUCTIONS FOR AI AGENTS

If using an LLM (like GPT, Claude, Gemini), preface the task with:

> “You are a cinematic visual translator. Your task is to convert each spoken segment into 5 emotionally intelligent, visually authentic, Pexels-optimized image search phrases. Prioritize mood, metaphor, and realism over literal description. Avoid clichés. Think like a film director and a poet.”

---

### 📁 DELIVERABLE FORMAT

Always return **valid JSON**, matching the input structure exactly, with only `"image_keywords"` added per segment.

---

## ✅ FINAL CHECKLIST FOR AGENTS

☐ All original fields preserved  
☐ Exactly 5 keywords per segment  
☐ Keywords are vivid, search-friendly, emotionally aligned  
☐ No robotic or generic phrases  
☐ Metaphors are visually interpreted  
☐ Matches tone and narrative progression  
☐ Valid JSON output

---

## 📌 BONUS: PROMPT SNIPPET FOR AI AGENTS

```text
You are a visual storytelling expert. Convert each transcript segment into 5 emotionally resonant, visually authentic, Pexels-search-optimized keyword phrases. Preserve all original JSON structure. Add only "image_keywords" per segment. Think cinematically: lighting, emotion, symbolism, realism. Avoid clichés. Match the story’s tone precisely.
```

---

With this instruction set, your agent — whether human editor, junior designer, or AI model — will produce **consistent, high-quality, story-driven image suggestions** every time.

Let me know if you want this as a:
- Notion template
- Google Doc brief
- API specification
- Training slide deck for your team

You’re now equipped to scale this creatively and systematically. 🚀📸






Absolutely — you can **implement this entire creative brief as a structured instruction set for your Autogen-based AI agent**. Below is a **complete, production-ready implementation** using `AssistantAgent` and `UserProxyAgent` from `autogen_agentchat`, with `OpenAIChatCompletionClient` (or compatible local LLM server), that:

✅ Accepts your JSON input  
✅ Processes each segment  
✅ Adds `"image_keywords"` per your spec  
✅ Returns valid, structured JSON  
✅ Uses your cinematic, emotionally intelligent prompt  

---

## ✅ FINAL IMPLEMENTATION

```python
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import UserMessage
import asyncio
import json

# --- CONFIGURE YOUR MODEL ---
# Replace with your local or remote model
client = OpenAIChatCompletionClient(
    model="gemma-3-1b-it",  # or "gpt-4", "llama3", etc.
    base_url="http://localhost:8080/v1",  # if using local server
    api_key="placeholder",
    # Remove response_format unless you're SURE your model supports strict JSON
)

# --- SYSTEM PROMPT: YOUR CREATIVE BRIEF ---
SYSTEM_PROMPT = """
You are a cinematic visual translator. Your task is to convert each spoken transcript segment into 5 emotionally intelligent, visually authentic, Pexels-optimized image search phrases.

## 🎯 GOAL
Transform each segment into 5 highly relevant, emotionally resonant, visually authentic keyword phrases that reflect:
- The literal scene
- The emotional tone (hope, fear, triumph, doubt, awe)
- The narrative arc
- Symbolic/metaphorical meaning (e.g., “backpack full of hope” → “sunlit backpack on trail at sunrise”)

## 🖋️ OUTPUT RULES
- PRESERVE all original JSON fields (id, start, end, words, etc.)
- ADD ONLY ONE NEW FIELD per segment: "image_keywords"
- "image_keywords" must be an array of exactly 5 strings
- Each phrase must be:
  - Vivid, search-friendly, natural language
  - Emotionally aligned
  - Visually authentic — suggest imagery that belongs in the story
  - Symbolic when needed — interpret metaphors visually
  - Avoid clichés, hashtags, robotic jargon

## 🎨 CREATIVE GUIDELINES
- Literal Scene: “steep rocky trail”, “lone hiker at dawn”
- Emotion: “nervous beginner”, “determined underdog”
- Symbolism: “doubt crept in” → “hiker sitting alone on rock looking down”
- Cinematic Tone: Think lighting, weather, framing, perspective
- Authenticity > Literalism

## 🧪 EXAMPLE
Input Segment: “Doubt crept in.”
→ Output:
"image_keywords": [
  "hiker sitting alone on rock looking down",
  "shadowed face showing inner struggle",
  "solitary figure against vast mountain",
  "moment of hesitation on cliff edge",
  "emotional low point during climb"
]

## 📋 PROCESS
1. Read segment text — absorb tone, imagery.
2. Identify visual elements + emotional subtext.
3. Brainstorm literal + symbolic interpretations.
4. Write 5 vivid, emotionally rich, search-optimized phrases.
5. Insert into segment as "image_keywords".

## 📁 DELIVERABLE
Return VALID JSON matching input structure — ONLY add "image_keywords" per segment.
"""

# --- AGENT SETUP ---
assistant = AssistantAgent(
    name="VisualKeywordAgent",
    model_client=client,
    system_message=SYSTEM_PROMPT,
)

user_proxy = UserProxyAgent(
    name="UserProxy",
    code_execution=False,  # We’re not executing code, just prompting
)

# --- MAIN FUNCTION ---
async def generate_image_keywords(transcript_json: dict) -> dict:
    """
    Accepts transcript JSON, returns same JSON with image_keywords added to each segment.
    """
    # Serialize input for LLM
    input_text = json.dumps(transcript_json, indent=2, ensure_ascii=False)

    # Send to agent
    messages = [
        UserMessage(content=input_text, source="UserProxy")
    ]

    # Get response
    response = await assistant.on_messages(messages, cancellation_token=None)

    # Extract content
    reply = response.messages[-1].content

    # Try to parse as JSON
    try:
        result = json.loads(reply)
        return result
    except json.JSONDecodeError:
        print("❌ Failed to parse LLM output as JSON. Raw output:")
        print(reply)
        raise ValueError("LLM did not return valid JSON.")

# --- EXAMPLE USAGE ---
async def main():
    sample_input = {
        "language": "en",
        "language_probability": 0.998,
        "segments": [
            {
                "id": 0,
                "text": "Doubt crept in.",
                "start": 10.5,
                "end": 13.2,
                "duration": 2.7,
                "words": [
                    {"word": "Doubt", "start": 10.5, "end": 11.1, "duration": 0.6},
                    {"word": "crept", "start": 11.1, "end": 11.8, "duration": 0.7},
                    {"word": "in.", "start": 11.8, "end": 13.2, "duration": 1.4}
                ]
            },
            {
                "id": 1,
                "text": "But I kept climbing.",
                "start": 13.5,
                "end": 16.0,
                "duration": 2.5,
                "words": [
                    {"word": "But", "start": 13.5, "end": 13.7, "duration": 0.2},
                    {"word": "I", "start": 13.7, "end": 13.8, "duration": 0.1},
                    {"word": "kept", "start": 13.8, "end": 14.2, "duration": 0.4},
                    {"word": "climbing.", "start": 14.2, "end": 16.0, "duration": 1.8}
                ]
            }
        ]
    }

    print("🧠 Processing transcript segments...")
    output = await generate_image_keywords(sample_input)

    print("\n✅ OUTPUT:")
    print(json.dumps(output, indent=2, ensure_ascii=False))

    # Validate structure
    for seg in output["segments"]:
        assert "image_keywords" in seg, "Missing image_keywords"
        assert len(seg["image_keywords"]) == 5, "Must have exactly 5 keywords"
        for kw in seg["image_keywords"]:
            assert isinstance(kw, str), "Keywords must be strings"
            assert len(kw) > 0, "Keywords must not be empty"

    print("\n✅ All segments processed successfully!")

# --- RUN ---
if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🧠 Why This Works

- **System Prompt Embeds Your Entire Brief** — tone, rules, examples, constraints.
- **Input/Output is Pure JSON** — agent receives serialized JSON, returns parsed JSON.
- **Validation Included** — checks for 5 keywords, strings, field presence.
- **Flexible Backend** — works with OpenAI, LocalAI, llama.cpp, etc.
- **Scalable** — drop in any transcript, get enriched output.

---

## 🚀 PRO TIPS

### 1. If Your Model Doesn’t Return Valid JSON
→ Add this instruction to `SYSTEM_PROMPT`:
```text
IMPORTANT: Your output must be valid JSON. Do not add explanations, markdown, or text outside the JSON structure.
```

### 2. For Better JSON Reliability (if using GPT-4-turbo or compatible)
Uncomment and add to `OpenAIChatCompletionClient`:
```python
response_format={ "type": "json_object" }
```
*(Only if your model/backend supports it!)*

### 3. Want to Log or Retry on Failure?
Wrap `generate_image_keywords()` in a retry loop or add fallback parsing.

---

## 📁 Output Example (What You’ll Get)

```json
{
  "language": "en",
  "language_probability": 0.998,
  "segments": [
    {
      "id": 0,
      "text": "Doubt crept in.",
      "start": 10.5,
      "end": 13.2,
      "duration": 2.7,
      "words": [...],
      "image_keywords": [
        "hiker sitting alone on rock looking down",
        "shadowed face showing inner struggle",
        "solitary figure against vast mountain",
        "moment of hesitation on cliff edge",
        "emotional low point during climb"
      ]
    },
    {
      "id": 1,
      "text": "But I kept climbing.",
      "start": 13.5,
      "end": 16.0,
      "duration": 2.5,
      "words": [...],
      "image_keywords": [
        "determined hiker ascending steep trail at sunset",
        "muddy boots pushing forward uphill",
        "sweat on brow, eyes focused ahead",
        "resilient climber ignoring fatigue",
        "small figure conquering massive mountain"
      ]
    }
  ]
}
```

---

## 🛠️ Next Steps

Want to turn this into:
- **FastAPI endpoint?** → Wrap `generate_image_keywords()` in a POST route.
- **CLI tool?** → Add `argparse` to read from file.
- **Batch processor?** → Loop over multiple transcripts.
- **GUI?** → Use Gradio or Streamlit.

---

Let me know if you want any of those extensions — I’ll build it for you. You now have a **cinematic, emotionally intelligent, auto-scaling visual keyword engine** 🎥📸🚀