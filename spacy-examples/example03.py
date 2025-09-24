from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from pprint import pprint

# Step 1: Load the model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Step 2: Reference words for each category
reference_words = {
    "characters": ["Alex", "hiker", "climber", "traveler", "adventurer"],
    "locations": ["mountain", "trail", "peak", "forest", "summit", "path"],
    "actions": ["climb", "walk", "hike", "struggle", "stumble", "rest", "howl", "block", "grow", "dream"],
    "nouns": ["gear", "backpack", "obstacle", "path", "wind", "hope", "rock", "step", "training"]
}

# Step 3: Precompute embeddings for reference words
ref_embeddings = {
    category: model.encode(words) for category, words in reference_words.items()
}

# Step 4: Suggest missing elements
def suggest_missing(sentence, present, ref_embeddings, reference_words, top_k=2, threshold=0.4):
    sent_embedding = model.encode(sentence)
    suggestions = {}

    for category in reference_words.keys():
        # Skip categories that already have values
        if present.get(category) and len(present[category]) > 0:
            continue

        # Get cosine similarities between sentence and reference words
        sims = cosine_similarity([sent_embedding], ref_embeddings[category])[0]
        top_indices = np.argsort(sims)[-top_k:][::-1]
        top_matches = [
            reference_words[category][i]
            for i in top_indices if sims[i] > threshold
        ]
        suggestions[category] = top_matches

    return suggestions

# Step 5: Input data (example sentences)
data = [
    {
        "sentence": "The first steps were easy.",
        "characters": [],
        "locations": [],
        "actions": [],
        "nouns": ["step"]
    },
    {
        "sentence": "But soon the trail grew steeper.",
        "characters": [],
        "locations": [],
        "actions": ["grow"],
        "nouns": ["trail"]
    },
    {
        "sentence": "Rocks blocked the way.",
        "characters": [],
        "locations": [],
        "actions": ["block"],
        "nouns": ["rock", "way"]
    },
    {
        "sentence": "The wind howled.",
        "characters": [],
        "locations": [],
        "actions": ["howl"],
        "nouns": ["wind"]
    },
    {
        "sentence": "Just a person with a dream and a backpack full of hope.",
        "characters": [],
        "locations": [],
        "actions": [],
        "nouns": ["person", "dream", "backpack", "hope"]
    }
]

# Step 6: Process each sentence
for entry in data:
    present = {
        "characters": entry["characters"],
        "locations": entry["locations"],
        "actions": entry["actions"],
        "nouns": entry["nouns"]
    }
    entry["suggestions"] = suggest_missing(entry["sentence"], present, ref_embeddings, reference_words)

# Step 7: Print results
pprint(data)
