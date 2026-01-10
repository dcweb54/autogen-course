from patchright.async_api import async_playwright, Playwright
import asyncio
from colab_page import ColabPage
from gradio_client import Client, handle_file
import os


async def run(playwright: Playwright):
    current_directory = os.getcwd()
    parent_directory = os.path.dirname(current_directory)
    print(f"Parent of current working directory: {parent_directory}")
    chromium = playwright.chromium  # or "firefox" or "webkit".
    browser = await chromium.launch_persistent_context(
        user_data_dir=os.path.join(parent_directory, "deepak"),
        channel="chrome",
        headless=False,
    )

    page = await browser.new_page()
    await page.goto(
        "https://colab.research.google.com/drive/1mC9z9XcH3XfqTY8q7bZZLxwZT3hVmh1E"
    )

    # await asyncio.sleep(20000)
    colab_page = ColabPage(page)
    await asyncio.sleep(1000)
    url = await colab_page.handle_page_v2()
    await asyncio.sleep(3)
    if url is not None:
        print(f"final url {url}")
        text_to_audio_example(url=url)
        await asyncio.sleep(3)

    # page = await browser.new_page()    # ✅ opens a new tab
    # await page.goto("https://github.com")
    # print("🌍 Opened GitHub in a new tab")

    # page = await browser.new_page()    # ✅ opens a new tab
    # await page.goto(url)
    # print("🌍 Opened Gradio live in a new tab")

    await asyncio.sleep(9999)


def text_to_audio_example(url: str):
    current_audio_file = os.path.join(
        os.getcwd(), "text-to-audio-use-cases", "audio-hindi.wav"
    )
    client = Client(url)
    result = client.predict(
        text_input="पिछले महीने हमने एक नया मील का पत्थर छुआ: हमारे YouTube चैनल पर दो",
        language_id="hi",
        audio_prompt_path_input=handle_file(current_audio_file),
        exaggeration_input=0.5,
        temperature_input=0.8,
        seed_num_input=0,
        cfgw_input=0.5,
        api_name="/generate_tts_audio",
    )

    print(result)


async def main():
    async with async_playwright() as playwright:
        await run(playwright)


if __name__ == "__main__":
    # print(segments)
    asyncio.run(main())
