from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
import copy
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
import asyncio


async def main():
    model_client = OpenAIChatCompletionClient(
        model="gemma-3-1b-it-GGUF",
        base_url="http://localhost:8080/v1",
        api_key="placeholder",
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "family": "",
            "structured_output": True,
        },
        # response_format={
        #     "type": "json_object",
        #     "schema": {
        #         "type": "object",
        #         "properties": {"capital": {"type": "string"}},
        #         "required": ["capital"],
        #     },
        # },
    )

    # Create the assistant agent
    keyword_agent = AssistantAgent(
        name="KeywordAgent",
        system_message="""
        You are an AI that extracts visual keywords from transcript segments for IMAGE SEARCH.
        Always output JSON for a single segment with id and keywords only.
        Rules:
        - Only include short, imageable keywords (nouns, adjectives, simple verbs).
        - Avoid abstract terms like 'doubt', 'success'.
        - Prioritize things a camera could capture: people, objects, places, actions, atmosphere.
        """,
        model_client=model_client,
        reflect_on_tool_use=True,
        model_client_stream=True,  # Enable streaming tokens from the model client.
    )

    # Example transcript JSON
    transcript = {
        "language": "en",
        "language_probability": 0.9995,
        "duration": 26.1,
        "text": "Alex had always dreamed ... Doubt crept in.",
        "segments": [
            {
                "id": 1,
                "text": "Alex had always dreamed of reaching the top of Eagle's Peak,",
                "start": 0.0,
                "end": 3.74,
                "duration": 3.74,
            },
            {
                "id": 2,
                "text": "a mountain so tall many said it can't be climbed without years of training.",
                "start": 3.92,
                "end": 8.6,
                "duration": 4.68,
            },
            {
                "id": 3,
                "text": "But Alex wasn't an expert.",
                "start": 9.16,
                "end": 10.88,
                "duration": 1.72,
            },
            {
                "id": 4,
                "text": "Just a person with a dream and a backpack full of hope.",
                "start": 11.5,
                "end": 15.02,
                "duration": 3.52,
            },
            {
                "id": 5,
                "text": "The first steps were easy.",
                "start": 15.64,
                "end": 17.22,
                "duration": 1.58,
            },
            {
                "id": 6,
                "text": "The path was clear.",
                "start": 17.32,
                "end": 18.52,
                "duration": 1.2,
            },
            {
                "id": 7,
                "text": "But soon the trail grew steeper.",
                "start": 19.1,
                "end": 21.3,
                "duration": 2.2,
            },
            {
                "id": 8,
                "text": "Rocks blocked the way.",
                "start": 21.68,
                "end": 22.78,
                "duration": 1.1,
            },
            {
                "id": 9,
                "text": "The wind howled.",
                "start": 23.08,
                "end": 24.38,
                "duration": 1.3,
            },
            {
                "id": 10,
                "text": "Doubt crept in.",
                "start": 25.06,
                "end": 26.1,
                "duration": 1.04,
            },
        ],
    }

    # Prompt template for each segment
    prompt_template = """
    Extract 3-6 image search keywords from the transcript segment below.
    Output JSON strictly as:
    {{
        "id": {id},
        "keywords": ["word1", "word2", "word3"]
    }}

    Transcript Segment:
    {id}: "{text}"
    """

    # Deep copy transcript so we can enrich
    enriched_transcript = copy.deepcopy(transcript)

    # Loop through segments
    for seg in enriched_transcript["segments"]:
        # prompt_template = f"""
        # Extract 3–6 image search keywords from the transcript segment below.
        # Transcript Segment:
        # "{text}"
        #  """
        # print(seg)
        filled_prompt = prompt_template.format(id=seg["id"], text=seg["text"])
        await Console(keyword_agent.run_stream(task=filled_prompt))
        # await model_client.close()


asyncio.run(main())
