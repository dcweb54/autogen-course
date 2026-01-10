from __future__ import annotations
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.ui import Console
from datetime import datetime
from pathlib import Path
import os
import json
from pydantic import BaseModel, Field


class TimelineItem(BaseModel):
    idx: int
    line: str
    emotions: list[str]
    actions: list[str]
    settings: list[str]
    objects_props: list[str] = Field(..., alias="objects/props")
    identity_cues: list[str] = Field(..., alias="identity cues")
    clip_query: str
    overlay_text: str


class Model(BaseModel):
    timeline: list[TimelineItem]


def get_mode_client():
    return OllamaChatCompletionClient(
        model="qwen2.5vl:3b",
        host="https://hyjyz6ojgd1a.share.zrok.io",
        # response_format=Model,
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "family": "",
            "structured_output": True,
        },
    )


def llama_model_client():
    return OpenAIChatCompletionClient(
        model="gemma-3-1b-it-GGUF",
        base_url="http://localhost:8080/v1",
        api_key="placeholder",
        # response_format=Model,
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "family": "",
            "structured_output": True,
        },
    )


def get_script():
    script_output_path = os.path.join(os.getcwd(), "script_generator", "output-02.txt")

    with open(script_output_path, "r") as f:
        load_script = f.read()

    return load_script


def get_visual_prompt(script: str):
    prompt = f"""
    You are a Visual Planner AI.
        Input: {script}
        Output JSON with: idx, text, duration, emotions, actions, settings, objects, identity_cues, clip_query, overlay_text.
        Ensure visuals are context-aware: clip_query should represent **what should appear visually**, not just random stock clips.
    """
    return prompt


def get_visual_promptv2(script_lines: str):
    return f"""You are a Visual Planner for motivational videos. For each script line below, generate a context-aware visual description in strict JSON format.
        Rules:
        - Output ONLY a JSON object with key "timeline", value = list of entries.
        - Each entry must have: idx (int), text (str), duration (float), emotions (list[str]), actions (list[str]), settings (list[str]), objects (list[str]), identity_cues (list[str]), clip_query (str), overlay_text (str).
        - Emotions: e.g., ["hope", "frustration", "empowerment"]
        - Actions: physical or expressive actions, e.g., ["walking forward", "sitting with head in hands"]
        - Settings: real-world locations, e.g., ["park", "home office"]
        - Objects: visible props, e.g., ["laptop", "journal"]
        - Identity cues: demographic/relatable traits, e.g., ["young adult", "woman of color"]
        - clip_query: natural-language, searchable phrase combining key elements (max 15 words)
        - overlay_text: 2–4 word phrase summarizing core message (concise, bold, readable)

        Script lines:
        {script_lines}

        Output JSON:
"""


def get_visual_promptv3(script_lines: str):
    return f"""You are a Visual Planner for high-impact motivational videos. Your job is to turn each abstract script line into **concrete, searchable visual directions** that match the emotion, pacing, and message.

        For every line, output a structured entry with these EXACT fields:
        - **idx**:<idx>
        - **line**:<script line>
        - **emotions**: 1–3 core feelings (e.g., "anxiety", "hope", "shock", "empowerment")
        - **actions**: specific physical behaviors (e.g., "packing desk", "scrolling phone", "filming selfie", "editing on laptop")
        - **settings**: real-world locations (e.g., "apartment", "office", "coffee shop", "park at sunset")
        - **objects/props**: visible, tangible items that reinforce context (e.g., "camera", "rent bill", "journal", "laptop")
        - **identity cues**: relatable human descriptors (e.g., "young adult", "woman of color", "freelancer", "college student")
        - **clip_query**: a single, natural-language phrase (max 15 words) combining the above for stock/AI video search
        - **overlay_text**: 2–4 bold, readable words that capture the core message (e.g., "One step", "Use your mind")

        > 🎯 Goal: Turn abstract feelings into *searchable, concrete footage*.

        Script lines:
        {script_lines}

        Output ONLY a valid JSON object with a "timeline" key containing a list of entries.
        Do NOT add explanations, markdown, or extra fields.
        """


def get_b_roll_footage(script_lines: str):
    return f"""
            You are a professional visual storyteller and video director.
            I will provide a list of script lines with line numbers.
            For each line, generate a concise B-roll brief in this exact format:

            Line [idx]: "[text]"

            Emotion: [1–3 words]
            Metaphor: [symbolic visual concept]
            B-roll Shots:
            • [Shot 1: concrete, filmable, emotionally resonant]
            • [Shot 2]
            • [Shot 3]
            Guidelines:

            Focus on universal, intimate visuals: hands, nature, light, textures, everyday objects.
            Avoid clichés (e.g., lightbulbs, handshakes, mirrors with affirmations).
            Prioritize shots that work in close-up or medium framing (easy to film or source as stock).
            Match the emotional arc: start heavy/cool → transition to warm/hopeful.
            Keep language practical and shootable (e.g., “hands smoothing crumpled paper,” not “visualize inner turmoil”).
            Here is my script
            {script_lines}
            """


def get_b_roll_suggestion(script_lines: str):
    return f"""
        You are the **B-roll Keyword Agent**.
        You will process a JSON input containing narrative script segments in the form:

        {{
        "lines": [
            {{"idx": <number>, "text": "<script line>"}},
            ...
        ]
        }}

        ---

        ## 🔹 STEP 2: EXTRACT KEY ELEMENTS PER BEAT
        For each `"line"`, identify:
        - **Emotions** (e.g., shock, hope, anxiety, empowerment)
        - **Actions** (e.g., packing desk, filming, editing, scrolling phone)
        - **Settings** (e.g., apartment, office, coffee shop, park)
        - **Objects/Props** (e.g., camera, laptop, rent bill, journal)
        - **Identity Cues** (e.g., young adult, woman of color, freelancer)

        ---

        ## 🔹 STEP 3: TRANSLATE INTO “FOOTAGE SEARCH LANGUAGE”
        For each line, create **B-roll search keywords** using this formula:

        > **[Identity] + [Action] + [Setting/Emotion/Prop]**

        Guidelines:
        - Keywords must be **visually specific** (e.g., “person packing office desk shocked expression”).
        - Avoid vague terms like “inspiring” or “emotional”.
        - Use multiple keyword variations when possible.

        ---

        ## 🔹 OUTPUT FORMAT
        Return results as a JSON-like array with the following schema:

        [
            {{
        "idx": "<same index as input>",
                "line": "<original script line>",
                "Emotions": [],
                "Actions": [],
                "Settings": [],
                "Objects": [],
                "Identity": [],
                "Broll_Keywords": []
            }}
        ]

        ---

        ## Rules:
        1. Always preserve the original wording in `"line"`.
        2. Ensure consistency: each line from input has a matching structured output.
        3. Be descriptive but concise — focus on what can actually appear in stock footage.
        4. If a line is abstract (e.g., “[pause]” or pure emotion), still try to imagine a visual metaphor for it.

        this is a input
        {script_lines}
"""


def get_b_roll_suggestionV2(script_lines: str):
    return f"""
        **Role**: B-roll Keyword Agent
        **Task**: Convert each script line into visual B-roll search keywords.

        **Input**:
        ```json
        {{"lines": [{{"idx": N, "text": "..."}}, ...]}}
        ```

        **Per line, extract only observable elements**:
        - **Emotions** (e.g., *shock*, *anxiety*)
        - **Actions** (e.g., *packing desk*, *scrolling phone*)
        - **Settings** (e.g., *office*, *coffee shop*)
        - **Objects** (e.g., *laptop*, *rent bill*)
        - **Identity** (e.g., *young woman*, *freelancer*)

        **Generate 2–4 B-roll keywords** using:
        `[Identity] + [Action] + [Setting/Emotion/Prop]`
        → Must be **visually specific**, stock-footage friendly.
        → No vague/abstract terms (e.g., “inspiring”).

        **Output**:
        ```json
        [
        {{
        "idx": N,
            "line": "<original>",
            "Emotions": [],
            "Actions": [],
            "Settings": [],
            "Objects": [],
            "Identity": [],
            "Broll_Keywords": ["..."]
        }}
        ]
        ```

        **Rules**:
        1. Keep `"line"` verbatim.
        2. One output object per input line.
        3. If abstract (e.g., “[pause]”), infer a plausible visual (e.g., “person staring out window”).
        4. Never invent unsupported details.

        **Process this**:
        `{script_lines}`

        """


def get_image_genration_prompt(script_lines: str):
    return f"""
    You are a visual generation assistant specialized in prompt creation for Juggernaut XL image generation.

    You will be given a JSON object containing an array of script lines.
    For each item, generate a concise Juggernaut XL–ready image prompt designed for consistent black-and-white line-art illustrations.

    ### Rules
    1. Character Consistency:
       - Main character: young man, mid-20s, short hair, wearing a hoodie and jeans.
       - Maintain identical appearance, outfit, and proportions across all prompts.

    2. Style (always include these base tags):
       black and white, line art, sketch, ink drawing, clean outlines, minimal shading, simple composition.

    3. Scene Adaptation:
       - Interpret the "text" value and express its emotion or message visually.
       - Emphasize body language, posture, and facial expression.
       - Backgrounds minimal; include only symbolic or essential details.

    4. Output Format:
       Return JSON with the same "idx" and "text", but add a "prompt" field:
       [{{
        "idx": <original idx>,
         "text": "<original script line>",
         "prompt": "<Juggernaut XL-optimized prompt>"
       }}]

    ---

    Here is my script input:
    {script_lines}

        """


async def get_visual_suggestion(ollama_client: OllamaChatCompletionClient):
    agent = AssistantAgent("assistant", ollama_client)
    response = await Console(
        agent.run_stream(task=get_image_genration_prompt(script_lines=get_script()))
    )
    response_content = response.messages[-1].to_text()
    return response_content


async def main() -> None:
    current_file_path = Path(__file__)
    load_prompt_path = os.path.join(current_file_path.parent, "output-010.txt")
    # Rise Above Your Fears
    ollama_client = get_mode_client()
    result = await get_visual_suggestion(ollama_client)
    # result = json.loads(result)
    # print(result)
    with open(load_prompt_path, "w") as f:
        write_result = f.write(result)
    print(write_result)


asyncio.run(main())


# test case-01
# get_b_roll_footage [working perfer there is mirror issue with data return types]


# test-case-02
# get_b_roll_suggestion [not working perfect for anyone]
#
# test-case-03
# get_b_roll_suggestionV2 [later will compare with first one]
