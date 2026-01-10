import os
import random
import numpy as np
import torch
import mesop as mp

from src.chatterbox.mtl_tts import (
    ChatterboxMultilingualTTS,
    SUPPORTED_LANGUAGES,
)

# -----------------------------
# Device
# -----------------------------
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🚀 Running on device: {DEVICE}")

# -----------------------------
# Model loading (CPU-safe)
# -----------------------------
MODEL = None
_original_torch_load = torch.load

def _patched_torch_load(f, map_location=None, **kwargs):
    return _original_torch_load(f, map_location="cpu", **kwargs)

def get_or_load_model():
    global MODEL
    if MODEL is None:
        torch.load = _patched_torch_load
        MODEL = ChatterboxMultilingualTTS.from_pretrained(DEVICE)
        torch.load = _original_torch_load
        if hasattr(MODEL, "to"):
            MODEL.to(DEVICE)
        print("✅ Model loaded")
    return MODEL


# -----------------------------
# Helpers
# -----------------------------
def set_seed(seed):
    torch.manual_seed(seed)
    if DEVICE == "cuda":
        torch.cuda.manual_seed_all(seed)
    random.seed(seed)
    np.random.seed(seed)

def chunk_text(text, max_len=300):
    import re
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks, current = [], ""
    for s in sentences:
        if len(current) + len(s) <= max_len:
            current += " " + s
        else:
            chunks.append(current.strip())
            current = s
    if current:
        chunks.append(current.strip())
    return chunks


# -----------------------------
# Defaults
# -----------------------------
LANGUAGE_CONFIG = {
    "en": {
        "text": "Last month, we reached a new milestone with two billion views."
    },
    "fr": {
        "text": "Le mois dernier, nous avons atteint un nouveau jalon."
    }
}


# -----------------------------
# Mesop State
# -----------------------------
@mp.state
class AppState:
    language: str = "en"
    text: str = LANGUAGE_CONFIG["en"]["text"]
    exaggeration: float = 0.5
    temperature: float = 0.8
    cfg_weight: float = 0.5
    seed: int = 0
    status: str = "Idle"
    progress: int = 0
    audio: np.ndarray | None = None
    sample_rate: int = 24000
    ref_audio_path: str | None = None


# -----------------------------
# Actions
# -----------------------------
def on_language_change(state: AppState, value: str):
    state.language = value
    state.text = LANGUAGE_CONFIG.get(value, {}).get("text", "")

def on_file_upload(state: AppState, files):
    if not files:
        state.ref_audio_path = None
        return

    file = files[0]
    path = "/content/ref_audio.wav"
    with open(path, "wb") as f:
        f.write(file["content"])
    state.ref_audio_path = path

def generate_speech(state: AppState):
    state.status = "Loading model..."
    state.progress = 5

    model = get_or_load_model()

    if state.seed != 0:
        set_seed(state.seed)

    chunks = chunk_text(state.text)
    audio_parts = []

    state.status = "Generating audio..."
    state.progress = 10

    for i, chunk in enumerate(chunks):
        wav = model.generate(
            chunk,
            language_id=state.language,
            exaggeration=state.exaggeration,
            temperature=state.temperature,
            cfg_weight=state.cfg_weight,
            audio_prompt_path=state.ref_audio_path,
        )

        audio_parts.append(wav.squeeze(0).cpu().numpy())
        state.progress = 10 + int(((i + 1) / len(chunks)) * 80)

    state.audio = np.concatenate(audio_parts)
    state.sample_rate = model.sr
    state.progress = 100
    state.status = "Done ✅"


# -----------------------------
# UI
# -----------------------------
@mp.app
def app(state: AppState):
    mp.heading("🗣️ Chatterbox Multilingual TTS", level=2)

    mp.text(f"🚀 Device: {DEVICE}")

    mp.select(
        label="Language",
        value=state.language,
        options=[(v, k) for k, v in SUPPORTED_LANGUAGES.items()],
        on_change=on_language_change,
    )

    mp.textarea(
        label="Text",
        value=state.text,
        rows=6,
        on_change=lambda s, v: setattr(s, "text", v),
    )

    mp.file_upload(
        label="Reference Audio (.wav / .flac)",
        accept=[".wav", ".flac"],
        multiple=False,
        on_upload=on_file_upload,
    )

    mp.slider(
        label="Exaggeration",
        value=state.exaggeration,
        min=0.25,
        max=2.0,
        step=0.05,
        on_change=lambda s, v: setattr(s, "exaggeration", v),
    )

    mp.slider(
        label="Temperature",
        value=state.temperature,
        min=0.05,
        max=5.0,
        step=0.05,
        on_change=lambda s, v: setattr(s, "temperature", v),
    )

    mp.slider(
        label="CFG / Pace",
        value=state.cfg_weight,
        min=0.2,
        max=1.0,
        step=0.05,
        on_change=lambda s, v: setattr(s, "cfg_weight", v),
    )

    mp.number(
        label="Seed (0 = random)",
        value=state.seed,
        on_change=lambda s, v: setattr(s, "seed", int(v)),
    )

    mp.button(
        "🎤 Generate Speech",
        on_click=generate_speech,
        type="primary",
    )

    mp.divider()

    mp.text(f"Status: {state.status}")
    mp.progress(state.progress)

    if state.audio is not None:
        mp.audio(state.audio, sample_rate=state.sample_rate)


# -----------------------------
# Launch inside Colab
# -----------------------------
mp.run()
