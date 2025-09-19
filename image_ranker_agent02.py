from __future__ import annotations
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
import asyncio
import json
from typing import List
from pydantic import BaseModel


class RankedImage(BaseModel):
    url: str
    score: float


class ImageSuggestion(BaseModel):
    image_keyword: str
    ranked_images: List[RankedImage]


async def main():
    # setup model client
    client = OpenAIChatCompletionClient(
        model="gemma-3-1b-it-GGUF",
        base_url="http://localhost:8080/v1",
        api_key="placeholder",
        response_format=ImageSuggestion,
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "family": "",
            "structured_output": True,
        },
    )
    
    # call the assistant agent
    image_ranker = AssistantAgent(
        name="image_ranker",
        model_client=client,
        model_client_stream=True,
        reflect_on_tool_use=True,
        system_message=(
            "You are an image relevance ranking agent.\n"
            "Your job is to analyze a keyword and a list of image metadata, "
            "and return the best-matching images.\n\n"
            "STRICT RULES:\n"
            "1. IGNORE AI-generated, non-human, and irrelevant images unless the keyword explicitly asks for them.\n"
            "2. Focus on: subject (man, woman, person, object), expression (sad, doubt, happy, confused), and framing (close-up, portrait, face).\n"
            "3. You MUST return EXACTLY 3 images - no more, no less.\n"
            "4. Assign each image a score between 1.0 (lowest) and 10.0 (highest).\n"
            "5. Scores must be distinct and reflect true relevance ranking.\n"
            "6. Output MUST be valid JSON in this exact format:\n"
            "{\n"
            '  "image_keyword": "exact keyword string",\n'
            '  "ranked_images": [\n'
            '    {"url": "EXACT_ORIGINAL_URL_1", "score": 9.5},\n'
            '    {"url": "EXACT_ORIGINAL_URL_2", "score": 8.2},\n'
            '    {"url": "EXACT_ORIGINAL_URL_3", "score": 7.1}\n'
            "  ]\n"
            "}\n"
            "7. CRITICAL: Return the EXACT URL strings as provided in the input. DO NOT modify, shorten, or change URLs in any way.\n"
            "8. If you cannot find 3 suitable images, prioritize the most relevant ones anyway.\n"
            "9. NEVER include images that don't match the keyword requirements.\n"
        ),
    )
    
    # this is a input as keyword
    keyword = "close-up of Alex's face showing doubt"

    # sample image metadata as input
    images = [
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2015/08/31/10/07/man-915230_1280.jpg",
            "name": "Free Man Sad photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2022/01/18/15/40/vietnam-6947342_1280.jpg",
            "name": "Free Vietnam Asian Woman photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2015/09/05/08/06/flashlight-924099_1280.jpg",
            "name": "Free Flashlight Dark photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2017/08/28/11/19/food-2689205_1280.jpg",
            "name": "Free Food Breakfast photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2019/03/15/18/54/fantasy-4057707_1280.jpg",
            "name": "Free Fantasy Sad photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2016/03/27/16/22/light-1283000_1280.jpg",
            "name": "Free Light Woman photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2016/11/22/19/09/abandoned-1850087_1280.jpg",
            "name": "Free Abandoned Alley photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2016/12/17/22/04/childrens-eyes-1914519_1280.jpg",
            "name": "Free Children&apos;S Eyes Eyes photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2024/02/05/02/53/cat-8553498_1280.jpg",
            "name": "Free Cat Woman illustration and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2017/09/01/20/55/girl-2705518_1280.jpg",
            "name": "Free Girl Black And White photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2019/07/31/01/44/hanamaki-4374136_1280.jpg",
            "name": "Free Hanamaki Steamed Bun photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2018/05/22/17/48/sad-3422002_1280.jpg",
            "name": "Free Sad Mood photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2023/09/11/16/37/angel-8247278_1280.jpg",
            "name": "Free Angel Sorrow photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2015/02/02/18/10/light-621211_1280.png",
            "name": "Free Light Word illustration and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2021/05/02/10/54/xiao-long-bao-6223162_1280.jpg",
            "name": "Free Xiao Long Bao Dim Sum photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2021/09/09/12/26/salvador-dali-mask-6610444_1280.jpg",
            "name": "Free Salvador Dalí Mask Red Jumpsuit photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2017/08/07/17/43/low-light-2606154_1280.jpg",
            "name": "Free Low Light People photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2021/11/10/18/00/map-6784496_1280.jpg",
            "name": "Free Map Geography photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2017/08/10/03/47/guy-2617866_1280.jpg",
            "name": "Free Guy Man photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2018/08/22/13/47/lobby-3623669_1280.jpg",
            "name": "Free Lobby Lounge photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2015/08/25/05/34/dim-sum-906211_1280.jpg",
            "name": "Free Dim Sum Hargao photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2012/02/17/15/26/light-14568_1280.jpg",
            "name": "Free Light Dim photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2020/11/06/15/33/woman-5718089_1280.jpg",
            "name": "Free Woman Mysterious photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2017/11/19/07/30/girl-2961959_1280.jpg",
            "name": "Free Girl Sad photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2021/12/29/22/21/dim-sum-6902894_1280.jpg",
            "name": "Free Dim Sum Steamed Bun photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2020/02/13/15/24/sad-4846019_1280.jpg",
            "name": "Free Sad Sky photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2024/04/22/17/19/ai-generated-8713139_1280.jpg",
            "name": "Free Ai Generated Dim Sum illustration and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2017/12/10/17/00/robot-3010309_1280.jpg",
            "name": "Free Robot Woman photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2020/12/15/14/20/old-woman-5833786_1280.jpg",
            "name": "Free Old Woman Portrait photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2025/05/27/03/35/ai-generated-9624442_1280.png",
            "name": "Free Ai Generated Crown illustration and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2022/11/04/10/55/woman-7569551_1280.jpg",
            "name": "Free Woman Cave illustration and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2023/05/21/03/49/child-8007770_1280.jpg",
            "name": "Free Child Nature illustration and picture",
        },
    ]
    
    # Create input prompt with explicit URL preservation instructions
    input_prompt = f"""
    KEYWORD: "{keyword}"
    
    IMAGE DATASET:
    {json.dumps(images, indent=2)}
    
    CRITICAL INSTRUCTIONS:
    1. Select EXACTLY 3 most relevant images for the keyword
    2. Return the EXACT URL strings as provided - DO NOT modify URLs in any way
    3. URLs must match exactly what's in the input dataset
    4. Rank from most relevant (highest score) to least relevant (lowest score)
    5. Output must be valid JSON in the specified format
    
    REQUIRED OUTPUT FORMAT:
    {{
      "image_keyword": "{keyword}",
      "ranked_images": [
        {{"url": "EXACT_ORIGINAL_URL_HERE", "score": 9.5}},
        {{"url": "EXACT_ORIGINAL_URL_HERE", "score": 8.2}},
        {{"url": "EXACT_ORIGINAL_URL_HERE", "score": 7.1}}
      ]
    }}
    """

    print("Sending prompt to image ranker...")
    print(f"Keyword: {keyword}")
    print(f"Total images: {len(images)}")

    # Get response
    response = await Console(image_ranker.run_stream(task=input_prompt))

    # Display results
    print("\n" + "="*60)
    print("IMAGE RANKING RESULTS:")
    print("="*60)
    
    if response.messages:
        last_message = response.messages[-1].to_text()
        print("Raw response:", last_message)
        
        # Simple display of results
        try:
            if hasattr(last_message, 'content') and last_message.content:
                content = last_message.content
                if isinstance(content, dict):
                    # Handle structured response
                    result = ImageSuggestion(**content)
                    print(f"Keyword: {result.image_keyword}")
                    print("Top 3 Images:")
                    for i, img in enumerate(result.ranked_images, 1):
                        print(f"{i}. Score: {img.score:.1f}")
                        print(f"   URL: {img.url}")
                        print()
                else:
                    # Handle text response
                    print("Response content:", content)
        except Exception as e:
            print(f"Error parsing response: {e}")
            print("Raw response content:", last_message)
    else:
        print("No response received")


asyncio.run(main())