# from sentence_transformers import SentenceTransformer, util

# model = SentenceTransformer('all-MiniLM-L6-v2')

# query_embedding = model.encode("mountain peak silhouette")

# image_embedding = model.encode(image_tags_string)

# similarity = util.cos_sim(query_embedding, image_embedding)


from sentence_transformers import SentenceTransformer, util
import json

# # ====== Load Model ======
model = SentenceTransformer('all-MiniLM-L6-v2')

# # ====== Example Segment ======
# segment = {
#     "id": 1,
#     "text": "Alex had always dreamed of reaching the top of Eagle's Peak,",
#     "image_suggestion": [
#         "mountain peak silhouette",
#         "young hiker gazing at the sky",
#         "close-up on a map"
#     ]
# }


with open("output.json", "r", encoding="utf-8") as f:
    segments = json.load(f)


segment = segments['segments'][2]
# # ====== Mock Image Metadata ======
# # Imagine these are tags from Pixabay images
mock_images = [
    {"url": "image1.jpg", "tags": "mountain, peak, landscape, sky"},
    {"url": "image2.jpg", "tags": "hiker, person, mountain, outdoors"},
    {"url": "image3.jpg", "tags": "map, compass, travel, adventure"},
    {"url": "image4.jpg", "tags": "sunset, valley, cliff, nature"}
]

with open("input.json", "r", encoding="utf-8") as f:
    images = json.load(f)
# # ====== Compute Similarity ======
selected_image = None
best_score = -1

for suggestion in segment["image_suggestion"]:
    print(suggestion)
    suggestion_embedding = model.encode(suggestion)

    for image in images:
        image_embedding = model.encode(image["name"])
        similarity = util.cos_sim(suggestion_embedding, image_embedding).item()
        
        print(f"Suggestion: '{"mountain peak silhouette"}' | Image: {image['contentUrl']} | Score: {similarity:.3f}")
        
        if similarity > best_score:
            best_score = similarity
            selected_image = image

    print("\n=== BEST MATCH ===")
    print(f"Selected Image: {selected_image['contentUrl']} with score {best_score:.3f}")
