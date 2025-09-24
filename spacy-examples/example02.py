from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer('all-mpnet-base-v2')


reference_words = {
    "characters": ["Alex", "climber", "hiker"],
    "locations": ["mountain", "trail", "peak", "forest"],
    "actions": ["walk", "climb", "struggle", "stumble", "rest"],
    "nouns": ["gear", "backpack", "obstacle", "path", "snow"]
}
ref_embeddings = {
    category: model.encode(words) for category, words in reference_words.items()
}


def suggest_missing(sentence, present, ref_embeddings, reference_words, top_k=2, threshold=0.5):
    sent_embedding = model.encode(sentence)

    suggestions = {}
    for category, embeddings in ref_embeddings.items():
        if category in present and present[category]:
            continue  # Already has elements

        sims = cosine_similarity([sent_embedding], embeddings)[0]
        top_indices = np.argsort(sims)[-top_k:][::-1]
        top_suggestions = [
            reference_words[category][i]
            for i in top_indices if sims[i] > threshold
        ]
        print(top_suggestions)
        suggestions[category] = top_suggestions
    return suggestions

def process_sentence(entry, model, ref_embeddings, reference_words):
    sentence = entry["sentence"]
    present = {
        "characters": entry["characters"],
        "locations": entry["locations"],
        "actions": entry["actions"],
        "nouns": entry["nouns"]
    }
    return suggest_missing(sentence, present, ref_embeddings, reference_words)



# Example data (from your input)
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

# Process all entries
for entry in data:
    sentence = entry["sentence"]
    present = {
        "characters": entry["characters"],
        "locations": entry["locations"],
        "actions": entry["actions"],
        "nouns": entry["nouns"]
    }
    suggestions = suggest_missing(sentence, present, ref_embeddings, reference_words)
    entry["suggestions"] = suggestions

# Display output
from pprint import pprint  # noqa: E402
pprint(data)