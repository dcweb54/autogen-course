import spacy
from textblob import TextBlob

# Load spaCy small English model
nlp = spacy.load("en_core_web_sm")

# Global visual style keywords to maintain consistency
STYLE_KEYWORDS = ["cinematic", "golden hour", "warm tones"]

def extract_global_context(script_segments):
    full_text = " ".join(script_segments)
    doc = nlp(full_text)
    global_keywords = set()

    # Named entities and noun chunks (overall subjects/settings)
    for ent in doc.ents:
        global_keywords.add(ent.text.lower())
    for chunk in doc.noun_chunks:
        global_keywords.add(chunk.text.lower())

    # Overall adjectives or repeated themes
    for token in doc:
        if token.pos_ == "ADJ":
            global_keywords.add(token.lemma_.lower())

    # Sentiment for mood
    sentiment = TextBlob(full_text).sentiment.polarity
    if sentiment > 0.2:
        global_keywords.update(["hopeful", "inspiring", "uplifting"])
    elif sentiment < -0.2:
        global_keywords.update(["tense", "dramatic", "struggle"])
    else:
        global_keywords.add("neutral")

    return global_keywords

def extract_segment_keywords(segment, global_tags):
    doc = nlp(segment)
    keywords = set()

    for ent in doc.ents:
        keywords.add(ent.text.lower())
    for chunk in doc.noun_chunks:
        keywords.add(chunk.text.lower())
    for token in doc:
        if token.pos_ == "ADJ":
            keywords.add(token.lemma_.lower())

    # Local sentiment
    sentiment = TextBlob(segment).sentiment.polarity
    if sentiment > 0.2:
        keywords.add("hopeful")
    elif sentiment < -0.2:
        keywords.add("tense")

    # Merge with global tags and style keywords
    combined = keywords.union(global_tags).union(STYLE_KEYWORDS)

    # Clean duplicates and formatting
    clean_keywords = " ".join(sorted(set(k.strip() for k in combined if k.strip())))
    return clean_keywords

def generate_pexels_searches(script_segments):
    global_tags = extract_global_context(script_segments)
    results = []
    for i, segment in enumerate(script_segments, 1):
        keywords = extract_segment_keywords(segment, global_tags)
        results.append((i, segment, keywords))
    return results

if __name__ == "__main__":
    # 📝 Replace these with your real script segments
    script_segments = [
        "Alex had always dreamed of reaching the top of Eagle's Peak,",
        "a mountain so tall many said it can't be climbed without years of training.",
        "But Alex wasn't an expert.",
        "Just a person with a dream and a backpack full of hope.",
        "The first steps were easy.",
        "The path was clear.",
        "But soon the trail grew steeper.",
        "Rocks blocked the way.",
        "The wind howled.",
        "Doubt crept in."
    ]

    search_results = generate_pexels_searches(script_segments)

    print("\n--- Pexels Search Keywords per Segment (Context-Aware) ---\n")
    for idx, segment, keywords in search_results:
        print(f"Segment {idx}: {segment}")
        print(f"Search Keywords: {keywords}\n")



import spacy

# Load spaCy small English model
nlp = spacy.load("en_core_web_sm")

# Your segmented script text
segments = [
    "Alex had always dreamed of reaching the top of Eagle's Peak,",
    "a mountain so tall many said it can't be climbed without years of training.",
    "But Alex wasn't an expert.",
    "Just a person with a dream and a backpack full of hope.",
    "The first steps were easy.",
    "The path was clear.",
    "But soon the trail grew steeper.",
    "Rocks blocked the way.",
    "The wind howled.",
    "Doubt crept in."
]

# Global context keywords for consistency (can be customized)
global_context = [
    "mountain", "hiking", "nature", "outdoors", "adventure", "hopeful",
    "cinematic", "golden hour", "uplifting", "warm tones"
]

def extract_keywords(text):
    doc = nlp(text.lower())
    keywords = set()
   
    # Extract nouns, proper nouns, adjectives (visual & mood clues)
    for token in doc:
        if token.pos_ in {"NOUN", "PROPN", "ADJ"} and not token.is_stop:
            keywords.add(token.lemma_)
   
    # Add some phrase replacements (e.g. "eagle's peak" -> "eagle's peak")
    if "eagle" in text.lower() and "peak" in text.lower():
        keywords.add("eagle's peak")
        keywords.discard("peak")
        keywords.discard("eagle")
   
    return keywords

# Generate keywords per segment + add global context
for i, segment in enumerate(segments, start=1):
    segment_keywords = extract_keywords(segment)
    combined_keywords = segment_keywords.union(global_context)
    # Sort and join for nice output
    keyword_string = " ".join(sorted(combined_keywords))
    print(f"Segment {i}: {segment}\nSearch Keywords: {keyword_string}\n")




That’s a great idea — you’re essentially building a **context-aware image suggestion tool** for video creation, using Pixabay and **Sentence Transformers** for semantic understanding. This can help scriptwriters and video editors find matching visuals in real-time while writing a script.

---

### 🧠 Idea Overview

You want to:

* Input: A **script** or **sentences**
* Process: Use **Sentence Transformers** to understand the meaning
* Output: Fetch **relevant images** from **Pixabay API** based on semantic similarity
* Optional: Compose a **video** automatically or semi-automatically from selected images

---

## 🏗️ System Architecture

### 1. **Input Handling**

* Take real-time or batch input of script lines.
* Tokenize or segment into sentences or phrases.

### 2. **Sentence Embedding**

* Use a pre-trained **SentenceTransformer** model like `all-MiniLM-L6-v2` to embed each sentence.

  ```python
  from sentence_transformers import SentenceTransformer
  model = SentenceTransformer('all-MiniLM-L6-v2')
  sentence_embedding = model.encode("A man walks through a forest at dusk")
  ```

### 3. **Search Pixabay with Keywords**

* Extract **semantic keywords** from sentence (e.g., via:

  * Named Entity Recognition
  * RAKE (keyword extraction)
  * KeyBERT (you can even use sentence-transformers for this)
* Use keywords to **query the Pixabay API**:

  ```python
  import requests

  def search_pixabay(api_key, query, per_page=3):
      url = f"https://pixabay.com/api/?key={api_key}&q={query}&image_type=photo&per_page={per_page}"
      response = requests.get(url)
      return response.json()['hits']
  ```

### 4. **Context Matching (Optional but Powerful)**

* For more precision, embed the **titles/descriptions** of Pixabay results and **rank** them by cosine similarity to your sentence embedding:

  ```python
  from sklearn.metrics.pairwise import cosine_similarity

  def rank_images(sentence_embedding, image_data):
      titles = [img['tags'] for img in image_data]
      title_embeddings = model.encode(titles)
      similarities = cosine_similarity([sentence_embedding], title_embeddings)[0]
      ranked = sorted(zip(image_data, similarities), key=lambda x: x[1], reverse=True)
      return [img for img, _ in ranked]
  ```

### 5. **Visual Keyboard / UI**

* Build a **keyboard-style UI** (could be web-based or an overlay in your editor) that:

  * Shows image suggestions per sentence
  * Allows quick insert or tag selection
  * Supports drag-drop into a timeline or storyboard

---

## 🔄 Optional: Video Builder

Once images are selected, you can generate a video from the script + images using tools like:

* **FFmpeg**
* **MoviePy (Python)**

```python
from moviepy.editor import ImageClip, concatenate_videoclips

def build_video(image_paths, duration_per_image=3):
    clips = [ImageClip(img).set_duration(duration_per_image) for img in image_paths]
    video = concatenate_videoclips(clips, method="compose")
    video.write_videofile("output_video.mp4", fps=24)
```

---

## 🔑 Key Tools & Libraries

| Purpose            | Tool                                            |
| ------------------ | ----------------------------------------------- |
| Sentence Embedding | `sentence-transformers`                         |
| Keyword Extraction | `KeyBERT`, `spaCy`, `RAKE`                      |
| Pixabay Search     | Pixabay REST API                                |
| Image Ranking      | `scikit-learn` cosine similarity                |
| UI                 | Web (React, Electron), or custom desktop widget |
| Video Creation     | `MoviePy`, `FFmpeg`                             |

---

## ⚡ Quick Example Flow

1. **Input Sentence**: “A child runs through a sunflower field.”
2. **Extracted Keywords**: “child”, “sunflower”, “field”
3. **Pixabay Search**: Run query with those keywords
4. **Rank**: Compare title/tags of images to sentence embedding
5. **UI**: Show top 5 images as clickable suggestions
6. **Build Video**: Export sequence with selected images

---

Would you like me to help you:

* Create a **starter script or prototype**?
* Build a **web UI concept**?
* Create a **workflow diagram**?
  Let me know how far along you are.


To use **spaCy** for turning a **script (text)** into something **visual**, like a diagram or graph of its linguistic structure, named entities, or relationships between parts of the text, you can follow these general steps:

---

### 🔧 1. **Install spaCy and Dependencies**

```bash
pip install spacy
python -m spacy download en_core_web_sm
```

Optional for visualization:

```bash
pip install spacy[lookups]  # for some visual features
```

---

### 📜 2. **Process Your Script (Text)**

```python
import spacy

# Load the English model
nlp = spacy.load("en_core_web_sm")

# Your script (or part of it)
script_text = """
John walks into the room. He looks around and sees a dusty old piano.
Suddenly, he starts playing a melancholic tune.
"""

# Process it with spaCy
doc = nlp(script_text)
```

---

### 🔍 3. **Visualize Linguistic Features**

#### Option A: **Dependency Parse Tree** (for sentence structure)

```python
from spacy import displacy

# Visualize one sentence at a time
displacy.render(doc, style="dep", jupyter=True)  # use in Jupyter Notebook

# OR serve in browser
displacy.serve(doc, style="dep")
```

---

#### Option B: **Named Entity Recognition (NER)**

```python
displacy.render(doc, style="ent", jupyter=True)

# OR serve in browser
displacy.serve(doc, style="ent")
```

This will highlight people, places, dates, etc.

---

### 🧠 4. **What Can You Visualize with spaCy?**

| Type   | What it shows                                                                            |
| ------ | ---------------------------------------------------------------------------------------- |
| `dep`  | Syntax tree (dependencies, parts of speech)                                              |
| `ent`  | Named entities (like "John", "New York", "Monday")                                       |
| Custom | You can extract relationships and visualize with tools like `networkx`, `graphviz`, etc. |

---

### 🎨 5. **Going Further – Custom Visuals**

If you want to make visuals **beyond spaCy’s built-in tools**, you can extract data and use other libraries.

#### Example: Visualizing Character Interactions in a Script

```python
import networkx as nx
import matplotlib.pyplot as plt

# Extract characters (e.g., named entities labeled as PERSON)
characters = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

# Count co-occurrence in sentences
from collections import Counter
import itertools

pairs = []
for sent in doc.sents:
    persons = [ent.text for ent in sent.ents if ent.label_ == "PERSON"]
    pairs.extend(itertools.combinations(set(persons), 2))

pair_freq = Counter(pairs)

# Create graph
G = nx.Graph()
for (p1, p2), freq in pair_freq.items():
    G.add_edge(p1, p2, weight=freq)

# Draw
plt.figure(figsize=(8, 6))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=2000, font_size=10)
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d["weight"] for u, v, d in G.edges(data=True)})
plt.title("Character Co-occurrence Graph")
plt.show()
```

---

### ✅ Summary

| Task                 | spaCy Tool                                     | Output                         |
| -------------------- | ---------------------------------------------- | ------------------------------ |
| POS tagging / syntax | `displacy.render(doc, style="dep")`            | Sentence structure             |
| Entity recognition   | `displacy.render(doc, style="ent")`            | Highlighted names, orgs, dates |
| Relationship graph   | `networkx`, `matplotlib`                       | Custom interaction graphs      |
| Export to HTML       | `displacy.render(doc, style="dep", page=True)` | Save visuals                   |

---

Would you like a specific type of visualization (like emotion arcs, scene changes, character maps)? I can tailor the code accordingly.

Great — you're looking to **create a "keyboard" or structured UI (likely a visual or interactive tool)** that helps you **search for footage** based on the **script’s content and context**.

Let's break this down and clarify what you’re aiming for, and then I’ll walk you through how to get there using **spaCy + your script + structured tagging/metadata**.

---

## 🧩 What You’re Trying to Build: A "Script Keyboard"

You want a **tool/interface** that lets you:

* Browse or search **footage (video clips)** using:

  * **Keywords** (e.g., "John enters room", "gunshot", "dark alley")
  * **Context** (e.g., **scene**, **character**, **emotion**, **location**, **action**)
* Possibly powered by NLP (spaCy), extracting entities, actions, etc.

This is often called a **semantic search keyboard** or **tag-based footage finder** — widely used in film post-production and AI-assisted editing workflows.

---

## ✅ Step-by-Step Guide

### 📁 Step 1: Parse Your Script into Structured Data

We'll extract key tags from your script using **spaCy**, and store them in a format like JSON or CSV.

```python
import spacy

nlp = spacy.load("en_core_web_sm")

script = """
INT. DARK ROOM - NIGHT

John enters cautiously. A creaking sound echoes.
He lights a match. Shadows dance on the walls.

Suddenly, a loud BANG.
"""

doc = nlp(script)

# Extract sentences and entities/actions
structured_script = []

for sent in doc.sents:
    entry = {
        "sentence": sent.text,
        "characters": [ent.text for ent in sent.ents if ent.label_ == "PERSON"],
        "locations": [ent.text for ent in sent.ents if ent.label_ in ["GPE", "LOC", "FAC"]],
        "actions": [token.lemma_ for token in sent if token.pos_ == "VERB"],
        "nouns": [token.lemma_ for token in sent if token.pos_ == "NOUN"],
        "raw": sent.text
    }
    structured_script.append(entry)
```

---

### 🧷 Step 2: Build a "Keyboard" UI with Tags

Now you turn that data into **searchable UI buttons**, such as:

```
[ John ] [ enter ] [ dark room ] [ night ] [ match ] [ bang ] [ creaking ]
```

You can do this in:

* **Python (Streamlit or Gradio)** — fast and simple
* **Web UI (HTML/JS + Flask backend)** — more flexible
* **Premiere/Resolve panels** (if targeting pro tools) — more advanced

#### Example: Streamlit App

```bash
pip install streamlit
```

```python
# app.py
import streamlit as st

# Load structured_script from earlier step

st.title("Script Keyboard - Search Footage")

# Collect unique tags
all_actions = set()
all_characters = set()
all_nouns = set()
for entry in structured_script:
    all_actions.update(entry["actions"])
    all_characters.update(entry["characters"])
    all_nouns.update(entry["nouns"])

selected_actions = st.multiselect("Actions", sorted(all_actions))
selected_characters = st.multiselect("Characters", sorted(all_characters))
selected_objects = st.multiselect("Objects/Keywords", sorted(all_nouns))

# Filter sentences
results = []
for entry in structured_script:
    if all(a in entry["actions"] for a in selected_actions) and \
       all(c in entry["characters"] for c in selected_characters) and \
       all(o in entry["nouns"] for o in selected_objects):
        results.append(entry["sentence"])

st.subheader("Matching Script Lines")
for r in results:
    st.write("- " + r)
```

Then run with:

```bash
streamlit run app.py
```

---

### 📼 Step 3: Link Script Segments to Footage

If you have your **script mapped to video clips** (e.g., timecodes or scene numbers), you can extend each entry:

```python
entry = {
    "scene_id": "Scene_5",
    "timecode": "00:05:12",
    "video_clip": "dark_room_scene.mp4",
    ...
}
```

Then you can make each result in the UI a **clickable video preview** or search link.

---

## 🔍 Optional Enhancements

| Feature              | Tool                                      |
| -------------------- | ----------------------------------------- |
| Emotion detection    | `transformers` (BERT-based sentiment)     |
| Scene classification | Use scene headings like `INT.`, `EXT.`    |
| Speaker detection    | Rule-based from dialogue blocks           |
| Searchable metadata  | Elasticsearch or vector database          |
| Visual map           | Use `displacy`, `Plotly`, or even `d3.js` |

---

## 🧠 TL;DR

To build a **context-aware script keyboard for footage search**:

1. **Use spaCy** to extract entities, verbs, nouns, locations from your script.
2. Store it as structured data (JSON/CSV).
3. Build a UI (e.g., Streamlit or Web) that allows **tag-based searching**.
4. Link results to **footage metadata** (clips, timecodes, scene numbers).
5. Optional: Enhance with sentiment, scene detection, or dialog tags.

---

Would you like me to generate a working Streamlit demo for this (with dummy video links), or help with integration into a specific platform (like DaVinci Resolve or Premiere)?


Perfect — you're asking the **right question**: *“How do I actually **build** this kind of footage-search keyboard tool from scratch?”*

Let’s break it down into **clear stages**, so you understand **what you're building**, **why it matters**, and **how it all fits together** — even if you're not an expert coder yet.

---

## 🧱 1. Core Idea: What Are You Building?

You're building a **tool that helps you search through footage using the script's content** — not just by keyword, but by **context**, like:

* **Who** is in the scene (characters)
* **What** is happening (actions)
* **Where** it's set (locations)
* **How** it feels (mood or tone)
* **When** it occurs (scene, day/night)

This is like a **smart search keyboard**, powered by the script.

---

## 📦 2. What Will You Need?

| Layer               | Tool/Tech                              | What It Does                                         |
| ------------------- | -------------------------------------- | ---------------------------------------------------- |
| 🧠 NLP Engine       | [spaCy](https://spacy.io/)             | Analyzes the script to extract people, actions, etc. |
| 🗂 Script Parser    | Python                                 | Reads your script line-by-line and pulls data out    |
| 🧰 Backend          | Python + Flask or Streamlit            | Powers the app and search logic                      |
| 🎛 UI               | Streamlit (easy) or HTML/JS (advanced) | Displays the interactive keyboard/buttons            |
| 🎥 Footage Metadata | JSON/CSV or manual mapping             | Connects scenes to actual clips or filenames         |

---

## 🛠 3. Step-by-Step Build Overview

Here’s a full breakdown:

---

### ✅ Step 1: Load & Parse Your Script

Your script might look like this:

```
INT. KITCHEN - NIGHT

Sarah enters with a knife in her hand.
John looks up from the table, startled.
```

You parse it using spaCy:

```python
import spacy

nlp = spacy.load("en_core_web_sm")

script = """
INT. KITCHEN - NIGHT

Sarah enters with a knife in her hand.
John looks up from the table, startled.
"""

doc = nlp(script)
```

---

### ✅ Step 2: Extract Keywords, Characters, and Actions

```python
structured = []

for sent in doc.sents:
    structured.append({
        "sentence": sent.text,
        "characters": [ent.text for ent in sent.ents if ent.label_ == "PERSON"],
        "actions": [token.lemma_ for token in sent if token.pos_ == "VERB"],
        "objects": [token.lemma_ for token in sent if token.pos_ == "NOUN"]
    })
```

Now you have something like this:

```json
[
  {
    "sentence": "Sarah enters with a knife in her hand.",
    "characters": ["Sarah"],
    "actions": ["enter"],
    "objects": ["knife", "hand"]
  }
]
```

---

### ✅ Step 3: Build a Searchable UI (Using Streamlit)

Install Streamlit:

```bash
pip install streamlit
```

Then write this `app.py`:

```python
import streamlit as st

# Let's pretend this is your structured data from step 2
structured = [
    {"sentence": "Sarah enters with a knife in her hand.",
     "characters": ["Sarah"],
     "actions": ["enter"],
     "objects": ["knife", "hand"]},
    
    {"sentence": "John looks up from the table, startled.",
     "characters": ["John"],
     "actions": ["look"],
     "objects": ["table"]}
]

# Collect unique tags
all_characters = sorted(set(c for line in structured for c in line['characters']))
all_actions = sorted(set(a for line in structured for a in line['actions']))
all_objects = sorted(set(o for line in structured for o in line['objects']))

st.title("Script Keyboard - Search by Tags")

# Tag filters
selected_chars = st.multiselect("Characters", all_characters)
selected_actions = st.multiselect("Actions", all_actions)
selected_objects = st.multiselect("Objects", all_objects)

# Filter logic
results = []
for line in structured:
    if all(c in line["characters"] for c in selected_chars) and \
       all(a in line["actions"] for a in selected_actions) and \
       all(o in line["objects"] for o in selected_objects):
        results.append(line["sentence"])

# Show results
st.subheader("Matching Lines")
for r in results:
    st.write("•", r)
```

Then run:

```bash
streamlit run app.py
```

✅ You now have a basic **interactive keyboard** that lets you search lines of your script by clicking on **tags** (characters, actions, objects).

---

### ✅ Step 4: Connect to Footage (Metadata Mapping)

This part depends on how your video files are stored.

You need to **map each script sentence** or **scene** to a file:

```python
# Add this to each structured entry
"video_file": "scene_4.mp4",
"timecode": "00:01:32"
```

Then in your UI, when a line appears, you can show:

```python
st.video("path/to/scene_4.mp4", start_time=92)  # start at 1:32
```

Or just show a link/button:

```python
st.markdown("[Play Scene 4](path/to/scene_4.mp4)")
```

---

## 🧠 Optional Smart Add-ons (Advanced)

| Feature                         | How                                                 |
| ------------------------------- | --------------------------------------------------- |
| Scene headings like `INT./EXT.` | Use regex or `split()`                              |
| Emotion detection               | Sentiment analysis (TextBlob or transformers)       |
| Timeline / scene order          | Assign line numbers or scene numbers                |
| Vector search                   | Use embeddings + similarity for fuzzy search        |
| Video preview thumbnails        | Extract frame from video using `OpenCV` or `ffmpeg` |

---

## 📌 Recap: You’re Building…

A tool that:

* 🧠 **Reads the script**
* 🔍 **Breaks it down into search tags**
* 🎛️ **Lets you interactively search lines**
* 📼 **Links back to actual footage**

---

Would you like:

1. A ready-to-run **starter repo** for this project?
2. Help with parsing **Final Draft (.fdx)** or PDF scripts?
3. Integration tips with your existing footage library or folder structure?

Let me know your next priority — I’ll guide you step-by-step.

Great — adding **emotion detection** to your script parsing can **enrich your footage search** by allowing you to filter scenes by **tone or mood** — for example:
🎭 *“Find all scenes where John is angry”*, or *“Search emotional moments with Sarah”.*

This is useful for **editorial decisions**, **highlight reels**, or **tagging scenes for AI-based editing tools.**

---

## 🔍 What Is Emotion Detection?

Emotion detection (also called **affective analysis**) means using NLP to identify emotions like:

* **Joy / Happiness**
* **Sadness**
* **Anger**
* **Fear**
* **Surprise**
* **Neutral**

---

## ✅ Options for Detecting Emotion from Script

| Method                                          | Tool                     | Pros               | Cons                          |
| ----------------------------------------------- | ------------------------ | ------------------ | ----------------------------- |
| 🔹 Simple Sentiment (positive/negative/neutral) | `TextBlob`, `VADER`      | Fast, light        | Not nuanced                   |
| 🔸 Emotion Classification (6+ emotions)         | HuggingFace transformers | Accurate, modern   | Slower, needs GPU or internet |
| 🧠 Fine-tuned LLM                               | OpenAI GPT, etc.         | Deep understanding | Needs API or custom model     |

---

## 🧪 Quick Option 1: VADER for Basic Sentiment (Fast)

```python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

sentence = "John slams the door and yells in rage."

score = analyzer.polarity_scores(sentence)

print(score)
# Output: {'neg': 0.582, 'neu': 0.318, 'pos': 0.1, 'compound': -0.7351}
```

You can categorize based on compound score:

```python
compound = score['compound']
if compound > 0.5:
    emotion = "Positive"
elif compound < -0.5:
    emotion = "Negative"
else:
    emotion = "Neutral"
```

---

## 🎯 Recommended Option 2: Emotion Classification Model

Use a **pre-trained model** from [Hugging Face](https://huggingface.co). Here’s a good one:

🧠 **Model:** `j-hartmann/emotion-english-distilroberta-base`
➡️ Detects: joy, anger, sadness, disgust, fear, surprise, neutral

### 🔧 Setup:

```bash
pip install transformers torch
```

### 🧪 Code:

```python
from transformers import pipeline

emotion_classifier = pipeline("text-classification", 
                              model="j-hartmann/emotion-english-distilroberta-base",
                              return_all_scores=True)

text = "John slams the door and yells in rage."

results = emotion_classifier(text)[0]

# Get top emotion
top_emotion = max(results, key=lambda x: x['score'])
print(f"Emotion: {top_emotion['label']} ({top_emotion['score']:.2f})")
```

💡 You can run this **on every sentence** in your script and store the results.

---

## 📦 Sample Structured Output

For each sentence:

```json
{
  "sentence": "John slams the door and yells in rage.",
  "characters": ["John"],
  "actions": ["slam", "yell"],
  "objects": ["door"],
  "emotion": "anger",
  "emotion_score": 0.88
}
```

---

## 🎛️ Integrate into UI

In Streamlit or your frontend, add a dropdown or filter for emotion:

```python
selected_emotion = st.selectbox("Filter by Emotion", ["All", "anger", "joy", "fear", "sadness", "surprise"])

# Filter results
for line in structured:
    if selected_emotion == "All" or line["emotion"] == selected_emotion:
        st.write(f"{line['sentence']} ({line['emotion']})")
```

---

## 🔄 Full Integration Flow

1. 🧠 Parse script with spaCy
2. 🧪 Analyze each line with emotion model
3. 🗂 Add emotion data to structured format
4. 🔍 Build tag + emotion filter in UI
5. 📼 Link to matching video clips

---

## ❓Want Help With

* Processing a full script?
* Batch tagging emotion + storing to JSON/CSV?
* Using your own emotion categories (like romantic, tense, scary)?
* Building emotion **heatmaps** across a script?

Let me know — I can generate a code snippet or tool tailored to your need.






