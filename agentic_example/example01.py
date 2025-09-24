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
