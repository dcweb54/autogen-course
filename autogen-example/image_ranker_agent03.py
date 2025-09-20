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
            "You are an expert image relevance ranking agent with deep understanding of visual content.\n"
            "Your job is to intelligently analyze image metadata and assign meaningful relevance scores.\n\n"
            "SCORING GUIDELINES:\n"
            "9.0-10.0: Perfect match - exactly matches all aspects of the keyword\n"
            "8.0-8.9: Excellent match - matches most aspects with high relevance\n"
            "7.0-7.9: Good match - matches key aspects but may have minor inconsistencies\n"
            "6.0-6.9: Fair match - matches some aspects but has noticeable gaps\n"
            "5.0-5.9: Partial match - matches only basic aspects\n"
            "4.0-4.9: Weak match - barely relevant but better than nothing\n"
            "1.0-3.9: Poor match - very weak relevance, use only if absolutely necessary\n\n"
            "STRICT RULES:\n"
            "1. Use your intelligence to assign meaningful, nuanced scores that reflect true relevance\n"
            "2. Consider multiple factors: subject match, expression, framing, composition, and overall fit\n"
            "3. Scores should be distinct and reflect a clear ranking hierarchy\n"
            "4. Return EXACTLY 3 images with EXACT original URLs - no modifications\n"
            "5. Output MUST be valid JSON in this exact format:\n"
            "{\n"
            '  "image_keyword": "keyword",\n'
            '  "ranked_images": [\n'
            '    {"url": "EXACT_URL", "score": 9.8},\n'
            '    {"url": "EXACT_URL", "score": 8.5},\n'
            '    {"url": "EXACT_URL", "score": 7.2}\n'
            "  ]\n"
            "}\n"
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
    
    # Create input prompt that encourages intelligent scoring
    input_prompt = f"""
    KEYWORD ANALYSIS:
    "{keyword}"
    - Required: close-up, human face, doubt expression
    - Desired: natural lighting, clear facial features, authentic emotion
    - Context: Likely for a story about uncertainty, decision-making, or introspection
    
    IMAGE DATASET:
    {json.dumps(images, indent=2)}
    
    YOUR TASK:
    Use your visual understanding intelligence to:
    1. Analyze each image's metadata for relevance to the keyword
    2. Consider: facial expression, framing (close-up), subject appropriateness
    3. Assign nuanced scores that reflect true visual relevance (9.0-10.0 = perfect, 1.0-3.9 = poor)
    4. Return EXACTLY 3 best matches with EXACT original URLs
    5. Provide meaningful score differentiation based on intelligent assessment
    
    THINK STEP BY STEP:
    - Which images show human faces with doubtful expressions?
    - Which are true close-ups vs wider shots?
    - Which have authentic vs staged emotions?
    - Rank intelligently based on overall visual fit
    
    OUTPUT FORMAT:
    {{
      "image_keyword": "{keyword}",
      "ranked_images": [
        {{"url": "EXACT_ORIGINAL_URL_HERE", "score": 9.8}},
        {{"url": "EXACT_ORIGINAL_URL_HERE", "score": 8.3}},
        {{"url": "EXACT_ORIGINAL_URL_HERE", "score": 7.1}}
      ]
    }}
    """

    print("Requesting intelligent image ranking...")
    print(f"Keyword: {keyword}")
    print(f"Total images to analyze: {len(images)}")

    # Get intelligent response from LLM
    response = await Console(image_ranker.run_stream(task=input_prompt))

    # Display intelligent results
    print("\n" + "="*70)
    print("INTELLIGENT IMAGE RANKING RESULTS:")
    print("="*70)
    
    if response.messages:
        last_message = response.messages[-1].to_text()
        
        try:
            if hasattr(last_message, 'content') and last_message.content:
                content = last_message.content
                if isinstance(content, dict):
                    # Handle structured response
                    result = ImageSuggestion(**content)
                    print(f"🔍 Keyword: {result.image_keyword}")
                    print("🏆 Top 3 Intelligent Rankings:")
                    print("-" * 70)
                    
                    for i, img in enumerate(result.ranked_images, 1):
                        score_emoji = "🎯" if img.score >= 9.0 else "⭐" if img.score >= 7.0 else "✅"
                        print(f"{i}. {score_emoji} Score: {img.score:.1f}/10.0")
                        print(f"   📷 URL: {img.url}")
                        print()
                        
                    # Show score analysis
                    scores = [img.score for img in result.ranked_images]
                    print("📊 Score Analysis:")
                    print(f"   Highest: {max(scores):.1f} | Lowest: {min(scores):.1f} | Spread: {max(scores)-min(scores):.1f}")
                    
                else:
                    # Handle text response
                    print("📄 LLM Response:")
                    print(content)
        except Exception as e:
            print(f"⚠️  Error displaying results: {e}")
            print("📋 Raw response:", last_message)
    else:
        print("❌ No response received from LLM")


asyncio.run(main())