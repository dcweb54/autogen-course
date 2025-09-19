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
        name="professional_image_director",
        model_client=client,
        model_client_stream=True,
        reflect_on_tool_use=True,
        system_message=(
            "You are a professional film director and visual storytelling expert.\n"
            "You have deep understanding of cinematic composition, emotional tone, and narrative context.\n\n"
            "PROFESSIONAL SCORING CRITERIA:\n"
            "9.5-10.0: Cinematic perfection - exactly matches story tone, character emotion, and visual style\n"
            "8.5-9.4: Excellent choice - strongly supports narrative and emotional context\n"
            "7.5-8.4: Very good - fits well with minor stylistic adjustments needed\n"
            "6.5-7.4: Good option - works but may require creative interpretation\n"
            "5.5-6.4: Acceptable - serves basic purpose but lacks narrative depth\n"
            "4.0-5.4: Marginal - barely relevant, use only if no better options\n"
            "1.0-3.9: Unusable - contradicts story tone or character portrayal\n\n"
            "EXPERT CONSIDERATIONS:\n"
            "1. Character consistency with Alex's personality and journey\n"
            "2. Emotional authenticity of the doubt expression\n"
            "3. Cinematic quality and visual storytelling potential\n"
            "4. Environmental context matching the story's setting\n"
            "5. Lighting and mood alignment with scene tone\n"
            "6. Composition and framing professional standards\n"
        ),
    )

    # Story context and script
    story_context = """
    STORY: "The Crossroads of Trust"
    
    GENRE: Psychological Drama
    TONE: Introspective, tense, emotionally raw
    
    PROTAGONIST: Alex Chen, 28-year-old software engineer
    - Background: Overachiever facing first major professional failure
    - Personality: Analytical, self-critical, usually confident but now doubting everything
    - Current state: Sleep-deprived, emotionally exhausted, questioning his career choices
    
    SCENE CONTEXT:
    - Time: 3 AM in Alex's minimalist apartment
    - Environment: Dark room lit only by laptop screen, empty coffee cups, scattered papers
    - Action: Alex staring at his reflection in the dark screen, realizing he might have made a catastrophic error
    - Emotional state: Deep doubt, self-questioning, vulnerability mixed with intense focus
    
    VISUAL STYLE REQUIREMENTS:
    - Lighting: Low-key, dramatic shadows, single light source (screen glow)
    - Framing: Intimate close-up, slightly off-center composition
    - Expression: Authentic doubt - not overly dramatic, subtle facial tension
    - Atmosphere: Isolation, introspection, technological alienation
    """

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

    # Professional director's brief
    input_prompt = f"""
    🎬 DIRECTOR'S BRIEF - PROFESSIONAL IMAGE SELECTION
    
    STORY CONTEXT:
    {story_context}
    
    SPECIFIC SHOT REQUIREMENT:
    "{keyword}"
    
    IMAGE DATASET FOR CONSIDERATION:
    {json.dumps(images, indent=2)}
    
    🎯 YOUR ROLE AS DIRECTOR:
    You are selecting the perfect reference image for this crucial scene. Consider:
    
    1. CHARACTER CONSISTENCY: Does the face match Alex's age (28), profession (engineer), and current emotional state?
    2. ENVIRONMENTAL CONTEXT: Does the lighting suggest late night/computer glow? Is the setting believably modern?
    3. EMOTIONAL AUTHENTICITY: Is the doubt expression subtle and believable for an intelligent professional?
    4. CINEMATIC QUALITY: Would this work as a reference for lighting, composition, and mood?
    5. NARRATIVE SUPPORT: Does the image enhance the story's themes of doubt and introspection?
    
    ⚠️ PROFESSIONAL CONSTRAINTS:
    - NO AI-generated images (breaks realism)
    - NO overly dramatic or theatrical expressions
    - NO inconsistent lighting with scene context
    - NO age/gender mismatches with character
    
    🏆 SELECTION CRITERIA:
    Choose images that feel like authentic documentary footage of this specific moment in Alex's life.
    
    OUTPUT FORMAT:
    {{
      "image_keyword": "{keyword}",
      "ranked_images": [
        {{"url": "EXACT_URL", "score": 9.8}},
        {{"url": "EXACT_URL", "score": 8.7}},
        {{"url": "EXACT_URL", "score": 7.9}}
      ]
    }}
    
    Think like a film director choosing reference images for their cinematographer.
    """

    print("🎬 Professional image selection in progress...")
    print("📖 Story: The Crossroads of Trust")
    print(f"🎭 Scene: {keyword}")
    print(f"📸 Images to evaluate: {len(images)}")

    # Get professional-level response
    response = await Console(image_ranker.run_stream(task=input_prompt))

    # Display professional results
    print("\n" + "=" * 80)
    print("🎬 DIRECTOR'S IMAGE SELECTION RESULTS")
    print("=" * 80)

    if response.messages:
        last_message = response.messages[-1]

        try:
            if hasattr(last_message, "content") and last_message.content:
                content = last_message.content
                if isinstance(content, dict):
                    result = ImageSuggestion(**content)

                    print(
                        "📖 Story Context: Psychological Drama - 3AM introspection scene"
                    )
                    print(f"🎯 Required: {result.image_keyword}")
                    print("\n" + "🏆 TOP 3 PROFESSIONAL CHOICES:" + "\n" + "-" * 50)

                    for i, img in enumerate(result.ranked_images, 1):
                        # Professional rating descriptions
                        if img.score >= 9.0:
                            rating = "CINEMATIC MASTERPIECE"
                            emoji = "🎬"
                        elif img.score >= 8.0:
                            rating = "PROFESSIONAL GRADE"
                            emoji = "⭐"
                        elif img.score >= 7.0:
                            rating = "PRODUCTION READY"
                            emoji = "✅"
                        else:
                            rating = "BACKUP OPTION"
                            emoji = "📦"

                        print(f"{i}. {emoji} {rating} - Score: {img.score:.1f}/10.0")
                        print(f"   📷 Reference URL: {img.url}")
                        print(
                            f"   💡 Director's Note: Would work with {'minimal' if img.score > 8.0 else 'some'} lighting adjustments"
                        )
                        print()

                    # Professional analysis
                    scores = [img.score for img in result.ranked_images]
                    print("📊 PROFESSIONAL ASSESSMENT:")
                    print(
                        f"   Best choice: {max(scores):.1f} ({(max(scores) / 10) * 100:.0f}% scene match)"
                    )
                    print(f"   Options range: {min(scores):.1f} - {max(scores):.1f}")
                    print(
                        f"   Overall quality: {'Excellent' if max(scores) > 8.5 else 'Good' if max(scores) > 7.0 else 'Adequate'}"
                    )

                else:
                    print("📝 Director's Notes:")
                    print(content)
        except Exception as e:
            print(f"⚠️  Technical note: {e}")
            print("📋 Raw selection:", last_message)
    else:
        print("❌ No selection made - please check connection")


asyncio.run(main())
