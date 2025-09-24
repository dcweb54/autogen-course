Awesome! You’re about to build a powerful **AI-powered video editing pipeline** that:

---

## 🎞️ Automates Video Creation with:

1. **Script analysis** → keywords + sentiment/emotion
2. **Fetches stock footage** from Pexels
3. **Fetches background music** from **Freesound** by emotion
4. **Downloads everything**
5. **Edits video using `ffmpeg`**:

   * Assembles clips into a timeline
   * Adds background music

---

## 🛠️ What We’ll Use

| Task                         | Tool                                       |
| ---------------------------- | ------------------------------------------ |
| Sentiment & emotion analysis | HuggingFace Transformers                   |
| Video search                 | Pexels API                                 |
| Music search                 | Freesound API                              |
| Video & audio editing        | `ffmpeg` (Python wrapper: `ffmpeg-python`) |
| Download files               | `requests`                                 |
| File management              | `os`, `shutil`, `uuid`                     |

---

### ✅ STEP 1: Install Dependencies

```bash
pip install transformers torch requests ffmpeg-python
```

You'll also need:

* `ffmpeg` installed on your system (accessible in PATH): [Download](https://ffmpeg.org/download.html)
* A **Freesound API key**: [https://freesound.org/docs/api/](https://freesound.org/docs/api/)

---

### ✅ STEP 2: Full Pipeline Script (with Download + Edit)

Here’s the full **Python script**, with comments to walk you through each part.

> ⚠️ Replace both API keys before running:

```python
PEXELS_API_KEY = "YOUR_PEXELS_API_KEY"
FREESOUND_API_KEY = "YOUR_FREESOUND_API_KEY"
```

```python
import os
import uuid
import requests
import shutil
import ffmpeg
from transformers import pipeline

# -----------------------
# CONFIGURATION
# -----------------------
PEXELS_API_KEY = "YOUR_PEXELS_API_KEY"
FREESOUND_API_KEY = "YOUR_FREESOUND_API_KEY"

VIDEO_OUTPUT = "final_video.mp4"
TEMP_DIR = "temp_assets"
os.makedirs(TEMP_DIR, exist_ok=True)

# -----------------------
# LOAD TRANSFORMERS
# -----------------------
sentiment_model = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")
emotion_model = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)

# -----------------------
# ANALYZE SCRIPT
# -----------------------
def analyze_script(script, top_n_emotions=2):
    sentiment = sentiment_model(script)[0]['label'].lower()
    emotions = sorted(
        emotion_model(script)[0], key=lambda x: x['score'], reverse=True
    )[:top_n_emotions]
    emotion_labels = [e['label'].lower() for e in emotions]

    sentiment_keywords = {
        'positive': ['sunlight', 'joyful', 'happy', 'bright', 'peaceful'],
        'negative': ['sad', 'cold', 'rain', 'lonely'],
        'neutral': ['nature', 'city', 'street']
    }

    emotion_keywords = {
        'joy': ['celebration', 'laughing', 'kids playing'],
        'calmness': ['serene', 'still lake', 'relaxing'],
        'sadness': ['rainy', 'isolation', 'grey sky'],
        'anger': ['conflict', 'storm'],
        'fear': ['dark', 'tension'],
        'excitement': ['festival', 'concert', 'sports'],
        'love': ['romantic', 'hug', 'wedding'],
    }

    keywords = sentiment_keywords.get(sentiment, [])
    for emotion in emotion_labels:
        keywords += emotion_keywords.get(emotion, [])

    keywords = list(dict.fromkeys(keywords))  # remove duplicates
    return sentiment, emotion_labels, keywords

# -----------------------
# FETCH VIDEOS FROM PEXELS
# -----------------------
def fetch_videos(keywords, max_results=3):
    query = " ".join(keywords[:5])
    url = "https://api.pexels.com/videos/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": max_results}
    r = requests.get(url, headers=headers, params=params)
    r.raise_for_status()
    videos = r.json().get("videos", [])
    return [v["video_files"][0]["link"] for v in videos]

# -----------------------
# FETCH AUDIO FROM FREESOUND
# -----------------------
def fetch_music(emotion):
    url = f"https://freesound.org/apiv2/search/text/"
    headers = {"Authorization": f"Token {FREESOUND_API_KEY}"}
    params = {
        "query": emotion,
        "filter": "duration:[10 TO 120]",
        "sort": "score",
        "fields": "id,name,previews",
        "page_size": 1
    }
    r = requests.get(url, headers=headers, params=params)
    r.raise_for_status()
    results = r.json().get("results", [])
    if results:
        return results[0]['previews']['preview-hq-mp3']
    return None

# -----------------------
# DOWNLOAD FILE
# -----------------------
def download_file(url, dest_folder, prefix):
    filename = f"{prefix}_{uuid.uuid4().hex[:8]}.mp4" if "video" in prefix else f"{prefix}_{uuid.uuid4().hex[:8]}.mp3"
    path = os.path.join(dest_folder, filename)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(path, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    return path

# -----------------------
# ASSEMBLE VIDEO WITH FFMPEG
# -----------------------
def create_final_video(video_paths, audio_path, output_path):
    input_list_path = os.path.join(TEMP_DIR, "input.txt")
    with open(input_list_path, "w") as f:
        for path in video_paths:
            f.write(f"file '{os.path.abspath(path)}'\n")

    concat_output = os.path.join(TEMP_DIR, "combined.mp4")

    # Step 1: Concatenate videos
    ffmpeg.input(input_list_path, format='concat', safe=0).output(concat_output, c='copy').run(overwrite_output=True)

    # Step 2: Add background music (looped if needed)
    ffmpeg.input(concat_output).output(audio_path, t=0).run(overwrite_output=True)  # Ensure music duration if needed
    final = ffmpeg.input(concat_output).audio_filter('volume=0.9').output(
        output_path, vf='format=yuv420p', audio=ffmpeg.input(audio_path), shortest=None
    )
    final.run(overwrite_output=True)

# -----------------------
# MAIN WORKFLOW
# -----------------------
def run_full_pipeline(script):
    print("🔍 Analyzing script...")
    sentiment, emotions, keywords = analyze_script(script)
    print("✅ Sentiment:", sentiment)
    print("✅ Emotions:", emotions)
    print("✅ Keywords:", keywords)

    print("\n🎬 Fetching stock videos...")
    video_urls = fetch_videos(keywords)
    video_paths = [download_file(url, TEMP_DIR, "video") for url in video_urls]
    print(f"✅ Downloaded {len(video_paths)} video(s).")

    print("\n🎵 Fetching background music...")
    music_url = fetch_music(emotions[0]) if emotions else None
    if not music_url:
        print("❌ No background music found.")
        return
    audio_path = download_file(music_url, TEMP_DIR, "music")
    print("✅ Background music downloaded.")

    print("\n🛠️ Assembling final video...")
    create_final_video(video_paths, audio_path, VIDEO_OUTPUT)
    print(f"\n✅ Final video created: {VIDEO_OUTPUT}")

# -----------------------
# EXAMPLE USAGE
# -----------------------
if __name__ == "__main__":
    sample_script = """
    The golden sunlight filtered through the trees, birds chirped melodiously, and a gentle breeze carried the scent of wildflowers.
    Everything felt calm and alive.
    """
    run_full_pipeline(sample_script)
```

---

## ✅ Output

After running the script, you’ll get:

* A fully edited video file: `final_video.mp4`
* With clips that match the **script tone**
* With background music that fits the **emotion**

---

## 🎯 Optional Improvements

* Add **subtitles** from the script using `ffmpeg drawtext`
* Fade transitions using `ffmpeg` filters
* Match **clip durations** to music beat
* Add **voiceover narration** using `TTS` (e.g., ElevenLabs, Google TTS)

---

## 🧠 Want this as a Web App or GUI?

I can turn this into:

* A **Streamlit web app**
* A **drag-and-drop GUI**
* A **desktop tool** with export options

Just say the word.

Let me know if you want:

* 🖼️ Video thumbnails preview
* 🎙️ Voiceover support
* 💾 Editable timeline builder

How far do you want to take this?
