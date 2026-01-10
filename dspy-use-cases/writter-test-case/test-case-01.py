# pip install -U "autogen-agentchat" "autogen-ext[openai]"
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_agentchat.ui import Console
import os
from pathlib import Path

async def main() -> None:
    current_file_path = Path(__file__)
    load_prompt_path = os.path.join(current_file_path.parent,'prompts','test-case-02.txt')
    # Rise Above Your Fears
    with open(load_prompt_path,'r') as f:
        load_prompt = f.read()
        
    print(load_prompt)
    agent = AssistantAgent("assistant", OllamaChatCompletionClient(model="llama3.1:latest",host="https://k38wbq5ylygc.share.zrok.io"))
    # print(await agent.run(task="Say 'Hello World!'"))
    response = await Console(agent.run_stream(task=load_prompt))
    response_content = response.messages[-1].to_text()
    print(f"response {response_content}")

asyncio.run(main())
