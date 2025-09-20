from __future__ import annotations
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
import asyncio
import json
from typing import List, Optional
from pydantic import BaseModel, Field, validator
import logging
from pathlib import Path
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
import re

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RankedImage(BaseModel):
    url: str = Field(..., description="URL of the image")
    score: float = Field(
        ..., ge=1.0, le=10.0, description="Relevance score between 1.0 and 10.0"
    )


class ImageSuggestion(BaseModel):
    image_keyword: str = Field(..., description="The search keyword")
    ranked_images: List[RankedImage] = Field(
        ..., min_items=3, max_items=3, description="Exactly 3 ranked images"
    )


class ImageMetadata(BaseModel):
    contentUrl: str
    name: str


class ImageRanker:
    def __init__(self):
        self.client = OpenAIChatCompletionClient(
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

        self.image_ranker = AssistantAgent(
            name="image_ranker",
            model_client=self.client,
            model_client_stream=True,
            reflect_on_tool_use=True,
            system_message=self._get_system_message(),
        )

    def _get_system_message(self) -> str:
        return (
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
            '    {"url": "image_url_1", "score": 9.5},\n'
            '    {"url": "image_url_2", "score": 8.2},\n'
            '    {"url": "image_url_3", "score": 7.1}\n'
            "  ]\n"
            "}\n"
            "7. If you cannot find 3 suitable images, prioritize the most relevant ones anyway.\n"
            "8. NEVER include images that don't match the keyword requirements.\n"
        )

    def _prefilter_images(self, images: List[dict], keyword: str) -> List[dict]:
        """Pre-filter images to remove obviously irrelevant ones"""
        filtered = []
        keyword_lower = keyword.lower()

        for img in images:
            name = img.get("name", "").lower()
            url = img.get("contentUrl", "")

            # Skip AI-generated images unless explicitly requested
            if "ai-generated" in name and "ai" not in keyword_lower:
                continue

            # Skip non-human/non-face images for face-related keywords
            if any(
                term in keyword_lower
                for term in ["face", "portrait", "close-up", "expression"]
            ):
                if not any(
                    term in name
                    for term in [
                        "man",
                        "woman",
                        "person",
                        "face",
                        "portrait",
                        "girl",
                        "boy",
                        "child",
                    ]
                ):
                    continue

            filtered.append(img)

        return filtered or images  # Return original if filtering removes everything

    def _create_prompt(self, keyword: str, images: List[dict]) -> str:
        """Create a structured prompt for the AI"""
        filtered_images = self._prefilter_images(images, keyword)

        return f"""
        KEYWORD ANALYSIS:
        Keyword: "{keyword}"
        - Required: close-up, face, doubt expression
        - Preferred: human subjects, natural expressions
        - Avoid: AI-generated, non-human, irrelevant subjects
        
        IMAGE DATASET:
        Here are {len(filtered_images)} potentially relevant images:
        {json.dumps(filtered_images, indent=2)}
        
        INSTRUCTIONS:
        1. Select EXACTLY 3 most relevant images
        2. Rank them by relevance to the keyword
        3. Assign scores from 10.0 (most relevant) to 1.0 (least relevant)
        4. Focus on: facial expression, close-up framing, human subjects
        5. Return ONLY valid JSON in the specified format
        6. Ensure all 3 images are returned, even if some are less perfect matches
        
        OUTPUT FORMAT (JSON):
        {{
          "image_keyword": "{keyword}",
          "ranked_images": [
            {{"url": "url1", "score": 9.5}},
            {{"url": "url2", "score": 8.2}},
            {{"url": "url3", "score": 7.1}}
          ]
        }}
        """

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((ValueError, json.JSONDecodeError)),
        reraise=True,
    )
    async def rank_images(self, keyword: str, images: List[dict]):
        """Rank images with retry mechanism and validation"""
        prompt = self._create_prompt(keyword, images)

        logger.info(f"Ranking images for keyword: {keyword}")
        logger.info(
            f"Using {len(images)} total images ({len(self._prefilter_images(images, keyword))} after pre-filtering)"
        )

        try:
            response = await Console(self.image_ranker.run_stream(task=prompt))
            last_message = response.messages[-1].to_text()

            # Extract JSON from response
            json_str = json.loads(last_message)
            path = Path("output_suggestion_url.json")
            with path.open("w", encoding="utf-8") as f:
                json.dump(json_str, f, ensure_ascii=False, indent=2)

            # Parse and validate

            # Additional validation
            # self._validate_result(result, images)

            # logger.info(f"Successfully ranked 3 images with scores: {[img.score for img in result.ranked_images]}")
            # return result

        except Exception as e:
            logger.error(f"Failed to rank images: {e}")
            raise


async def main():
    ranker = ImageRanker()

    keyword = "close-up of Alex's face showing doubt"

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
            "contentUrl": "https://cdn.pixabay.com/photo/2022/12/24/21/14/portrait-7676482_1280.jpg",
            "name": "Free Portrait Man photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2014/01/18/10/14/vaulted-cellar-247391_1280.jpg",
            "name": "Free Vaulted Cellar Tunnel photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2015/04/25/08/42/tree-738816_1280.jpg",
            "name": "Free Tree Bald illustration and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2017/11/12/09/05/black-2941843_1280.jpg",
            "name": "Free Black Blow photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2014/08/24/14/40/stairs-426389_1280.jpg",
            "name": "Free Stairs Steps photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2017/08/07/23/25/woman-2609115_1280.jpg",
            "name": "Free Woman Sad photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2018/01/02/20/46/tunnel-3057026_1280.jpg",
            "name": "Free Tunnel Architecture photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2021/03/26/15/21/beautiful-6126170_1280.jpg",
            "name": "Free Beautiful Woman photo and picture",
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
            "contentUrl": "https://cdn.pixabay.com/photo/2017/06/03/01/15/bike-2367705_1280.jpg",
            "name": "Free Bicycle Traffic Light photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2018/08/17/10/10/christmas-wallpaper-3612508_1280.jpg",
            "name": "Free Christmas Wallpaper Candlelight photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2022/12/03/12/11/coffee-7632568_1280.jpg",
            "name": "Free Coffee Pastries photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2017/08/07/17/43/low-light-2606154_1280.jpg",
            "name": "Free Low Light People photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2017/03/12/21/22/candles-2138132_1280.jpg",
            "name": "Free Candles Candlelight photo and picture",
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
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2017/08/18/15/55/riverside-2655400_1280.jpg",
            "name": "Free Riverside Sunset photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2016/05/10/02/09/blue-1382940_1280.jpg",
            "name": "Free Blue Girl photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2019/04/18/00/32/tray-people-4135839_1280.jpg",
            "name": "Free Carton Man Doll photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2024/07/07/06/26/ai-generated-8878414_1280.jpg",
            "name": "Free Ai Generated Stress illustration and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2020/04/07/04/17/desperate-5011953_1280.jpg",
            "name": "Free Desperate Think photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2018/01/04/15/07/fantasy-3060912_1280.jpg",
            "name": "Free Fantasy Monument photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2015/12/11/13/59/lights-1088141_1280.jpg",
            "name": "Free Lights Lamps photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2016/12/09/08/56/roma-1893861_1280.jpg",
            "name": "Free Roma Ceiling photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2020/10/07/12/33/cafe-5635015_1280.jpg",
            "name": "Free Cafe Interior photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2021/10/09/06/46/baloch-6693129_1280.jpg",
            "name": "Free Baloch Iranian photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2020/06/03/14/28/light-5255121_1280.jpg",
            "name": "Free Light Bulb photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2023/09/15/20/33/ai-generated-8255513_1280.jpg",
            "name": "Free Ai Generated Woman illustration and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2022/01/06/01/03/railway-6918365_1280.jpg",
            "name": "Free Railway Track photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2020/11/24/11/52/room-5772311_1280.jpg",
            "name": "Free Room Attic photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2016/11/29/02/59/girl-1866959_1280.jpg",
            "name": "Free Girl African American photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2020/10/07/12/33/cafe-5635013_1280.jpg",
            "name": "Free Cafe Interior photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2025/06/12/21/10/girl-9656879_1280.png",
            "name": "Free Girl Candle illustration and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2015/11/16/08/50/dim-sum-1045400_1280.jpg",
            "name": "Free Dim Sum Food photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2023/01/27/08/42/light-7748075_1280.jpg",
            "name": "Free Light Girl photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2020/08/23/09/05/hong-kong-5510261_1280.jpg",
            "name": "Free Hong Kong Wedding Reception photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2016/01/31/00/23/light-bulb-1170778_1280.jpg",
            "name": "Free Light Bulb Idea photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2017/10/18/20/36/homework-2865410_1280.jpg",
            "name": "Free Homework Time Management photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2018/02/03/05/22/car-3126964_1280.jpg",
            "name": "Free Car Garage illustration and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2018/11/22/19/43/sculpture-3832653_1280.jpg",
            "name": "Free Sculpture Sad Girl photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2016/10/05/02/08/notre-dame-1715909_1280.jpg",
            "name": "Free Notre Dame Cathedral photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2019/06/12/13/31/person-4269272_1280.jpg",
            "name": "Free Person Girl illustration and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2024/07/07/06/26/ai-generated-8878417_1280.jpg",
            "name": "Free Ai Generated Stress illustration and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2024/02/22/17/44/rain-8590529_1280.png",
            "name": "Free Rain Dog illustration and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2015/07/14/06/06/man-844208_1280.jpg",
            "name": "Free Man Portrait photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2015/11/01/19/42/abandonded-1017454_1280.jpg",
            "name": "Free Abandonded Building photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2025/01/16/17/55/face-9338090_1280.jpg",
            "name": "Free Face Soul illustration and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2019/07/13/18/40/floor-4335428_1280.jpg",
            "name": "Free Floor Gloomy photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2023/03/17/16/14/silhouette-7858977_1280.jpg",
            "name": "Free Silhouette Person photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2019/11/20/12/35/mood-4639945_1280.jpg",
            "name": "Free Mood Architecture photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2020/01/01/13/31/church-4733584_1280.jpg",
            "name": "Free Church Dim Fireworks photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2017/08/26/11/11/torii-2682780_1280.jpg",
            "name": "Free Torii Light photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2017/08/07/08/58/house-2601655_1280.jpg",
            "name": "Free House Rocking photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2018/05/22/22/36/girl-3422711_1280.jpg",
            "name": "Free Girl Sad photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2021/11/11/21/32/tea-light-6787277_1280.jpg",
            "name": "Free Tea Light Candle photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2015/12/17/17/03/light-1097599_1280.jpg",
            "name": "Free Light Nature photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2021/12/30/00/10/dim-sum-6903004_1280.jpg",
            "name": "Free Dim Sum Breakfast photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2021/11/11/14/34/tunnel-6786462_1280.jpg",
            "name": "Free Tunnel Light photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2016/01/05/09/11/dim-sum-1122153_1280.jpg",
            "name": "Free Dumpling Dim Sum photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2024/04/22/17/19/ai-generated-8713140_1280.jpg",
            "name": "Free Ai Generated Dim Sum illustration and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2025/05/27/03/35/ai-generated-9624435_1280.png",
            "name": "Free Ai Generated Study illustration and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2025/06/13/21/48/mother-9658822_1280.jpg",
            "name": "Free Mother Son illustration and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2016/09/01/13/35/doll-1636128_1280.jpg",
            "name": "Free Puppet Clown photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2019/07/31/01/44/hanamaki-4374137_1280.jpg",
            "name": "Free Hanamaki Steamed Bun photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2022/11/04/10/55/man-7569552_1280.jpg",
            "name": "Free Man Cave illustration and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2023/06/15/02/40/window-8064282_1280.png",
            "name": "Free Window Room illustration and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2019/07/31/01/44/hanamaki-4374138_1280.jpg",
            "name": "Free Hanamaki Steamed Bun photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2024/06/23/20/54/ai-generated-8848753_1280.jpg",
            "name": "Free Ai Generated Movie Theater illustration and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2017/02/08/13/43/woman-2048905_1280.jpg",
            "name": "Free Woman Sad photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2024/07/07/06/26/ai-generated-8878419_1280.jpg",
            "name": "Free Ai Generated Stress illustration and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2017/08/07/07/26/hand-2600996_1280.jpg",
            "name": "Free Hand Palm photo and picture",
        },
        {
            "contentUrl": "https://cdn.pixabay.com/photo/2016/09/01/13/33/doll-1636124_1280.jpg",
            "name": "Free Puppet Clown photo and picture",
        },
    ]

    await ranker.rank_images(keyword, images)


asyncio.run(main())
