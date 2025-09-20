from patchright.async_api import async_playwright, Playwright
import asyncio
from colab_page import ColabPage
from gradio_client import Client, handle_file


async def run(playwright: Playwright):
    
    chromium = playwright.chromium  # or "firefox" or "webkit".
    browser = await chromium.launch_persistent_context(
        user_data_dir="tmp/deepak",
        channel="chrome",
        headless=False,
    )

    page = await browser.new_page()
    await page.goto(
        "https://colab.research.google.com/drive/1mC9z9XcH3XfqTY8q7bZZLxwZT3hVmh1E"
    )
    
    
    
    colab_page = ColabPage(page)
    await asyncio.sleep(3)
    url = await colab_page.handle_page_v2()
    await asyncio.sleep(3)
    if url is not None:
        print(f"final url {url}")
        await asyncio.sleep(3)
    
    # page = await browser.new_page()    # ✅ opens a new tab
    # await page.goto("https://github.com")
    # print("🌍 Opened GitHub in a new tab")
    
    
    # page = await browser.new_page()    # ✅ opens a new tab
    # await page.goto(url)
    # print("🌍 Opened Gradio live in a new tab")
    

    # client = Client(url)
    
    # result = client.predict(
    #     lang="hi",
    #     current_ref=handle_file('https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/hi_f1.flac'),
    #     current_text="पिछले महीने हमने एक नया मील का पत्थर छुआ: हमारे YouTube चैनल पर दो अरब व्यूज़।  पिछले महीने हमने एक नया मील का पत्थर छुआ: हमारे YouTube चैनल पर दो अरब व्यूज़।",
    #     api_name="/on_language_change"
    # )

    # print(result)
    
    await asyncio.sleep(9999)


async def main():
    async with async_playwright() as playwright:
        await run(playwright)


if __name__ == "__main__":
    # print(segments)
    asyncio.run(main())
