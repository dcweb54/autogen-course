import os
import json
import spacy

nlp = spacy.load("en_core_web_sm")
# from sentence_transformers import SentenceTransformer, util

# model = SentenceTransformer('all-MiniLM-L6-v2')

with open(
    os.path.join(os.getcwd(), "image_suggestion_system", "output.json"),
    "r",
    encoding="utf-8",
) as f:
    transcription = json.load(f)


doc = nlp(transcription["text"])

# Iterate over detected sentences
# for sent in doc.sents:
#     # print("-",sent.text,sent.label)
#     for ent in sent.ents:
#         print(ent.label_,"=>",ent)


# Print named entities with labels
# for ent in doc.ents:
#     print(ent.text, "→", ent.label_)

# structured_script = []

# for sent in doc.sents:
#     entry = {
#         "sentence": sent.text,
#         "characters": [ent.text for ent in sent.ents if ent.label_ == "PERSON"],
#         "locations": [
#             ent.text for ent in sent.ents if ent.label_ in ["GPE", "LOC", "FAC"]
#         ],
#         "actions": [token.lemma_ for token in sent if token.pos_ == "VERB"],
#         "nouns": [token.lemma_ for token in sent if token.pos_ == "NOUN"],
#         "raw": sent.text,
#     }
#     print(entry)
# structured_script.append(entry)

print("=================")

structured = []
# print(structured_script)
for sent in doc.sents:
    structured.append(
        {
            "sentence": sent.text,
            "characters": [ent.text for ent in sent.ents if ent.label_ == "PERSON"],
            "locations": [
                ent.text for ent in sent.ents if ent.label_ in ["GPE", "LOC", "FAC"]
            ],
            "actions": [token.lemma_ for token in sent if token.pos_ == "VERB"],
            "nouns": [token.lemma_ for token in sent if token.pos_ == "NOUN"],
        }
    )

file_path = "output_spacy.json"
with open(os.path.join(os.getcwd(), "image_suggestion_system",file_path), 'w') as json_file:
    json.dump(structured, json_file, indent=4)
print("++++++++++++++++++++++++")

# segments = transcription['segments']

# for segement in segments:
#     print(segement['text'])
