# pip install -U "autogen-agentchat" "autogen-ext[openai]"
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_agentchat.ui import Console
from datetime import datetime
from pathlib import Path
import os


def get_mode_client():
    return OllamaChatCompletionClient(
        model="llama3.1:latest", host="https://9kbau0ktwch8.share.zrok.io"
    )


def generate_tts_ready_script(topic: str):
    prompt = f"""
    You are a motivational scriptwriter.
    Generate a short motivational script for the topic: "{topic}"
    Format it as JSON with key "lines":
    - "idx": line number starting from 1
    - "text": TTS-ready line (use [pause] where appropriate)
    Total duration ~20 seconds.
    Output ONLY JSON.
    """
    return prompt


async def get_new_script(ollama_client: OllamaChatCompletionClient):
    agent = AssistantAgent("assistant", ollama_client)
    response = await Console(
        agent.run_stream(task=generate_tts_ready_script(topic="Overcoming self-doubt"))
    )
    response_content = response.messages[-1].to_text()
    return response_content


async def main() -> None:
    current_file_path = Path(__file__)
    load_prompt_path = os.path.join(current_file_path.parent, "output-02.txt")
    # Rise Above Your Fears
    ollama_client = get_mode_client()
    result = await get_new_script(ollama_client)

    print(result)
    with open(load_prompt_path, "w") as f:
        _ = f.write(result)


asyncio.run(main())
