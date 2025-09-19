from __future__ import annotations
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
import asyncio
import json
from typing import List
from pydantic import BaseModel


class RankedImage(BaseModel):
    id: int
    name: str
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
        name="adventure_film_director",
        model_client=client,
        model_client_stream=True,
        reflect_on_tool_use=True,
        system_message=(
            "You are a professional adventure film director and outdoor cinematography expert.\n"
            "You specialize in mountain climbing scenes and authentic outdoor storytelling.\n\n"
            "PROFESSIONAL SCORING CRITERIA:\n"
            "9.5-10.0: Perfect mountain climbing moment - authentic struggle, real outdoor setting\n"
            "8.5-9.4: Excellent adventure shot - strong emotional resonance with climbing context\n"
            "7.5-8.4: Very good - captures mountain struggle but may need compositional adjustments\n"
            "6.5-7.4: Good option - shows effort but might lack specific doubt expression\n"
            "5.5-6.4: Acceptable - generic outdoor struggle without specific climbing context\n"
            "4.0-5.4: Marginal - barely relevant to mountain climbing narrative\n"
            "1.0-3.9: Unusable - contradicts mountain climbing context or emotional tone\n\n"
            "STORY-SPECIFIC CONSIDERATIONS:\n"
            "1. Amateur climber (not professional mountaineer)\n"
            "2. Early stages of climb (not summit attempt)\n"
            "3. Authentic doubt expression during physical struggle\n"
            "4. Mountain environment with challenging terrain\n"
            "5. Natural lighting and weather conditions\n"
            "6. Age-appropriate (20s-30s) non-professional appearance\n"
        ),
    )

    # Your specific story context
    story_context = """
    STORY: "The Dream of Eagle's Peak"
    
    GENRE: Inspirational Adventure Drama
    TONE: Determined yet vulnerable, authentic struggle
    
    PROTAGONIST: Alex, amateur climber
    - Background: Dreamer attempting something beyond their experience level
    - Personality: Hopeful but realistic, facing first major obstacles
    - Current state: Beginning to doubt capabilities during initial challenges
    
    SCENE CONTEXT:
    - Location: Lower slopes of Eagle's Peak mountain
    - Environment: Rocky terrain, steep incline, windy conditions
    - Action: Alex encountering first real obstacles after optimistic start
    - Emotional state: Hope turning to doubt, physical struggle triggering mental uncertainty
    - Time: Daytime, natural mountain lighting
    
    KEY NARRATIVE ELEMENTS:
    - "Rocks blocked the way" - physical obstacles
    - "The wind howled" - environmental challenges  
    - "Doubt crept in" - internal emotional shift
    - "Not an expert" - amateur status important
    - "Backpack full of hope" - emotional baggage metaphor
    """

    keyword = "close-up of Alex's face showing doubt during mountain climb"
    
    # load a json file and # sample image metadata as input
    with open("input.json", "r", encoding="utf-8") as f:
        images = json.load(f)

    # print(images)          # Python dict
    # print(type(images['name']))    # <class 'dict'>
    
    selected = list(map(lambda x: {"id": x["id"], "name": x["name"]}, images))

    # Professional adventure director's brief
    input_prompt = f"""
    🏔️ ADVENTURE DIRECTOR'S BRIEF - MOUNTAIN CLIMBING SCENE
    
    STORY CONTEXT:
    {story_context}
    
    SPECIFIC MOMENT TO CAPTURE:
    "{keyword}"
    
    IMAGE DATASET FOR CONSIDERATION:
    {json.dumps(selected, indent=2)}
    
    🎯 YOUR ROLE AS ADVENTURE DIRECTOR:
    You are selecting reference images for a crucial mountain climbing scene. Consider:
    
    1. MOUNTAIN AUTHENTICITY: Does this look like real mountain terrain? (rocks, steepness, natural environment)
    2. AMATEUR CLIMBER: Does the person look like a beginner? (appropriate age, non-professional appearance)
    3. DOUBT EXPRESSION: Is the facial expression authentic doubt during physical struggle?
    4. ENVIRONMENTAL CONTEXT: Can you sense wind, challenging conditions, outdoor elements?
    5. NARRATIVE ALIGNMENT: Does this match the "hope turning to doubt" emotional arc?
    
    ⚠️ STORY-SPECIFIC CONSTRAINTS:
    - NO summit shots (this is early climb)
    - NO professional climbing gear (amateur with basic equipment)
    - NO indoor or studio-looking images
    - NO overly dramatic or theatrical expressions
    - NO age mismatches (Alex is young adult)
    
    🏆 SELECTION CRITERIA:
    Choose images that feel like documentary footage of a real person's first mountain challenge.
    Look for authentic struggle, not posed adventure shots.
    
    OUTPUT FORMAT:
    {{
      "image_keyword": "{keyword}",
      "ranked_images": [
        {{"id": <id>, "name":<name>,"score": 9.8}},
        {{"id": <id>,"name":<name>, "score": 8.7}},
        {{"id": <id>,"name":<name>, "score": 7.9}}
      ]
    }}
    
    Think like an adventure filmmaker capturing authentic human struggle against nature.
    """

    print("🏔️ Adventure image selection in progress...")
    print("📖 Story: The Dream of Eagle's Peak")
    print("🎭 Scene: First doubts on the mountain")
    print(f"📸 Images to evaluate: {len(selected)}")

    # Get professional-level response
    response = await Console(image_ranker.run_stream(task=input_prompt))

    # Display professional results
    print("\n" + "=" * 80)
    print("🏔️ ADVENTURE DIRECTOR'S IMAGE SELECTION")
    print("=" * 80)

    if response.messages:
        last_message = response.messages[-1].to_text()

        try:
            if hasattr(last_message, "content") and last_message.content:
                content = last_message.content
                if isinstance(content, dict):
                    result = ImageSuggestion(**content)

                    print("📖 Story: Amateur climber facing first mountain challenges")
                    print(f"🎯 Required: {result.image_keyword}")
                    print("\n" + "🏆 TOP 3 ADVENTURE SHOTS:" + "\n" + "-" * 50)

                    for i, img in enumerate(result.ranked_images, 1):
                        # Adventure-specific rating descriptions
                        if img.score >= 9.0:
                            rating = "MOUNTAIN AUTHENTIC"
                            emoji = "🏔️"
                        elif img.score >= 8.0:
                            rating = "ADVENTURE READY"
                            emoji = "⛰️"
                        elif img.score >= 7.0:
                            rating = "OUTDOOR WORTHY"
                            emoji = "🌄"
                        else:
                            rating = "BACKUP OPTION"
                            emoji = "🎒"

                        print(f"{i}. {emoji} {rating} - Score: {img.score:.1f}/10.0")
                        print(f"   📷 Reference URL: {img.url}")
                        print(
                            f"   🎬 Director's Note: {'Perfect struggle moment' if img.score > 9.0 else 'Good emotional capture' if img.score > 8.0 else 'Works with context'}"
                        )
                        print()

                    # Professional analysis
                    scores = [img.score for img in result.ranked_images]
                    print("📊 ADVENTURE ASSESSMENT:")
                    print(
                        f"   Best choice: {max(scores):.1f} ({(max(scores) / 10) * 100:.0f}% story match)"
                    )
                    print("Emotional range: Hope → Doubt → Determination")
                    print(
                        f"Scene authenticity: {'Highly believable' if max(scores) > 8.5 else 'Moderately convincing'}"
                    )

                else:
                    print("📝 Director's Mountain Notes:")
                    print(content)
        except Exception as e:
            print(f"⚠️  Technical note: {e}")
            print("📋 Raw selection:", last_message)
    else:
        print("❌ No selection made - please check connection")


asyncio.run(main())
