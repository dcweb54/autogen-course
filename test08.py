from autogen_agentchat.agents import AssistantAgent
import copy
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
import asyncio
import json
import re
from typing import Dict, List, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TranscriptEnricher:
    """A sophisticated processor for enriching transcripts with image search strategies."""
    
    def __init__(self, model_client):
        self.model_client = model_client
        self.keyword_agent = self._create_keyword_agent()
        
    def _create_keyword_agent(self) -> AssistantAgent:
        """Create and configure the keyword generation agent."""
        return AssistantAgent(
            name="VisualStorytellerAgent",
            system_message=self._get_system_prompt(),
            model_client=self.model_client,
            reflect_on_tool_use=True,
            model_client_stream=True,
        )
    
    def _get_system_prompt(self) -> str:
        """Return the comprehensive system prompt for visual storytelling."""
        return """
        You are a VISUAL STORYTELLER specializing in creating image search blueprints for video content.

        # CORE MISSION
        Transform transcript segments into actionable image search strategies that follow narrative arcs.

        # STRATEGIC FRAMEWORK
        1. NARRATIVE ARC ANALYSIS: Map each segment to story progression (Exposition → Rising Action → Climax → Resolution)
        2. VISUAL HIERARCHY: Prioritize shots by importance (Establishing → Medium → Close-up → Detail)
        3. SEARCH OPTIMIZATION: Create Pexels-friendly queries that balance specificity with findability

        # RULES FOR IMAGE SUGGESTIONS
        - MUST use concrete visual descriptors (show, don't tell)
        - MUST maintain character/setting consistency throughout
        - MUST consider shot composition appropriate for the narrative moment
        - MUST avoid abstract concepts (hope, dream, fear) - use visual metaphors instead
        - MUST generate exactly 5 suggestions per segment, ranked by priority

        # QUERY GENERATION BLUEPRINT
        For each segment, analyze:
        🎯 NARRATIVE ROLE: Exposition/Conflict/Resolution/Transition
        📷 SHOT TYPE: Establishing/Medium/Close-up/Detail
        🌟 VISUAL PRIORITY: Primary/Secondary/Contextual
        🔍 SEARCH STRATEGY: Broad → Specific layering

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
              "image_suggestions": [
                {
                  "query": "search phrase",
                  "priority": 1-5,
                  "shot_description": "visual description",
                  "composition_tips": ["tip1", "tip2"]
                }
              ]
            }
          ],
          "story_arc_summary": {
            "primary_character": "name",
            "primary_setting": "location",
            "emotional_arc": "description",
            "visual_theme": "overarching visual style"
          }
        }

        # QUALITY CONTROL
        - Validate all queries are 2-4 word phrases
        - Ensure visual consistency across segments
        - Verify narrative progression makes sense
        - Check for duplicate or redundant suggestions
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

    def _create_strategic_prompt(self, transcript: Dict) -> str:
        """Create a comprehensive prompt for the AI agent."""
        return f"""
        # VISUAL STORYTELLING MISSION
        
        ## STORY CONTEXT
        Full Narrative: "{transcript['text']}"
        Total Duration: {transcript['duration']} seconds
        
        ## SEGMENT ANALYSIS REQUEST
        Analyze each segment below and generate a comprehensive visual search strategy.
        
        For EACH segment, provide:
        1. Narrative role classification
        2. Recommended shot type
        3. Visual priority assessment
        4. 5 ranked image search suggestions with detailed metadata
        
        ## SEGMENTS TO PROCESS:
        {json.dumps(transcript['segments'], indent=2)}
        
        ## STRATEGIC CONSIDERATIONS:
        - Consider pacing: shorter durations may need more impactful/close-up visuals
        - Maintain character consistency throughout
        - Build visual tension following the narrative arc
        - Ensure search queries are actually findable on stock sites
        
        Return complete JSON response with story arc summary.
        """

    def _parse_and_validate_response(self, response_content: str) -> Optional[Dict]:
        """Parse and validate the AI response with robust error handling."""
        try:
            # Extract JSON from potential markdown or other formatting
            json_match = re.search(r'```json\s*(.*?)\s*```', response_content, re.DOTALL)
            if json_match:
                response_content = json_match.group(1)
            
            data = json.loads(response_content)
            
            # Validate response structure
            if 'segments' not in data:
                raise ValueError("Missing 'segments' key in response")
                
            for segment in data['segments']:
                if 'image_suggestions' not in segment:
                    raise ValueError(f"Missing 'image_suggestions' in segment {segment.get('id', 'unknown')}")
                    
            return data
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed: {e}")
            return None
        except ValueError as e:
            logger.error(f"Validation error: {e}")
            return None

    async def enrich_transcript(self, transcript: Dict):
        """Main method to enrich transcript with visual search strategy."""
        if not self._validate_transcript_structure(transcript):
            raise ValueError("Invalid transcript structure")
        
        enriched_transcript = copy.deepcopy(transcript)
        
        try:
            # Create strategic prompt
            prompt = self._create_strategic_prompt(transcript)
            
            # Get AI response
            logger.info("Generating visual search strategy...")
            response = await Console(self.keyword_agent.run_stream(task=prompt))
            
            # Parse and validate response
            # parsed_data = self._parse_and_validate_response(response.content)
            
            # if not parsed_data:
            #     logger.warning("Failed to parse AI response, using fallback strategy")
            #     return self._apply_fallback_strategy(enriched_transcript)
            
            # Merge AI insights with original transcript
            # self._merge_strategic_data(enriched_transcript, parsed_data)
            
            logger.info("Successfully enriched transcript with visual strategy")
            # return enriched_transcript
            
        except Exception as e:
            logger.error(f"Error in enrichment process: {e}")
            # return self._apply_fallback_strategy(enriched_transcript)

    def _apply_fallback_strategy(self, transcript: Dict) -> Dict:
        """Fallback strategy if AI processing fails."""
        for segment in transcript['segments']:
            segment['image_suggestions'] = [{
                'query': 'fallback generic image',
                'priority': 1,
                'shot_description': 'Generic placeholder',
                'composition_tips': ['Use appropriate shot for duration']
            }]
        return transcript

    def _merge_strategic_data(self, original: Dict, ai_data: Dict) -> None:
        """Merge AI-generated strategic data with original transcript."""
        segment_map = {s['id']: s for s in ai_data['segments']}
        
        for original_segment in original['segments']:
            ai_segment = segment_map.get(original_segment['id'])
            if ai_segment:
                # Add all AI-generated fields
                for key, value in ai_segment.items():
                    if key not in ['id', 'text', 'start', 'end', 'duration']:
                        original_segment[key] = value
        
        # Add story summary if available
        if 'story_arc_summary' in ai_data:
            original['story_arc_summary'] = ai_data['story_arc_summary']


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
    
    # Display results
    print("\n" + "="*60)
    print("🎬 VISUAL STORYTELLING BLUEPRINT")
    print("="*60)
    # print(json.dumps(enriched_result, indent=2, ensure_ascii=False))
    
    # Generate summary report
    print("\n" + "="*60)
    print("📊 STRATEGIC SUMMARY")
    print("="*60)
    # if 'story_arc_summary' in enriched_result:
    #     summary = enriched_result['story_arc_summary']
    #     print(f"Primary Character: {summary.get('primary_character', 'N/A')}")
    #     print(f"Primary Setting: {summary.get('primary_setting', 'N/A')}")
    #     print(f"Visual Theme: {summary.get('visual_theme', 'N/A')}")
    #     print(f"Emotional Arc: {summary.get('emotional_arc', 'N/A')}")


if __name__ == "__main__":
    asyncio.run(main())