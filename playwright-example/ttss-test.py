from typing import Dict, Any, Optional, Tuple
import requests


class GradioClientError(Exception):
    """Custom exception for GradioClient errors."""


def call_on_language_change(
    base_url: str,
    lang_code: str,
    file_url: str,
    text: str,
    timeout: int = 30,
) -> Tuple[str, Optional[Dict[str, Any]]]:
    """
    Call the Gradio API `on_language_change` endpoint.

    Args:
        base_url (str): The base Gradio URL (e.g., "https://72f15a55a104fca03a.gradio.live").
        lang_code (str): Language code (e.g., "ar").
        file_url (str): URL to the audio file.
        text (str): Text input for the model.
        timeout (int): Timeout in seconds for the request.

    Returns:
        Tuple[str, Optional[Dict[str, Any]]]:
            - Event ID string
            - Event response JSON if available, else None
    """
    try:
        endpoint = f"{base_url}/gradio_api/call/on_language_change"

        payload = {
            "data": [
                lang_code,
                {"path": file_url, "meta": {"_type": "gradio.FileData"}},
                text,
            ]
        }

        headers = {"Content-Type": "application/json"}

        # First request to get EVENT_ID
        response = requests.post(endpoint, json=payload, headers=headers, timeout=timeout)
        response.raise_for_status()

        json_data = response.json()
        event_id = json_data.get("event_id") or json_data.get("data") or None

        if not event_id:
            raise GradioClientError("Could not extract event_id from response")

        # Second request: stream results
        stream_url = f"{endpoint}/{event_id}"
        stream_resp = requests.get(stream_url, stream=True, timeout=timeout)
        stream_resp.raise_for_status()

        # Collect output
        output_data = None
        for line in stream_resp.iter_lines():
            if line:
                try:
                    output_data = line.decode("utf-8")
                except UnicodeDecodeError:
                    continue

        return str(event_id), {"output": output_data}

    except (requests.RequestException, ValueError) as e:
        raise GradioClientError(f"Request failed: {e}") from e


if __name__ == "__main__":
    BASE_URL = "https://075da5c745641c498d.gradio.live"
    LANG = "ar"
    FILE_URL = "https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav"
    TEXT = "Hello!!"

    try:
        event_id, result = call_on_language_change(BASE_URL, LANG, FILE_URL, TEXT)
        print(f"✅ Event ID: {event_id}")
        print(f"📦 Result: {result}")
    except GradioClientError as e:
        print(f"❌ Error: {e}")
