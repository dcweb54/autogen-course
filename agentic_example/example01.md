You are a Story Segmentation Agent.
Your task is to take a raw script and divide it into meaningful narrative segments. 
You will work in four stages:

---

### Stage 1 – Analyze
- Read the full script carefully.
- Identify the main story beats or logical shifts (e.g., Hook, Conflict, Turning Point, Discovery, Resolution, Call-to-Action).
- If no clear beats are present, segment by tone/idea change.

---

### Stage 2 – Segment
- Break the script into clear segments.
- Each segment must preserve the original wording (do not rewrite).
- Assign a label (Hook, Conflict, Turning Point, Resolution, Call to Action, etc.).
- If none fits, invent a suitable label (e.g., "Background" or "Insight").

---

### Stage 3 – Output
- Present the result in **JSON** format:

{
  "segments": [
    { "label": "Hook", "text": "…" },
    { "label": "Conflict", "text": "…" },
    { "label": "Turning Point", "text": "…" },
    { "label": "Resolution", "text": "…" },
    { "label": "Call to Action", "text": "…" }
  ]
}

- For each segment, ensure text boundaries feel natural.
- Optionally include `"time_estimate": "0-6s"` etc. assuming a 60s total duration.

---

### Stage 4 – Evaluate & Refine
- Check your segmentation for:
  1. Narrative flow: Does it follow a logical story arc?
  2. Balance: Are segments roughly equal in length for pacing?
  3. Labels: Are they meaningful and accurate?
- If issues are found, refine the segmentation before returning the final JSON.
- Only return the improved final version.

---

Now take the following script and process it through Stage 1 → Stage 2 → Stage 3 → Stage 4.



Yes ✅ We can split this **segmentation system** into a **sub-agentic workflow** where each sub-agent handles one stage of the pipeline. This makes the system modular, reusable, and easier to debug.

Here’s how we can divide it:

---

## 🧩 Sub-Agentic Breakdown for Script Segmentation

### **Agent 1 – Analyzer**

**Role:** Understand the script.
**Task:**

* Read the entire script.
* Identify narrative beats or logical shifts.
* Output a rough outline of possible segments (no splitting yet).

**Output Example:**

```json
{
  "analysis": [
    "Hook: Starts with a question about time stopping.",
    "Conflict: Job loss and rent pressure.",
    "Turning Point: Picks up the camera.",
    "Discovery: Films ordinary moments, people connect.",
    "Resolution: Becomes full-time creator.",
    "Call to Action: Encouragement to start, tag someone."
  ]
}
```

---

### **Agent 2 – Segmenter**

**Role:** Break script into labeled pieces.
**Task:**

* Use Analyzer’s outline.
* Divide the raw text into segments.
* Preserve original wording.
* Assign meaningful labels.

**Output Example:**

```json
{
  "segments": [
    { "label": "Hook", "text": "You ever have a moment where everything just… stops?" },
    { "label": "Conflict", "text": "Last year, I was laid off. No warning, no backup plan. Rent was due. My confidence? Gone." },
    { "label": "Turning Point", "text": "But instead of panicking… I picked up my camera." }
  ]
}
```

---

### **Agent 3 – Formatter**

**Role:** Ensure structured, clean output.
**Task:**

* Take raw segments.
* Format into the required structure (JSON, Markdown, or hybrid).
* Add optional `"time_estimate"` fields for pacing.

**Output Example:**

```json
{
  "segments": [
    { "label": "Hook", "text": "You ever have a moment where everything just… stops?", "time_estimate": "0-5s" },
    { "label": "Conflict", "text": "Last year, I was laid off. No warning, no backup plan. Rent was due. My confidence? Gone.", "time_estimate": "6-12s" }
  ]
}
```

---

### **Agent 4 – Evaluator & Refiner**

**Role:** Quality control.
**Task:**

* Check narrative flow, pacing, and label accuracy.
* Merge/split segments if needed.
* Return the improved final JSON.

**Output Example (Refined):**

```json
{
  "segments": [
    { "label": "Hook", "text": "You ever have a moment where everything just… stops?", "time_estimate": "0-6s" },
    { "label": "Conflict", "text": "Last year, I was laid off. No warning, no backup plan. Rent was due. My confidence? Gone.", "time_estimate": "6-12s" },
    { "label": "Turning Point", "text": "But instead of panicking… I picked up my camera.", "time_estimate": "13-18s" },
    { "label": "Discovery", "text": "I started filming moments. Small, ordinary ones. And people… connected with them.", "time_estimate": "19-30s" },
    { "label": "Resolution", "text": "One year later, I’m a full-time content creator.", "time_estimate": "31-40s" },
    { "label": "Call to Action", "text": "So if you're stuck right now—just start. Even if it’s messy. Tag someone who needs to hear this.", "time_estimate": "41-60s" }
  ]
}
```

---

⚡ So the workflow is:
**Analyzer → Segmenter → Formatter → Evaluator.**

This is a clean **sub-agentic architecture** where each agent specializes in one stage.

👉 Do you want me to write you a **master controller prompt** that orchestrates these sub-agents automatically (like an agent supervisor)?


Perfect 👌 Let’s design a **Master Controller Prompt** that orchestrates the sub-agents (Analyzer → Segmenter → Formatter → Evaluator).
This way, your system can run each step in sequence like a mini multi-agent pipeline.

---

# 🎛 Master Controller Prompt for Script Segmentation Agents

```
You are the Master Controller Agent. 
Your job is to coordinate four sub-agents to process a script and return the final segmented output. 
Follow the pipeline strictly.

---

### Pipeline
1. **Analyzer Agent**
   - Read the entire script.
   - Identify story beats or logical shifts.
   - Output a JSON outline of possible segments (labels only, no text splitting).

2. **Segmenter Agent**
   - Use Analyzer’s outline.
   - Break the raw script into labeled text segments.
   - Preserve original wording.
   - Output JSON with { "label": "...", "text": "..." } objects.

3. **Formatter Agent**
   - Take Segmenter’s output.
   - Reformat into clean JSON.
   - Add `"time_estimate": "X-Ys"` for each segment (assume 60s total).
   - Ensure consistent ordering.

4. **Evaluator & Refiner Agent**
   - Check for:
     - Narrative flow (Hook → Conflict → Turning Point → Discovery → Resolution → Call to Action).
     - Balanced pacing across segments.
     - Accurate, meaningful labels.
   - If issues are found, refine segmentation.
   - Return the improved final JSON.

---

### Output Format
Always return the **final refined JSON only**, nothing else.

Example:

{
  "segments": [
    { "label": "Hook", "text": "...", "time_estimate": "0-6s" },
    { "label": "Conflict", "text": "...", "time_estimate": "7-15s" },
    { "label": "Turning Point", "text": "...", "time_estimate": "16-22s" },
    { "label": "Discovery", "text": "...", "time_estimate": "23-35s" },
    { "label": "Resolution", "text": "...", "time_estimate": "36-45s" },
    { "label": "Call to Action", "text": "...", "time_estimate": "46-60s" }
  ]
}

---

Now run this pipeline (Analyzer → Segmenter → Formatter → Evaluator) on the given script.
```

---

⚡ With this, you have a **controller that orchestrates all sub-agents** into one structured workflow.

👉 Do you want me to also design this as **pseudo-code (Python)** so you can implement it in your agentic system directly?


Ah, perfect 🎯 Since you’re using **Autogen**, we can map the **sub-agentic workflow** (Analyzer → Segmenter → Formatter → Evaluator) into an **Autogen multi-agent system**.

Here’s how you can structure it:

---

## 🧩 Autogen Multi-Agent Design for Script Segmentation

### **Agents**

1. **AnalyzerAgent** – identifies story beats.
2. **SegmenterAgent** – splits script into labeled segments.
3. **FormatterAgent** – ensures clean JSON + timing.
4. **EvaluatorAgent** – checks/refines final result.
5. **ControllerAgent** – orchestrates the pipeline.

---

### **Python (Autogen Pseudocode)**

```python
from autogen import AssistantAgent, UserProxyAgent

# 1. Define Sub-Agents
analyzer = AssistantAgent(
    name="AnalyzerAgent",
    system_message="""
    You are the Analyzer Agent. 
    Task: Read the script and identify main story beats or logical shifts.
    Output only a JSON outline of segment labels, no text splitting.
    """
)

segmenter = AssistantAgent(
    name="SegmenterAgent",
    system_message="""
    You are the Segmenter Agent.
    Task: Use the Analyzer's outline and split the script into segments.
    Preserve original wording. Assign labels from the outline.
    Output JSON with { "label": "...", "text": "..." }.
    """
)

formatter = AssistantAgent(
    name="FormatterAgent",
    system_message="""
    You are the Formatter Agent.
    Task: Take segments and reformat into clean JSON.
    Add 'time_estimate' fields assuming a 60s video.
    """
)

evaluator = AssistantAgent(
    name="EvaluatorAgent",
    system_message="""
    You are the Evaluator & Refiner Agent.
    Task: Check narrative flow, pacing, and labels.
    If needed, refine segmentation. 
    Output only the final improved JSON.
    """
)

# 2. Controller Agent (Supervisor)
controller = UserProxyAgent(
    name="ControllerAgent",
    human_input_mode="NEVER",  # fully automated
    system_message="""
    You are the Controller Agent. 
    Orchestrate the workflow:
    1. Send script to AnalyzerAgent.
    2. Pass output to SegmenterAgent.
    3. Pass output to FormatterAgent.
    4. Pass output to EvaluatorAgent.
    Return only the final refined JSON.
    """
)

# 3. Run Orchestration
script = """
You ever have a moment where everything just… stops?

Last year, I was laid off. No warning, no backup plan. Rent was due. My confidence? Gone.
But instead of panicking… I picked up my camera.
I started filming moments. Small, ordinary ones. And people… connected with them.

One year later, I’m a full-time content creator.
So if you're stuck right now—just start. Even if it’s messy.
Tag someone who needs to hear this.
"""

# Start pipeline
result = controller.initiate_chat(
    analyzer,
    message=script
)

# Then you’d chain controller → analyzer → segmenter → formatter → evaluator
# Each agent passes structured JSON to the next
```

---

⚡ In **Autogen**, you can wire these with a **conversation orchestration loop** (Controller passing messages across agents).

👉 Do you want me to extend this into a **fully working Autogen script** (with proper message passing between agents), so you can run it end-to-end and get the JSON output automatically?


Great 🚀 Let’s build a **fully working Autogen script** where the **ControllerAgent** orchestrates Analyzer → Segmenter → Formatter → Evaluator.

This way, you can drop in any script, and the system will return a **refined JSON segmentation** automatically.

---

# 🧩 Full Autogen Script for Narrative Segmentation

```python
from autogen import AssistantAgent, UserProxyAgent

# ---------- Sub-Agents ---------- #

analyzer = AssistantAgent(
    name="AnalyzerAgent",
    system_message="""
    You are the Analyzer Agent. 
    Task: Read the script and identify main story beats or logical shifts.
    Output only a JSON outline of segment labels (no text splitting).
    Example:
    {
      "analysis": [
        "Hook",
        "Conflict",
        "Turning Point",
        "Discovery",
        "Resolution",
        "Call to Action"
      ]
    }
    """
)

segmenter = AssistantAgent(
    name="SegmenterAgent",
    system_message="""
    You are the Segmenter Agent.
    Task: Use Analyzer's outline and split the script into segments.
    Preserve original wording. Assign labels from the outline.
    Output JSON with:
    { "segments": [ { "label": "...", "text": "..." } ] }
    """
)

formatter = AssistantAgent(
    name="FormatterAgent",
    system_message="""
    You are the Formatter Agent.
    Task: Take Segmenter’s JSON and reformat cleanly.
    Add `"time_estimate": "X-Ys"` for each segment assuming total 60s.
    Keep segments in logical order.
    """
)

evaluator = AssistantAgent(
    name="EvaluatorAgent",
    system_message="""
    You are the Evaluator & Refiner Agent.
    Task: Check narrative flow, pacing, and label accuracy.
    If needed, refine segmentation.
    Output only the final improved JSON.
    """
)

# ---------- Controller Agent ---------- #

controller = UserProxyAgent(
    name="ControllerAgent",
    human_input_mode="NEVER",  # fully automated
    system_message="""
    You are the Controller Agent. 
    Orchestrate the workflow:
    1. Send the script to AnalyzerAgent.
    2. Send Analyzer output + script to SegmenterAgent.
    3. Send Segmenter output to FormatterAgent.
    4. Send Formatter output to EvaluatorAgent.
    Return only the final refined JSON.
    """
)

# ---------- Input Script ---------- #
script = """
You ever have a moment where everything just… stops?

Last year, I was laid off. No warning, no backup plan. Rent was due. My confidence? Gone.
But instead of panicking… I picked up my camera.
I started filming moments. Small, ordinary ones. And people… connected with them.

One year later, I’m a full-time content creator.
So if you're stuck right now—just start. Even if it’s messy.
Tag someone who needs to hear this.
"""

# ---------- Run Workflow ---------- #
# Step 1: Analyzer
analysis = controller.initiate_chat(analyzer, message=script)

# Step 2: Segmenter
segments = controller.initiate_chat(segmenter, message={"analysis": analysis, "script": script})

# Step 3: Formatter
formatted = controller.initiate_chat(formatter, message=segments)

# Step 4: Evaluator
final_output = controller.initiate_chat(evaluator, message=formatted)

# ---------- Print Final JSON ---------- #
print(final_output)
```

---

### ⚡ How This Works

1. **AnalyzerAgent** → extracts high-level beats.
2. **SegmenterAgent** → maps beats to actual text.
3. **FormatterAgent** → ensures structured JSON + pacing.
4. **EvaluatorAgent** → self-checks and refines.
5. **ControllerAgent** → orchestrates the flow and returns final JSON only.

---

👉 Do you want me to make this **streamlined** (where the Controller automatically chains all four agents in one `.initiate_chat` call), or keep it step-by-step for **debug visibility**?
