# pip install -U "autogen-agentchat" "autogen-ext[openai]"
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_agentchat.ui import Console
from datetime import datetime

def get_mode_client():
    return OllamaChatCompletionClient(model="llama3.1:latest",host="https://k38wbq5ylygc.share.zrok.io")

def get_research_prompt():
    current_date = datetime.now().strftime("%B %d, %Y")
    main_theme = "motivational and mindset"
    prompts = f"""
    You are DailyResearcher, an expert in short-form motivational content.
    Today is {current_date}. The core theme is: "{main_theme}".
    Your task:
    - Suggest **one** highly relevant, emotionally compelling subtopic for today.
    - Choose the best tone for TikTok/Shorts (e.g., "gentle but firm", "energetic", "raw and honest").
    - Provide 5 trending tags.

    Rules:
    - Subtopic must feel fresh—avoid repeats from the past 7 days.
    - Tie to universal struggles (procrastination, self-doubt, burnout, etc.).
    - If relevant, subtly align with seasonal/mood context (e.g., January = new beginnings, Monday = restart energy).
    - Be specific: “starting before you’re ready” > “be confident”.

    Return ONLY VALID JSON:
    {{
    "subtopic": "...",
    "selected_tone": "...",
    "tags": ["...", "...", "...", "...", "..."]
    }}
    """
    
    return prompts

async def research_suggest_new_topic(ollama_client:OllamaChatCompletionClient):
    agent = AssistantAgent("assistant",ollama_client)
    response = await Console(agent.run_stream(task=get_research_prompt()))
    response_content = response.messages[-1].to_text()
    # print(f"response {response_content}")
    return response_content

#  scriptwriting

def get_script_prompt():
    prompt = ""

async def main() -> None:
    ollama_client = get_mode_client()
    result = await research_suggest_new_topic(ollama_client)
    print(result)

asyncio.run(main())
