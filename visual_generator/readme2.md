Absolutely! We can **upgrade your Visual Planner** to not just map lines to clips and overlay text, but to **extract key elements per beat**—turning abstract motivational lines into **concrete, searchable video assets**. This is perfect for automation with stock footage or AI-generated visuals.

---

# **1. Enhanced Timeline Structure**

Each line (beat) will now contain:

| Key             | Description                                     |
| --------------- | ----------------------------------------------- |
| `idx`           | Line number (from TTS)                          |
| `text`          | Original TTS line                               |
| `duration`      | Duration in seconds                             |
| `emotions`      | Emotional tone (shock, hope, empowerment, etc.) |
| `actions`       | Physical actions or gestures                    |
| `settings`      | Locations or environments                       |
| `objects`       | Props to include in scene                       |
| `identity_cues` | Demographics / character cues                   |
| `clip_query`    | Concise description for searching stock/AI clip |
| `overlay_text`  | Short text for video overlay                    |

---

# **2. Example JSON Output**

```json
{
  "timeline": [
    {
      "idx": 1,
      "text": "You feel stuck… like nothing moves? [pause]",
      "duration": 4,
      "emotions": ["frustration", "anxiety"],
      "actions": ["sitting at desk", "head in hands"],
      "settings": ["office", "apartment"],
      "objects": ["laptop", "papers", "coffee mug"],
      "identity_cues": ["young adult", "freelancer"],
      "clip_query": "frustrated young adult sitting at desk with laptop and papers",
      "overlay_text": "Feeling stuck"
    },
    {
      "idx": 2,
      "text": "Like everyone is running, you are standing still? [pause]",
      "duration": 4,
      "emotions": ["envy", "self-doubt"],
      "actions": ["standing still", "watching people walk past"],
      "settings": ["busy street", "park path"],
      "objects": ["backpack", "phone"],
      "identity_cues": ["woman of color", "student"],
      "clip_query": "young woman standing still watching people walk past in street",
      "overlay_text": "Standing still"
    },
    {
      "idx": 3,
      "text": "Action beats fear. Take one small step. [pause]",
      "duration": 5,
      "emotions": ["hope", "empowerment"],
      "actions": ["walking forward", "stepping confidently"],
      "settings": ["street", "trail", "office corridor"],
      "objects": ["shoes", "bag"],
      "identity_cues": ["young adult", "freelancer"],
      "clip_query": "young adult confidently stepping forward on street",
      "overlay_text": "One step"
    },
    {
      "idx": 4,
      "text": "Your mind is your power. Use it. [pause]",
      "duration": 3,
      "emotions": ["empowerment", "confidence"],
      "actions": ["raising arms", "looking at horizon"],
      "settings": ["hilltop", "beach", "park"],
      "objects": ["journal", "camera"],
      "identity_cues": ["young adult", "woman of color"],
      "clip_query": "young adult standing on hilltop raising arms with journal",
      "overlay_text": "Use your mind"
    }
  ]
}
```

---

# **3. How to Implement This**

### **A. Rule-Based Approach (Simple)**

1. Map **keywords** from each TTS line to emotions, actions, and settings.
2. Assign **props/identity cues** based on topic context.
3. Generate **clip_query** automatically by combining elements.

```python
import json

tts_script = {
    "lines":[
        {"idx":1, "text":"You feel stuck… like nothing moves? [pause]", "duration":4},
        {"idx":2, "text":"Like everyone is running, you are standing still? [pause]", "duration":4},
        {"idx":3, "text":"Action beats fear. Take one small step. [pause]", "duration":5},
        {"idx":4, "text":"Your mind is your power. Use it. [pause]", "duration":3}
    ]
}

timeline = []

# Simple mapping dictionary (expandable)
mapping = {
    "stuck": {"emotions":["frustration"], "actions":["sitting at desk"], "settings":["office"], "objects":["laptop","papers"], "identity_cues":["young adult"]},
    "standing still": {"emotions":["self-doubt"], "actions":["standing still"], "settings":["street"], "objects":["phone"], "identity_cues":["student"]},
    "one small step": {"emotions":["hope"], "actions":["walking forward"], "settings":["street"], "objects":["shoes"], "identity_cues":["freelancer"]},
    "mind is your power": {"emotions":["empowerment"], "actions":["raising arms"], "settings":["hilltop"], "objects":["journal"], "identity_cues":["young adult"]}
}

overlay_texts = ["Feeling stuck", "Standing still", "One step", "Use your mind"]

for i, line in enumerate(tts_script["lines"]):
    key = list(mapping.keys())[i]
    props = mapping[key]
    clip_query = f"{props['identity_cues'][0]} {props['actions'][0]} in {props['settings'][0]} with {' and '.join(props['objects'])}"
    
    timeline.append({
        "idx": line["idx"],
        "text": line["text"],
        "duration": line["duration"],
        "emotions": props["emotions"],
        "actions": props["actions"],
        "settings": props["settings"],
        "objects": props["objects"],
        "identity_cues": props["identity_cues"],
        "clip_query": clip_query,
        "overlay_text": overlay_texts[i]
    })

visual_plan = {"timeline": timeline}

with open("visual_plan_enhanced.json", "w") as f:
    json.dump(visual_plan, f, indent=4)

print("Enhanced visual plan generated!")
```

---

### **B. AI-Powered Approach (Smart & Scalable)**

* Prompt GPT-5 Mini to **extract key elements** per TTS line and generate timeline JSON:

```text
You are a Visual Planner AI.  
Input: A TTS script line with duration.  
Output JSON with keys: idx, text, duration, emotions, actions, settings, objects, identity_cues, clip_query, overlay_text.  
Example line: "You feel stuck… like nothing moves?"  
Generate concrete, searchable clip descriptions for each beat.
```

* This method can **handle thousands of lines dynamically** and produce richer, more varied clip queries.

---

# **4. Integration with Video Automation**

1. **TTS Agent** → generates audio per line.
2. **Enhanced Visual Planner** → outputs `timeline` JSON with emotions, actions, props, clip_query, overlay_text.
3. **Stock Clip / AI Clip Fetcher** → uses `clip_query` to pull footage.
4. **Video Agent (FFmpeg)** → overlays text, syncs audio, applies motion/effects.

---

💡 **Pro Tip:**

* Use `emotions`, `actions`, `settings`, `objects`, `identity_cues` to **rank or filter stock clips** automatically.
* `clip_query` becomes the main **searchable prompt** for AI-generated or stock footage.
* This approach turns **abstract motivational lines into concrete, automatable visuals**.

---

I can **create a fully working Python module** for you that:

* Takes a TTS-ready JSON script
* Outputs this **enhanced visual planner JSON with all key elements**
* Directly usable with your FFmpeg automation system

Do you want me to do that next?
