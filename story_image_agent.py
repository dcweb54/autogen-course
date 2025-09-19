# story_image_agent.py
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from typing import List, Dict, Any, Optional
from autogen_agentchat.ui import Console
import json
import os


class StoryImageAgent:
    """
    A universal agent for selecting the most narratively appropriate image from a list of options.
    Handles its own configuration and model client lifecycle.
    """

    def __init__(
        self,
    ):
        """
        Initialize the Story Image Selection Agent.

        Args:
            model: The OpenAI model to use (e.g., "gpt-4o", "gpt-4-turbo")
            api_key: Your OpenAI API key. If None, will try to get from OPENAI_API_KEY env variable.
            system_message: Custom system message for the agent. Uses default if None.
        """
        # Get API key from environment if not provided

        # Initialize model client
        self.model_client = OpenAIChatCompletionClient(
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

        # Default system message
        default_system_message = """You are an expert visual storytelling assistant. Your primary function is to select the most narratively appropriate image for a specific moment in a story.

When provided with a story context, target image description, and available images, analyze them as follows:

1. DECONSTRUCT the target description into:
   - Technical components (shot type, subject: "close-up", "face", "person", etc.)
   - Emotional/thematic components ("doubt", "hope", "struggle", etc.)

2. EVALUATE each available image:
   - First, check if it matches the TECHNICAL requirements. If not, reject it.
   - If it passes technically, score it 1-100 on emotional/thematic match.

3. SELECT the image with the highest score, or return null if no suitable image exists.

4. PROVIDE a clear justification for your choice.

Return your final decision as JSON with: {"selected_image_id": <number-or-null>, "selected_image_name": "<name>", "justification": "your reasoning"}"""

        self.system_message = default_system_message

        # Initialize the assistant agent WITHOUT tools first
        self.agent = AssistantAgent(
            name="story_image_selector",
            model_client=self.model_client,
            system_message=self.system_message,
            reflect_on_tool_use=True,
            model_client_stream=True,
        )

    async def select_image(
        self,
        story_context: str,
        target_keyword: str,
        image_options: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Main method to select an image for a story moment.

        Args:
            story_context: The story text or script
            target_keyword: Description of the needed image (e.g., "close-up of face showing doubt")
            image_options: List of available images with 'id' and 'name'/'description'

        Returns:
            Dictionary with selected_image_id and justification
        """
        # Create a comprehensive prompt that includes everything
        prompt = f"""
        STORY IMAGE SELECTION TASK

        STORY CONTEXT:
        \"\"\"{story_context}\"\"\"

        TARGET IMAGE DESCRIPTION:
        \"\"\"{target_keyword}\"\"\"

        AVAILABLE IMAGE OPTIONS:
        {json.dumps(image_options, indent=2)}

        PLEASE ANALYZE AND SELECT:

        1. DECONSTRUCT the target description:
           - Technical requirements: shot type, subject, composition
           - Emotional/thematic requirements: emotion, mood, theme

        2. EVALUATE each image option:
           - Check technical compatibility first
           - Score emotionally compatible images 1-100

        3. MAKE YOUR SELECTION:
           - Choose the image with the highest emotional score that is technically compatible
           - If no images are technically compatible, select null

        4. RETURN your final decision as JSON with this exact structure:
           {{
             "selected_image_id": <number-or-null>,
             "selected_image_name": "<name-of-selected-image>",
             "justification": "Clear explanation of your choice"
           }}

        Be strict about technical requirements. An image must match the core technical aspects to be considered."""

        try:
            # Run the agent with the comprehensive prompt
            result = await Console(self.agent.run_stream(task=prompt))

            response = result.messages[-1].to_text()

            print(response)

            # The agent's response will contain the analysis and decision
            # In a real implementation, you would parse this to extract the JSON

        except Exception as e:
            return {"error": f"Agent execution failed: {str(e)}"}

    async def close(self):
        """Clean up the model client connection."""
        await self.model_client.close()


# Example usage
async def example_usage():
    """Demonstrate how to use the agent."""

    # Initialize the agent
    agent = StoryImageAgent()

    # Your data
    story_script = "Alex had always dreamed of reaching the top of Eagle's Peak, a mountain so tall many said it can't be climbed without years of training. But Alex wasn't an expert. Just a person with a dream and a backpack full of hope. The first steps were easy. The path was clear. But soon the trail grew steeper. Rocks blocked the way. The wind howled. Doubt crept in."
    target_kw = "close-up of Alex's face showing doubt"
    with open("input.json", "r", encoding="utf-8") as f:
        images = json.load(f)

    # print(images)          # Python dict
    # print(type(images['name']))    # <class 'dict'>

    selected = list(map(lambda x: {"id": x["id"], "name": x["name"]}, images))

    # images = [
    #     {"id": 13, "name": "Free Woman Sad photo and picture"},
    #     {"id": 14, "name": "Free Room Attic photo and picture"},
    #     {"id": 15, "name": "Free Light Dim photo and picture"},
    # ]

    try:
        await agent.select_image(story_script, target_kw, selected)
        # print("Selection Result:", json.dumps(result, indent=2))

    finally:
        await agent.close()


# Run if executed directly
if __name__ == "__main__":
    import asyncio

    asyncio.run(example_usage())
