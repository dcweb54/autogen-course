# masterpiece_audio_visual_enricher.py
from autogen_agentchat.agents import AssistantAgent
import copy
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
import asyncio
import json
import re
from typing import Dict, List, Any, Optional, Tuple
import logging
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AudioMood(Enum):
    INSPIRATIONAL = "inspirational"
    TENSE = "tense"
    MELANCHOLY = "melancholy"
    TRIUMPHANT = "triumphant"
    NEUTRAL = "neutral"
    MYSTERIOUS = "mysterious"
    EPIC = "epic"
    CALM = "calm"

class SoundType(Enum):
    AMBIENT = "ambient"
    FX = "sound_effect"
    TRANSITION = "transition"
    TEXTURE = "texture"

class TranscriptEnricher:
    """A sophisticated processor for enriching transcripts with audio-visual strategies."""
    
    def __init__(self, model_client):
        self.model_client = model_client
        self.audio_visual_agent = self._create_audio_visual_agent()
        
    def _create_audio_visual_agent(self) -> AssistantAgent:
        """Create and configure the audio-visual strategy agent."""
        return AssistantAgent(
            name="AudioVisualStorytellerAgent",
            system_message=self._get_audio_visual_prompt(),
            model_client=self.model_client,
            reflect_on_tool_use=True,
            model_client_stream=True,
            max_consecutive_auto_reply=3,
            temperature=0.1
        )
    
    def _get_audio_visual_prompt(self) -> str:
        """Return the comprehensive system prompt for audio-visual storytelling."""
        return """
        You are an AUDIO-VISUAL STORYTELLER specializing in creating complete production blueprints.

        # CORE MISSION
        Transform transcript segments into actionable audio-visual strategies for professional video production.

        # AUDIO STRATEGY FRAMEWORK
        1. BACKGROUND MUSIC: Suggest music that matches emotional tone and narrative arc
        2. SOUND EFFECTS: Recommend specific SFX for actions and environments
        3. AMBIENT SOUNDS: Suggest background audio to enhance immersion
        4. TRANSITION SOUNDS: Recommend audio cues for scene changes

        # MUSIC MOOD CATEGORIES:
        - inspirational: Uplifting, motivational, positive (strings, piano, soft pads)
        - tense: Nervous, anxious, suspenseful (drones, low strings, percussion)
        - melancholy: Sad, reflective, thoughtful (piano, cello, minor keys)
        - triumphant: Victory, achievement, success (brass, orchestral, major keys)
        - epic: Grand, large-scale, dramatic (orchestral, choir, big drums)
        - calm: Peaceful, serene, tranquil (pads, nature sounds, soft textures)

        # SOUND EFFECT CATEGORIES:
        - ambient: Background environment sounds (wind, rain, forest, city)
        - sound_effect: Specific action sounds (footsteps, rustling, impacts)
        - transition: Whooshes, sweeps, risers for scene changes
        - texture: Atmospheric layers for depth (vinyl crackle, light drones)

        # OUTPUT FORMAT
        Strictly valid JSON with this structure:
        {
          "segments": [
            {
              "id": <int>,
              "text": "<segment_text>",
              "start": <float>,
              "end": <float>,
              "duration": <float>,
              "narrative_role": "exposition|conflict|resolution|transition",
              "shot_type": "establishing|medium|closeup|detail",
              "visual_priority": "primary|secondary|contextual",
              "emotional_tone": "hopeful|anxious|determined|reflective",
              "image_suggestions": [
                {
                  "query": "search phrase",
                  "priority": 1-5,
                  "shot_description": "visual description",
                  "composition_tips": ["tip1", "tip2"]
                }
              ],
              "audio_suggestions": {
                "background_music": {
                  "mood": "inspirational|tense|triumphant|etc",
                  "description": "music style description",
                  "search_terms": ["cinematic piano", "epic orchestral", "etc"]
                },
                "sound_effects": [
                  {
                    "type": "ambient|fx|transition|texture",
                    "description": "specific sound description",
                    "timing": "start|end|throughout|specific_time",
                    "search_terms": ["wind howling", "footsteps gravel", "etc"]
                  }
                ]
              }
            }
          ],
          "story_arc_summary": {
            "primary_character": "name",
            "primary_setting": "location",
            "emotional_arc": "description",
            "visual_theme": "overarching visual style",
            "audio_theme": {
              "overall_mood": "primary music mood",
              "recommended_bgm": "main background music style",
              "key_sound_elements": ["element1", "element2"],
              "music_transition_points": ["segment_id:time", "segment_id:time"]
            }
          }
        }

        # QUALITY CONTROL
        - Ensure audio suggestions match visual tone
        - Consider segment duration for sound effect placement
        - Create smooth audio transitions between segments
        - Suggest findable sound assets from platforms like Epidemic Sound, Artlist, Freesound
        """

    def _validate_transcript_structure(self, transcript: Dict) -> bool:
        """Validate the transcript structure meets requirements."""
        required_keys = ['segments', 'text', 'duration']
        if not all(key in transcript for key in required_keys):
            return False
        
        if not isinstance(transcript['segments'], list):
            return False
            
        required_segment_keys = ['id', 'text', 'start', 'end', 'duration']
        for segment in transcript['segments']:
            if not all(key in segment for key in required_segment_keys):
                return False
                
        return True

    def _create_audio_visual_prompt(self, transcript: Dict) -> str:
        """Create a comprehensive prompt for the AI agent."""
        return f"""
        # COMPLETE AUDIO-VISUAL STORYTELLING MISSION
        
        ## STORY CONTEXT
        Full Narrative: "{transcript['text']}"
        Total Duration: {transcript['duration']} seconds
        
        ## COMPREHENSIVE ANALYSIS REQUEST
        Analyze each segment below and generate complete audio-visual production strategy.
        
        For EACH segment, provide:
        1. Visual strategy (shot types, compositions, search terms)
        2. Audio strategy (music mood, specific sound effects, ambient layers)
        3. Emotional tone analysis
        4. Timing and synchronization recommendations
        
        ## SEGMENTS TO PROCESS:
        {json.dumps(transcript['segments'], indent=2)}
        
        ## STRATEGIC CONSIDERATIONS:
        - Match audio mood to visual tone and narrative moment
        - Consider segment duration for sound effect placement
        - Suggest findable assets from major stock platforms
        - Create smooth transitions between audio segments
        - Build audio tension following the narrative arc
        
        Return complete JSON response with comprehensive story arc summary including audio theme.
        """

    def _parse_and_validate_response(self, response_content: str) -> Optional[Dict]:
        """Parse and validate the AI response with robust error handling."""
        try:
            json_match = re.search(r'```json\s*(.*?)\s*```', response_content, re.DOTALL)
            if json_match:
                response_content = json_match.group(1)
            
            data = json.loads(response_content)
            
            # Validate response structure
            if 'segments' not in data:
                raise ValueError("Missing 'segments' key in response")
                
            for segment in data['segments']:
                if 'audio_suggestions' not in segment:
                    raise ValueError(f"Missing 'audio_suggestions' in segment {segment.get('id', 'unknown')}")
                    
            return data
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed: {e}")
            return None
        except ValueError as e:
            logger.error(f"Validation error: {e}")
            return None

    def _suggest_audio_assets(self, emotional_tone: str, duration: float) -> Dict:
        """Generate audio suggestions based on emotional tone and duration."""
        audio_templates = {
            "hopeful": {
                "background_music": {
                    "mood": "inspirational",
                    "description": "Uplifting cinematic strings with soft piano melodies",
                    "search_terms": ["inspirational cinematic", "hopeful orchestral", "uplifting strings"]
                },
                "sound_effects": [
                    {
                        "type": "ambient",
                        "description": "Gentle wind with distant bird sounds",
                        "timing": "throughout",
                        "search_terms": ["gentle wind", "forest ambiance", "morning birds"]
                    }
                ]
            },
            "tense": {
                "background_music": {
                    "mood": "tense",
                    "description": "Suspenseful drones with subtle percussion",
                    "search_terms": ["tense drones", "suspenseful ambient", "anxious strings"]
                },
                "sound_effects": [
                    {
                        "type": "texture",
                        "description": "Low rumbling with subtle crackles",
                        "timing": "throughout",
                        "search_terms": ["dark ambiance", "rumble low frequency", "tension texture"]
                    }
                ]
            },
            "triumphant": {
                "background_music": {
                    "mood": "triumphant",
                    "description": "Epic orchestral with brass and percussion",
                    "search_terms": ["epic orchestral", "triumphant brass", "victory music"]
                },
                "sound_effects": [
                    {
                        "type": "transition",
                        "description": "Orchestral hit or cymbal crash",
                        "timing": "end",
                        "search_terms": ["orchestral hit", "cymbal crash", "impact whoosh"]
                    }
                ]
            }
        }
        
        return audio_templates.get(emotional_tone.lower(), audio_templates["hopeful"])

    async def enrich_transcript(self, transcript: Dict) -> Dict:
        """Main method to enrich transcript with audio-visual strategy."""
        if not self._validate_transcript_structure(transcript):
            raise ValueError("Invalid transcript structure")
        
        enriched_transcript = copy.deepcopy(transcript)
        
        try:
            prompt = self._create_audio_visual_prompt(transcript)
            
            logger.info("Generating complete audio-visual strategy...")
            
            response = await  Console(self.audio_visual_agent.run_stream(task=prompt))
            
            # print(response.messages[-1].content.response)
            
            parsed_data = self._parse_and_validate_response(response.content)
            
            if not parsed_data:
                logger.warning("Failed to parse AI response, using fallback strategy")
                return self._apply_audio_fallback_strategy(enriched_transcript)
            
            self._merge_audio_visual_data(enriched_transcript, parsed_data)
            
            logger.info("Successfully enriched transcript with audio-visual strategy")
            return enriched_transcript
            
        except Exception as e:
            logger.error(f"Error in enrichment process: {e}")
            return self._apply_audio_fallback_strategy(enriched_transcript)

    def _apply_audio_fallback_strategy(self, transcript: Dict) -> Dict:
        """Fallback strategy if AI processing fails."""
        emotional_arc = ["hopeful", "determined", "tense", "challenging", "triumphant"]
        
        for i, segment in enumerate(transcript['segments']):
            mood_index = min(i, len(emotional_arc) - 1)
            emotional_tone = emotional_arc[mood_index]
            
            audio_suggestions = self._suggest_audio_assets(emotional_tone, segment['duration'])
            
            segment['emotional_tone'] = emotional_tone
            segment['audio_suggestions'] = audio_suggestions
            segment['image_suggestions'] = [{
                'query': f'{emotional_tone} {segment["text"][:20]}',
                'priority': 1,
                'shot_description': 'Fallback visual',
                'composition_tips': ['Use appropriate shot for emotional tone']
            }]
        
        return transcript

    def _merge_audio_visual_data(self, original: Dict, ai_data: Dict) -> None:
        """Merge AI-generated audio-visual data with original transcript."""
        segment_map = {s['id']: s for s in ai_data['segments']}
        
        for original_segment in original['segments']:
            ai_segment = segment_map.get(original_segment['id'])
            if ai_segment:
                for key, value in ai_segment.items():
                    if key not in ['id', 'text', 'start', 'end', 'duration']:
                        original_segment[key] = value
        
        if 'story_arc_summary' in ai_data:
            original['story_arc_summary'] = ai_data['story_arc_summary']

    def generate_audio_asset_list(self, enriched_transcript: Dict) -> List[Dict]:
        """Generate a comprehensive list of required audio assets."""
        audio_assets = []
        
        for segment in enriched_transcript['segments']:
            audio = segment.get('audio_suggestions', {})
            
            # Add background music
            if 'background_music' in audio:
                bgm = audio['background_music']
                audio_assets.append({
                    'type': 'music',
                    'segment_id': segment['id'],
                    'mood': bgm.get('mood', ''),
                    'search_terms': bgm.get('search_terms', []),
                    'duration': segment['duration'],
                    'priority': 'high'
                })
            
            # Add sound effects
            for sfx in audio.get('sound_effects', []):
                audio_assets.append({
                    'type': sfx.get('type', 'fx'),
                    'segment_id': segment['id'],
                    'description': sfx.get('description', ''),
                    'search_terms': sfx.get('search_terms', []),
                    'timing': sfx.get('timing', ''),
                    'priority': 'medium'
                })
        
        return audio_assets


async def main():
    # Initialize model client
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

    # Example transcript
    transcript = {
        "language": "en",
        "language_probability": 0.9995,
        "duration": 26.1,
        "text": "Alex had always dreamed of reaching the top of Eagle's Peak, a mountain so tall many said it can't be climbed without years of training. But Alex wasn't an expert. Just a person with a dream and a backpack full of hope. The first steps were easy. The path was clear. But soon the trail grew steeper. Rocks blocked the way. The wind howled. Doubt crept in.",
        "segments": [
            {"id": 1, "text": "Alex had always dreamed of reaching the top of Eagle's Peak,", "start": 0.0, "end": 3.74, "duration": 3.74},
            {"id": 2, "text": "a mountain so tall many said it can't be climbed without years of training.", "start": 3.92, "end": 8.6, "duration": 4.68},
            {"id": 3, "text": "But Alex wasn't an expert.", "start": 9.16, "end": 10.88, "duration": 1.72},
            {"id": 4, "text": "Just a person with a dream and a backpack full of hope.", "start": 11.5, "end": 15.02, "duration": 3.52},
            {"id": 5, "text": "The first steps were easy.", "start": 15.64, "end": 17.22, "duration": 1.58},
            {"id": 6, "text": "The path was clear.", "start": 17.32, "end": 18.52, "duration": 1.2},
            {"id": 7, "text": "But soon the trail grew steeper.", "start": 19.1, "end": 21.3, "duration": 2.2},
            {"id": 8, "text": "Rocks blocked the way.", "start": 21.68, "end": 22.78, "duration": 1.1},
            {"id": 9, "text": "The wind howled.", "start": 23.08, "end": 24.38, "duration": 1.3},
            {"id": 10, "text": "Doubt crept in.", "start": 25.06, "end": 26.1, "duration": 1.04},
        ],
    }

    # Process transcript
    enricher = TranscriptEnricher(model_client)
    enriched_result = await enricher.enrich_transcript(transcript)
    
    # Generate audio asset list
    audio_assets = enricher.generate_audio_asset_list(enriched_result)
    
    # Display results
    print("\n" + "="*80)
    print("🎬 COMPLETE AUDIO-VISUAL STORYTELLING BLUEPRINT")
    print("="*80)
    print(json.dumps(enriched_result, indent=2, ensure_ascii=False))
    
    # Display audio assets summary
    print("\n" + "="*80)
    print("🎵 REQUIRED AUDIO ASSETS")
    print("="*80)
    for asset in audio_assets:
        print(f"{asset['type'].upper():<12} | {asset['description'][:50]:<50} | {asset['mood'] if 'mood' in asset else 'N/A':<15} | Segment {asset['segment_id']}")
    
    # Generate summary report
    print("\n" + "="*80)
    print("📊 STRATEGIC SUMMARY")
    print("="*80)
    if 'story_arc_summary' in enriched_result:
        summary = enriched_result['story_arc_summary']
        audio_theme = summary.get('audio_theme', {})
        print(f"Primary Character: {summary.get('primary_character', 'N/A')}")
        print(f"Primary Setting: {summary.get('primary_setting', 'N/A')}")
        print(f"Visual Theme: {summary.get('visual_theme', 'N/A')}")
        print(f"Audio Mood: {audio_theme.get('overall_mood', 'N/A')}")
        print(f"Recommended BGM: {audio_theme.get('recommended_bgm', 'N/A')}")
        print(f"Key Sound Elements: {', '.join(audio_theme.get('key_sound_elements', []))}")


if __name__ == "__main__":
    asyncio.run(main())