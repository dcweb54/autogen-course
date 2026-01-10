Perfect! If you want **context-aware visuals**, the Visual Planner must **understand the meaning, emotions, and action of each TTS line**, not just assign random clips. This ensures visuals **match the script’s intent**, making the video more engaging. Here’s how to implement a **context-aware Visual Planner**:

---

# **1. Context-Aware Design Principles**

For each TTS line, the planner should extract:

| Feature           | Purpose for Context Awareness                                                      |
| ----------------- | ---------------------------------------------------------------------------------- |
| **Emotions**      | Match the mood (hope, frustration, empowerment) → affects color grading, clip type |
| **Actions**       | Show relevant movements/gestures → reinforces message                              |
| **Settings**      | Location/environment matching the narrative                                        |
| **Objects/Props** | Helps identify visual cues and concrete clip elements                              |
| **Identity Cues** | Ensure the actor/person fits the audience context                                  |
| **Clip Query**    | Combines all above for **searchable, semantically accurate footage**               |
| **Overlay Text**  | Short summary emphasizing the message                                              |

---

# **2. Example Context-Aware Timeline JSON**

```json
{
  "timeline": [
    {
      "idx": 1,
      "text": "You feel stuck… like nothing moves? [pause]",
      "duration": 4,
      "emotions": ["frustration", "anxiety"],
      "actions": ["sitting at desk, head in hands"],
      "settings": ["home office", "apartment"],
      "objects": ["laptop", "papers", "coffee mug"],
      "identity_cues": ["young adult", "freelancer"],
      "clip_query": "young freelancer sitting frustrated at home office desk with laptop and papers",
      "overlay_text": "Feeling stuck"
    },
    {
      "idx": 2,
      "text": "Like everyone is running, you are standing still? [pause]",
      "duration": 4,
      "emotions": ["envy", "self-doubt"],
      "actions": ["standing still, watching people walk past"],
      "settings": ["busy street", "park path"],
      "objects": ["backpack", "phone"],
      "identity_cues": ["woman of color", "student"],
      "clip_query": "woman of color standing still watching blurred people walking past in park",
      "overlay_text": "Standing still"
    },
    {
      "idx": 3,
      "text": "Action beats fear. Take one small step. [pause]",
      "duration": 5,
      "emotions": ["hope", "empowerment"],
      "actions": ["walking forward, stepping confidently"],
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
      "actions": ["raising arms, looking at horizon"],
      "settings": ["hilltop", "beach", "park"],
      "objects": ["journal", "camera"],
      "identity_cues": ["young adult", "woman of color"],
      "clip_query": "young adult standing on hilltop raising arms with journal",
      "overlay_text": "Use your mind"
    }
  ]
}
```

✅ Notice how **clip_query** is fully context-aware: it combines **emotions, actions, settings, props, and identity cues** to form a **concrete visual search prompt**.

---

# **3. Implementation Approach**

### **A. Rule-Based Context Mapping (Simple)**

1. Define **emotion → visual style mapping**.
2. Define **keywords → actions/settings/props**.
3. For each TTS line:

   * Extract keywords
   * Map to emotion/action/setting/prop
   * Build `clip_query` from all fields

```python
clip_query = f"{identity_cues} {actions} in {settings} with {' and '.join(objects)}"
```

---

### **B. AI-Powered Context Extraction (Recommended)**

* Use GPT-5 Mini to **analyze each TTS line** and generate all fields in JSON:

```text
You are a Visual Planner AI.  
Input: TTS line text and duration.  
Output JSON with: idx, text, duration, emotions, actions, settings, objects, identity_cues, clip_query, overlay_text.  
Ensure visuals are context-aware: clip_query should represent **what should appear visually**, not just random stock clips.
```

* Benefits:

  * Fully context-aware
  * Scales to hundreds of lines
  * Dynamically adapts to any script

---

# **4. Integration with Automation Pipeline**

1. **TTS Agent** → generates audio
2. **Context-Aware Visual Planner** → outputs enhanced timeline JSON
3. **Clip Fetcher / AI Generator** → uses `clip_query` to get footage
4. **Video Agent (FFmpeg)** → overlays `overlay_text`, syncs TTS, applies motion/effects

---

# **5. Best Practices**

* **Prioritize Emotions & Actions** → these should dominate clip query for accurate visuals.
* **Use Settings and Props** → provide context and realism.
* **Identity Cues** → match target audience, improves relatability.
* **Keep overlay_text short** → readable in 1–2 seconds.
* **Test dynamically generated clip_query** with AI or stock APIs to ensure search accuracy.

---

I can now **build a fully working Python module** that:

* Takes your TTS-ready script
* Generates a **context-aware visual timeline**
* Outputs JSON ready for automated FFmpeg video generation

Do you want me to do that next?
