Got it! You want your **Visual Planner** to output JSON in a **timeline-focused structure** where each line contains:

* `idx` → line number
* `clip_query` → search query or description for stock/AI clip
* `duration` → seconds (matching TTS line)
* `overlay_text` → short text to overlay on the video

Here’s how to implement that.

---

# **1. Python Implementation Example (Rule-Based)**

```python
import json

# Example TTS-ready script
tts_script = {
    "lines":[
        {"idx":1, "text":"You feel stuck… like nothing moves? [pause]", "duration":4},
        {"idx":2, "text":"Like everyone is running, you are standing still? [pause]", "duration":4},
        {"idx":3, "text":"Action beats fear. Take one small step. [pause]", "duration":5},
        {"idx":4, "text":"Your mind is your power. Use it. [pause]", "duration":3}
    ]
}

# Visual query mapping (simple example)
visual_queries = [
    "person sitting frustrated desk close-up",
    "people walking blurred street",
    "foot stepping forward slow-mo",
    "person on hilltop arms raised"
]

# Overlay text mapping (short & punchy)
overlay_texts = ["Feeling stuck", "Standing still", "One step", "Use your mind"]

# Generate timeline JSON
timeline = []

for i, line in enumerate(tts_script["lines"]):
    timeline.append({
        "idx": line["idx"],
        "clip_query": visual_queries[i % len(visual_queries)],
        "duration": line["duration"],
        "overlay_text": overlay_texts[i % len(overlay_texts)]
    })

visual_plan = {"timeline": timeline}

# Save JSON
with open("visual_plan_timeline.json", "w") as f:
    json.dump(visual_plan, f, indent=4)

print("Visual timeline JSON generated!")
```

---

# **2. Sample Output (`visual_plan_timeline.json`)**

```json
{
    "timeline": [
        {"idx":1, "clip_query":"person sitting frustrated desk close-up","duration":4,"overlay_text":"Feeling stuck"},
        {"idx":2, "clip_query":"people walking blurred street","duration":4,"overlay_text":"Standing still"},
        {"idx":3, "clip_query":"foot stepping forward slow-mo","duration":5,"overlay_text":"One step"},
        {"idx":4, "clip_query":"person on hilltop arms raised","duration":3,"overlay_text":"Use your mind"}
    ]
}
```

---

# **3. How to Integrate With Automation**

1. **TTS Agent** → generates audio lines (same duration as timeline)
2. **Visual Planner** → outputs `timeline` JSON
3. **Video Agent / FFmpeg** → uses `clip_query` to:

   * Fetch stock clip / AI-generated image
   * Cut/extend clip to match `duration`
   * Overlay `overlay_text`
4. **Synchronize** TTS audio with clip timeline

---

# **4. Optional AI-Powered Visual Planner**

Instead of hardcoding `clip_query` and `overlay_text`, you can prompt GPT:

```text
You are a visual planner for short motivational videos.
Input: TTS-ready JSON script line with idx, text, duration.
Output JSON with keys:
- idx
- clip_query (short descriptive search query for stock or AI clip)
- duration
- overlay_text (short punchy text for video overlay)
```

GPT can generate **dynamic queries** per line automatically for more varied visuals.

---

💡 **Pro Tip:**

* `clip_query` can later be used with **stock clip APIs or AI image generation** (MidJourney / DALL·E).
* `overlay_text` should match the **TTS line key message** to make your video readable even without sound.

---

If you want, I can **create a ready-to-use Python Visual Planner module** that:

* Takes any TTS-ready JSON
* Outputs this **timeline JSON** automatically
* Can optionally generate **clip queries dynamically via GPT**

Do you want me to create that next?


 black and white line drawing storyboard of a woman with short black hair wearing a beanie in nature in front of bushes looking at her phone with a smile on her face