from __future__ import annotations
from autogen_agentchat.agents import AssistantAgent
import copy
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
import asyncio
import json
from pathlib import Path
from typing import Any
from typing import List
from pydantic import BaseModel


class Segment(BaseModel):
    id: int
    text: str
    start: float
    end: float
    duration: float
    image_suggestion: List[str]


class Model(BaseModel):
    segments: List[Segment]


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

    # Create the assistant agent with updated blueprint strategy
    keyword_agent = AssistantAgent(
        name="KeywordAgent",
        system_message="""
        You are an AI that extracts descriptive IMAGE SEARCH suggestions for transcript segments using a strategic blueprint approach.

        RULES FOR IMAGE SUGGESTIONS:
        - Always consider the full story context (all segments together)
        - For each segment, return 5 IMAGE SEARCH suggestions
        - Each phrase should describe a visual scene, object, or action as if tagging an image
        - Use adjectives + nouns (e.g., "snow-covered mountain peak", "lone hiker with backpack")
        - Avoid abstract words like "hope", "dream", "fear" - show don't tell
        - Maintain consistency of the story (character, setting, progression)

        BLUEPRINT STRATEGY:
        For each segment, analyze:
        1. NARRATIVE MOMENT: What is happening emotionally and physically?
        2. CORE CONCEPT: The main subject (e.g., "mountain climbing", "hiking")
        3. VISUAL CUES: Specific adjectives + nouns that create searchable imagery

        SEARCH QUERY PRINCIPLES:
        - Start with core concept, then add descriptive layers
        - Think like a photographer naming their image
        - Use 2-4 word phrases maximum
        - Focus on concrete, visual elements
        - Consider composition (close-ups for emotion, wide shots for setting)

        OUTPUT FORMAT: Strictly valid JSON:
        {
          "segments": [
            {
              "id": <segment_id>,
              "text": <segment_text>,
              "start": <segment_start>,
              "end": <segment_end>,
              "duration": <segment_duration>,
              "image_suggestion": ["phrase1", "phrase2", "phrase3", "phrase4", "phrase5"]
            }
          ]
        }

        EXAMPLE THINKING PROCESS:
        For "Doubt crept in.":
        - Narrative: Emotional low point, fatigue
        - Core: Hiker struggling
        - Visual: tired expression, slumped posture, looking down
        - Suggestions: ["tired hiker sitting", "exhausted climber resting", "hiker head in hands", "weary adventurer pausing", "discouraged backpacker on trail"]
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
        "text": "Alex had always dreamed of reaching the top of Eagle's Peak, a mountain so tall many said it can't be climbed without years of training. But Alex wasn't an expert. Just a person with a dream and a backpack full of hope. The first steps were easy. The path was clear. But soon the trail grew steeper. Rocks blocked the way. The wind howled. Doubt crept in.",
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

    # Prepare the task prompt with clear context
    task_prompt = f"""
    ANALYZE this story and generate image search suggestions for each segment using the blueprint strategy.

    FULL STORY: "{transcript['text']}"

    Generate 5 specific, visual, search-friendly image suggestions for each segment. Focus on:
    - Concrete visual elements (not abstract concepts)
    - Composition appropriate for the narrative moment
    - Consistency with the overall story arc
    - Search-friendly adjective+noun combinations

    Process the following segments:
    {json.dumps(enriched_transcript['segments'], indent=2)}
    """

    # Get response from the agent
    response = await Console(keyword_agent.run_stream(task=task_prompt))
    
    print("Response: ", response.messages[-1])
    
    # Display the response in console
 

    # If you want to parse and use the response programmatically:
    try:
        # Extract the content from the response (adjust based on actual response structure)
        # response_content = response.content if hasattr(response, 'content') else str(response)
        
        # Parse JSON output from assistant
        response_content = response.messages[-1].to_text()
        enriched_data = json.loads(response_content)
        
        # Merge the image suggestions back into the original transcript structure
        segment_map = {s["id"]: s for s in enriched_data["segments"]}
        for seg in enriched_transcript["segments"]:
            if seg["id"] in segment_map:
                seg["image_suggestion"] = segment_map[seg["id"]]["image_suggestion"]
                
        # Print the final enriched transcript
        print("\n" + "="*50)
        print("FINAL ENRICHED TRANSCRIPT:")
        print("="*50)
        path = Path('output.json')
        with path.open("w", encoding="utf-8") as f:
            json.dump(enriched_transcript, f, ensure_ascii=False, indent=2)
        # print(json.dumps(enriched_transcript, indent=2))
        
    except json.JSONDecodeError as e:
        print("Error parsing JSON response:", e)
    #     print("Raw response:", response_content)
    except Exception as e:
        print("Error processing response:", e)
    #     print("Raw response:", response_content)


if __name__ == "__main__":
    asyncio.run(main())