# import uuid
# from pathlib import Path
# import os
# current_file_path = Path(__file__)

# # Get the parent directory
# load_prompt = os.path.join(current_file_path.parent,'notes.md')


# with open(load_prompt,'r') as f:
#     load = f.read()
    
# print(load)

# # Generate a UUID and convert it to a string for use as a filename
# random_filename = str(uuid.uuid4())

# print(random_filename[1:5])

# import os

# # full_path = __file__
# current_file = __file__.split("\\")[-1].split(".")[0]
# print(f"Full path: {current_file}")


#  how to get file path name

# print(parent_directory)



from datetime import datetime

current_date = datetime.now().strftime("%B %d, %Y")
main_theme = "Overcoming Self-Doubt"

prompts = f"""
You are DailyResearcher, an expert in short-form motivational content.
Today is {current_date}. The core theme is: "{main_theme}".

Your task:
- Suggest **one** highly relevant, emotionally compelling subtopic for today.
- Choose the best tone for TikTok/Shorts (e.g., "gentle but firm", "energetic", "raw and honest").
- Provide 5 trending tags.

Rules:
- Subtopic must feel fresh—avoid repeats from the past 7 days.
- Tie to universal struggles (procrastination, self-doubt, burnout, etc.).
- If relevant, subtly align with seasonal/mood context (e.g., January = new beginnings, Monday = restart energy).
- Be specific: “starting before you’re ready” > “be confident”.

Return ONLY VALID JSON:
{{
  "subtopic": "...",
  "selected_tone": "...",
  "tags": ["...", "...", "...", "...", "..."]
}}
"""


print(prompts)