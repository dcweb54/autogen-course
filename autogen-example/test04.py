prompt_template = """
Extract 3-6 image search keywords from the transcript segment below.
Output JSON strictly as:
{{
    "id": {id},
    "keywords": ["word1", "word2", "word3"]
}}

Transcript Segment:
{id}: "{text}"
"""

# Fill in the template
filled_prompt = prompt_template.format(
    id="segment_001",
    text="The scientist examined the microscopic organisms under the laboratory microscope",
)

print(filled_prompt)
