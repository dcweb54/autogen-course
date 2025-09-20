# import re
# def extract_url(text):
#     match = re.search(r'https?://[^\s]+', text)
#     return match.group(0) if match else None

# logs = ['t3_23lang.safetensors:  97% 2.09G/2.14G [00:18<00:00, 233MB/s]', '', 't3_23lang.safetensors:  99% 2.12G/2.14G [00:18<00:00, 241MB/s]', '', 't3_23lang.safetensors: 100% 2.14G/2.14G [00:18<00:00, 115MB/s]', 'Fetching 6 files: 100% 6/6 [00:18<00:00,  3.14s/it]', '/usr/local/lib/python3.12/dist-packages/diffusers/models/lora.py:393: FutureWarning: `LoRACompatibleLinear` is deprecated and will be removed in version 1.0.0. Use of `LoRACompatibleLinear` is deprecated. Please switch to PEFT backend by installing PEFT: `pip install peft`.', '  deprecate("LoRACompatibleLinear", "1.0.0", deprecation_message)', 'Cangjie5_TC.json: 1.92MB [00:00, 4.87MB/s]', 'WARNING:src.chatterbox.models.tokenizers.tokenizer:pkuseg not available - Chinese segmentation will be skipped', 'loaded PerthNet (Implicit) at step 250,000', 'Model loaded successfully. Internal device: cuda', '* Running on local URL:  http://127.0.0.1:7860', '* Running on public URL: https://2aef41db01a16f3802.gradio.live', '', 'This share link expires in 1 week. For free permanent hosting and GPU upgrades, run `gradio deploy` from the terminal in the working directory to deploy to Hugging Face Spaces (https://huggingface.co/spaces)', 'Keyboard interruption in main thread... closing server.', '^C']

# for log in logs:
#     if "Running on public URL" in log:
#         print(extract_url(log))

# import time

# max_try_connection = 3

# while True:
#     if max_try_connection == 0:
#         print(f"max connection {max_try_connection} ")
#         break
#     else:
#         print(f"current {max_try_connection}")
#     time.sleep(5)
#     max_try_connection -= 1

# import asyncio

# print("welcome")
# await asyncio.sleep(20)
# await asyncio.sleep(2)
# print("marketing")
# await asyncio.sleep(2)
# print("currency")
# await asyncio.sleep(2)
# print("power")
     
     
# dummy_text = """
#  welcome
# marketing
# currency
# power

# """

# print(dummy_text.strip().split("\n"))

from playwright.async_api import async_playwright,Playwright
import asyncio

async def run(playwright:Playwright):
    browser = await playwright.chromium.launch(headless=False)
    page = await browser.new_page()
    await page.goto("https://example.com")
    print(await page.title())
    # await browser.close()

async def main():
    playwright = await async_playwright().start()   # ✅ manual start
    try:
        await run(playwright)
    finally:
        print("close the brose")
        await playwright.stop()                     # ✅ manual stop

asyncio.run(main())
