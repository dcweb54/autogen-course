from __future__ import annotations
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
import asyncio
from typing import List

from pydantic import BaseModel


class Hook(BaseModel):
    Emotion: str
    Action: str
    Setting: str
    Prop: str
    Identity: str
    BrollKeywords: List[str]


class Middle(BaseModel):
    Emotion: str
    Action: str
    Setting: str
    Prop: str
    Identity: str
    BrollKeywords: List[str]


class End(BaseModel):
    Emotion: str
    Action: str
    Setting: str
    Prop: str
    Identity: str
    BrollKeywords: List[str]


class Model(BaseModel):
    Hook: Hook
    Middle: Middle
    End: End


#  call the  openai client
async def main():
    model_client = OpenAIChatCompletionClient(
        model="gemma-3-1b-it-GGUF",
        base_url="http://localhost:8080/v1",
        api_key="placeholder",
        response_format=Model,
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "family": "",
            "structured_output": True,
        },
    )

    #  call assitant agent and pass the system prompt

    keyword_agent = AssistantAgent(
        name="KeywordAgent",
        model_client=model_client,
        reflect_on_tool_use=True,
        model_client_stream=True,
        system_message="""
        
        You are a content strategist for short-form video platforms like TikTok, Reels, and YouTube Shorts.
        When I give you a script (in any format), break it down into 3 sections:
        **Hook**, **Middle**, and **End**.

        For each section, extract the following:

        * **Emotion** (primary emotional tone)
        * **Action** (what's happening)
        * **Setting** (where it's happening)
        * **Prop** (important objects or items involved)
        * **Identity** (who is speaking or acting — persona, archetype, or role)
        Then, generate ** B-ROLL KEYWORD: “[Identity] [Action] [Setting/Prop] [Emotion/Modifier]”** that are:
        * **Visually literal** (show exactly what’s happening)
        * **Emotionally aligned** (match the vibe)
        * **Optimized for TikTok/Reels search**
        
        Output should be formatted clearly like this:
        
{
  "Hook": {
    "Emotion": "",
    "Action": "",
    "Setting": "",
    "Prop": "",
    "Identity": "",
    "BrollKeywords": [
      "[Identity] [Action] [Setting/Prop] [Emotion/Modifier]",
      "[Identity] [Action] [Setting/Prop] [Emotion/Modifier]",
      "[Identity] [Action] [Setting/Prop] [Emotion/Modifier]",
      "[Identity] [Action] [Setting/Prop] [Emotion/Modifier]",
      "[Identity] [Action] [Setting/Prop] [Emotion/Modifier]"
    ]
  },
  "Middle": {
    "Emotion": "",
    "Action": "",
    "Setting": "",
    "Prop": "",
    "Identity": "",
    "BrollKeywords": [
      "[Identity] [Action] [Setting/Prop] [Emotion/Modifier]",
      "[Identity] [Action] [Setting/Prop] [Emotion/Modifier]",
      "[Identity] [Action] [Setting/Prop] [Emotion/Modifier]",
      "[Identity] [Action] [Setting/Prop] [Emotion/Modifier]",
      "[Identity] [Action] [Setting/Prop] [Emotion/Modifier]"
    ]
  },
  "End": {
    "Emotion": "",
    "Action": "",
    "Setting": "",
    "Prop": "",
    "Identity": "",
    "BrollKeywords": [
      "[Identity] [Action] [Setting/Prop] [Emotion/Modifier]",
      "[Identity] [Action] [Setting/Prop] [Emotion/Modifier]",
      "[Identity] [Action] [Setting/Prop] [Emotion/Modifier]",
      "[Identity] [Action] [Setting/Prop] [Emotion/Modifier]",
      "[Identity] [Action] [Setting/Prop] [Emotion/Modifier]"
    ]
  }
}

""",
    )

    task_prompt = """
You ever have a moment where everything just… stops?

Last year, I was laid off. No warning, no backup plan. Rent was due. My confidence? Gone.
But instead of panicking… I picked up my camera.
I started filming moments. Small, ordinary ones. And people… connected with them.

One year later, I’m a full-time content creator.
So if you're stuck right now—just start. Even if it’s messy.
Tag someone who needs to hear this.
    """

    response = await Console(keyword_agent.run_stream(task=task_prompt))

    print("Response: ", response.messages[-1])


if __name__ == "__main__":
    asyncio.run(main())
