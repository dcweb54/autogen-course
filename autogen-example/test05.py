from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
import copy
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
import asyncio
import json


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
    )

    # Create the assistant agent
    keyword_agent = AssistantAgent(
        name="KeywordAgent",
        system_message="""
        You are an AI that extracts descriptive IMAGE SEARCH suggestion for transcript segments.

        Rules:
        - For each transcript segment, return IMAGE SEARCH suggestion.
        - Each phrase should describe a visual scene, object, or action.
        - Use adjectives + nouns (e.g., "snow-covered mountain peak", "hiker with backpack").
        - Avoid abstract or emotional words like "hope", "fear", "dream".
        - Output strictly valid JSON in this format:
        {
          "segments": [
            {
              "id": <segment_id>,
              "image_suggestion": []
            }
          ]
        }
        """,
        model_client=model_client,
        reflect_on_tool_use=True,
        model_client_stream=True,
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

    # Deep copy transcript to enrich
    enriched_transcript = copy.deepcopy(transcript)

    # One-shot prompt with all segments
    transcript_text = json.dumps(enriched_transcript["segments"], indent=2)
    task_prompt = f"Enrich the following transcript segments with image_keywords:\n{transcript_text}"

    response = await Console(keyword_agent.run_stream(task=task_prompt))

    # Parse JSON output from assistant
    # try:
    #     enriched_data = json.loads(response)
    #     segment_map = {s["id"]: s for s in enriched_data["segments"]}
    #     for seg in enriched_transcript["segments"]:
    #         if seg["id"] in segment_map:
    #             seg["image_keywords"] = segment_map[seg["id"]]["image_keywords"]
    # except Exception as e:
    #     print("Error parsing assistant output:", e)

    # # ✅ Final enriched transcript with image_keywords
    # print(json.dumps(enriched_transcript, indent=2))


asyncio.run(main())
