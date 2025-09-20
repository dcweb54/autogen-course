from autogen_core.models import CreateResult, UserMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import asyncio


async def main():
    model_client = OpenAIChatCompletionClient(
        model="gemma-3-1b-it-GGUF",
        base_url="http://localhost:8080/v1",
        api_key="placeholder",
        model_info={
            "vision": False,
            "function_calling": False,
            "json_output": True,
            "family": "",
            "structured_output": True,
        },
    )
    sample_input = {
        "language": "en",
        "language_probability": 0.998,
        "segments": [
            {
                "id": 0,
                "text": "Doubt crept in.",
                "start": 10.5,
                "end": 13.2,
                "duration": 2.7,
            },
            {
                "id": 1,
                "text": "But I kept climbing.",
                "start": 13.5,
                "end": 16.0,
                "duration": 2.5,
            },
        ],
    }

    messages = [
        UserMessage(
            content=f"You are a visual storytelling expert. Convert each transcript segment into 5 emotionally resonant, visually authentic, Pexels-search-optimized keyword phrases. Preserve all original JSON structure. Add only image_keywords per segment. Think cinematically: lighting, emotion, symbolism, realism. Avoid clichés. Match the story’s tone precisely. this is a input {sample_input}",
            source="user",
        ),
    ]

    # Create a stream.
    stream = model_client.create_stream(messages=messages)

    # Iterate over the stream and print the responses.
    print("Streamed responses:")
    async for chunk in stream:  # type: ignore
        if isinstance(chunk, str):
            # The chunk is a string.
            print(chunk, flush=True, end="")
        else:
            # The final chunk is a CreateResult object.
            assert isinstance(chunk, CreateResult) and isinstance(chunk.content, str)
            # The last response is a CreateResult object with the complete message.
            print("\n\n------------\n")
            print("The complete response:", flush=True)
            print(chunk.content, flush=True)


asyncio.run(main())
