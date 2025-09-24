import asyncio
import json
from pathlib import Path
# from sentence_transformers import SentenceTransformer, util
import os
import shutil

# from playwright.async_api import async_playwright, Playwright
from patchright.async_api import async_playwright, Playwright, Page


def handle_image(index: str):
    #  current directory
    current_dir = Path(os.path.join(os.getcwd(), "image_downloads"))
    # target directory
    target_dir = Path(os.path.join(os.getcwd(), "images"))

    for file in current_dir.iterdir():
        if file.is_file():
            new_name = f"{index}.jpg"
            new_path = target_dir / new_name  # new folder + new name
            # file.rename(new_path)
            shutil.move(str(file), str(new_path))
            print(f"Moved + renamed {file.name} → {new_path}")


async def handle_pixabay_filter(page: Page):
    try:
        # photo => div[class^="filters"] div[class^="lhs"]  div[class^="container"]:nth-child(1) > div[class^="triggerWrapper"] > button
        await (
            await page.query_selector(
                'div[class^="filters"] div[class^="lhs"]  div[class^="container"]:nth-child(1) > div[class^="triggerWrapper"] > button'
            )
        ).click()

        await asyncio.sleep(2)
        # dropdown photo click => div[class^="filters"] div[class^="lhs"]  div[class^="container"]:nth-child(1) > div[class^="dropdown"]  div[class^="dropdownMenuItem"]:nth-child(2)
        await (
            await page.query_selector(
                'div[class^="filters"] div[class^="lhs"]  div[class^="container"]:nth-child(1) > div[class^="dropdown"]  div[class^="dropdownMenuItem"]:nth-child(2)'
            )
        ).click()
        await asyncio.sleep(2)
        # horizontal => div[class^="filters"] div[class^="lhs"]  div[class^="container"]:nth-child(2) > div[class^="triggerWrapper"] >button
        await (
            await page.query_selector(
                'div[class^="filters"] div[class^="lhs"]  div[class^="container"]:nth-child(2) > div[class^="triggerWrapper"] >button'
            )
        ).click()
        await asyncio.sleep(2)
        # div[class^="filters"] div[class^="lhs"]  div[class^="container"]:nth-child(2) > div[class^="dropdown"]  div[class^="dropdownMenuItem"]:nth-child(2)
        await (
            await page.query_selector(
                'div[class^="filters"] div[class^="lhs"]  div[class^="container"]:nth-child(2) > div[class^="dropdown"]  div[class^="dropdownMenuItem"]:nth-child(2)'
            )
        ).click()
        await asyncio.sleep(2)
        # authencity => div[class^="filters"] div[class^="lhs"]  div[class^="container"]:nth-child(6) > div[class^="triggerWrapper"] >button
        await (
            await page.query_selector(
                'div[class^="filters"] div[class^="lhs"]  div[class^="container"]:nth-child(6) > div[class^="triggerWrapper"] >button'
            )
        ).click()
        await asyncio.sleep(2)
        # div[class^="filters"] div[class^="lhs"]  div[class^="container"]:nth-child(6) > div[class^="dropdown"]  div[class^="dropdownMenuItem"]:nth-child(2)
        await (
            await page.query_selector(
                'div[class^="filters"] div[class^="lhs"]  div[class^="container"]:nth-child(6) > div[class^="dropdown"]  div[class^="dropdownMenuItem"]:nth-child(2)'
            )
        ).click()
        await asyncio.sleep(2)
    except Exception as e:
        print(e)


async def run(playwright: Playwright):
    current_directory = os.getcwd()
    parent_directory = os.path.dirname(current_directory)
    print(f"Parent of current working directory: {parent_directory}")
    chromium = playwright.chromium  # or "firefox" or "webkit".
    browser = await chromium.launch_persistent_context(
        user_data_dir=os.path.join(parent_directory,'deepak'),
        channel="chrome",
        headless=False,
    )

    
    with open(os.path.join(current_directory,'common-example','output.json'), "r", encoding="utf-8") as f:
        transcription = json.load(f)

    segments = transcription["segments"]

    for segment in segments:
        page = await browser.new_page()
        await page.goto("https://pixabay.com/")
        await asyncio.sleep(2)
        await (await page.query_selector(selector="input[type='search']")).fill(
            segment["image_suggestion"][0]
        )
        await page.evaluate(
            expression="""()=>{
                
                    // Create a new KeyboardEvent for Enter
                    var enterEvent = new KeyboardEvent('keydown', {
                        key: 'Enter',
                        code: 'Enter',
                        keyCode: 13,
                        which: 13,
                        bubbles: true
                    });

                    // Dispatch the event on the currently focused element
                    document.activeElement.dispatchEvent(enterEvent);      
                    } """
        )
        await asyncio.sleep(3)

        await handle_pixabay_filter(page)

        images = await page.query_selector_all(
            'div[class^="results"] div[class^="verticalMasonry"] script[type="application/ld+json"]'
        )
        for image in images:
            img = json.loads(await image.text_content())
            print(img["contentUrl"])

        await page.close()

        # await asyncio.sleep(5000)
    # other actions...
    await browser.close()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)


if __name__ == "__main__":
    # print(segments)
    asyncio.run(main())
