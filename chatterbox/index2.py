# app.py
import os
import random
import numpy as np
import torch
from typing import Any
import mesop as me
import mesop.labs as mel

# Import your TTS model (make sure src is in PYTHONPATH)
from src.chatterbox.mtl_tts import ChatterboxMultilingualTTS, SUPPORTED_LANGUAGES

# ----------------------------
# Global state and model
# ----------------------------

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

MODEL = None

def get_or_load_model():
  global MODEL
  if MODEL is None:
    # Patch torch.load to load on CPU first
    original_load = torch.load
    def patched_load(*args, **kwargs):
      kwargs["map_location"] = "cpu"
      return original_load(*args, **kwargs)
    torch.load = patched_load
    MODEL = ChatterboxMultilingualTTS.from_pretrained(DEVICE)
    torch.load = original_load
    if hasattr(MODEL, "to"):
      MODEL.to(DEVICE)
  return MODEL

def set_seed(seed: int):
  torch.manual_seed(seed)
  if DEVICE == "cuda":
    torch.cuda.manual_seed_all(seed)
  random.seed(seed)
  np.random.seed(seed)

def chunk_text(text: str, max_len: int = 300) -> list[str]:
  import re
  sentences = re.split(r"(?<=[.!?]) +", text)
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

# ----------------------------
# Mesop State
# ----------------------------

@me.stateclass
class State:
  language: str = "en"
  text: str = "Last month, we reached a new milestone with two billion views."
  exaggeration: float = 0.5
  temperature: float = 0.8
  cfg_weight: float = 0.5
  seed: int = 0
  ref_audio: mel.UploadedFile | None = None
  audio_url: str = ""
  is_generating: bool = False
  error: str = ""

# ----------------------------
# Event Handlers
# ----------------------------

def on_generate_click(e: me.ClickEvent):
  state = me.state(State)
  state.is_generating = True
  state.error = ""
  me.navigate("/generating")  # Optional: show loading page
  yield

  try:
    model = get_or_load_model()

    if state.seed != 0:
      set_seed(state.seed)

    # Save uploaded reference audio
    ref_path = None
    if state.ref_audio:
      ref_path = "/tmp/ref_audio." + (state.ref_audio.name.split(".")[-1] or "wav")
      with open(ref_path, "wb") as f:
        f.write(state.ref_audio.getvalue())

    # Generate audio
    chunks = chunk_text(state.text)
    audio_parts = []

    for chunk in chunks:
      wav = model.generate(
        chunk,
        language_id=state.language,
        exaggeration=state.exaggeration,
        temperature=state.temperature,
        cfg_weight=state.cfg_weight,
        audio_prompt_path=ref_path,
      )
      audio_parts.append(wav.squeeze(0).cpu().numpy())

    final_audio = np.concatenate(audio_parts)

    # Save to /tmp and serve via Mesop
    audio_path = "/tmp/generated.wav"
    from scipy.io.wavfile import write
    write(audio_path, model.sr, final_audio)

    # Read back as bytes and encode
    with open(audio_path, "rb") as f:
      audio_bytes = f.read()
    state.audio_url = f"data:audio/wav;base64,{me.base64_encode(audio_bytes)}"
    me.navigate("/result")

  except Exception as ex:
    state.error = str(ex)
    print("Generation error:", ex)
  finally:
    state.is_generating = False
    yield

def on_file_upload(e: mel.FileUploadEvent):
  state = me.state(State)
  state.ref_audio = e.file

# ----------------------------
# Pages
# ----------------------------

@me.page(path="/", title="🗣️ Chatterbox TTS")
def main_page():
  state = me.state(State)

  with me.box(style=me.Style(padding=me.Padding.all(16), max_width=800, margin=me.Margin.symmetric(horizontal="auto"))):
    me.text("🗣️ Chatterbox Multilingual TTS", type="headline-5", style=me.Style(margin=me.Margin(bottom=24)))

    # Language
    me.select(
      label="Language",
      options=[me.SelectOption(label=SUPPORTED_LANGUAGES[lang], value=lang) for lang in SUPPORTED_LANGUAGES],
      on_selection_change=lambda e: setattr(me.state(State), 'language', e.value),
      value=state.language,
    )

    # Text input
    me.textarea(
      label="Text to speak",
      rows=4,
      on_input=lambda e: setattr(me.state(State), 'text', e.value),
      value=state.text,
    )

    # Reference audio
    mel.file_upload(
      label="Upload reference audio (.wav, .flac)",
      accepted_file_types=[".wav", ".flac"],
      on_upload=on_file_upload,
    )

    # Sliders
    me.slider(
      label="Exaggeration",
      min=0.25,
      max=2.0,
      step=0.05,
      value=state.exaggeration,
      on_value_change=lambda e: setattr(me.state(State), 'exaggeration', e.value),
    )
    me.slider(
      label="Temperature",
      min=0.05,
      max=5.0,
      step=0.05,
      value=state.temperature,
      on_value_change=lambda e: setattr(me.state(State), 'temperature', e.value),
    )
    me.slider(
      label="CFG / Pace",
      min=0.2,
      max=1.0,
      step=0.05,
      value=state.cfg_weight,
      on_value_change=lambda e: setattr(me.state(State), 'cfg_weight', e.value),
    )

    # Seed
    me.input(
      label="Seed (0 = random)",
      value=str(state.seed),
      type="number",
      on_input=lambda e: setattr(me.state(State), 'seed', int(e.value) if e.value.isdigit() else 0),
    )

    # Generate button
    me.button(
      "🎤 Generate Speech",
      on_click=on_generate_click,
      disabled=state.is_generating,
      style=me.Style(margin=me.Margin(top=24)),
    )

    # Error display
    if state.error:
      me.text(f"❌ Error: {state.error}", style=me.Style(color="red", margin=me.Margin(top=16)))

@me.page(path="/result", title="✅ Result")
def result_page():
  state = me.state(State)

  with me.box(style=me.Style(padding=me.Padding.all(16), max_width=800, margin=me.Margin.symmetric(horizontal="auto"))):
    me.text("✅ Generated Speech", type="headline-5")
    if state.audio_url:
      me.audio(src=state.audio_url, controls=True)
    me.button("← Back", on_click=lambda e: me.navigate("/"), style=me.Style(margin=me.Margin(top=24)))

# Optional: loading page
@me.page(path="/generating", title="⏳ Generating...")
def generating_page():
  with me.box(style=me.Style(padding=me.Padding.all(16), text_align="center")):
    me.text("Generating speech...", type="headline-6")
    me.progress_spinner()

# ----------------------------
# Run with: mesop run app.py
# ----------------------------