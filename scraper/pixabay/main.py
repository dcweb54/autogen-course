from patchright.async_api import async_playwright, Playwright, Page
from pixabay_scraper import PixabayScraper
from visual_image_downloader import VisualImageDownloader
import os
import asyncio


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
    
    # page = await browser.new_page()
    
    # visual = VisualImageDownloader(browser=browser)
    
    # await visual.transcript_path(path='output.json')
    
    pixabay = PixabayScraper(browser=browser,curr_dir=parent_directory)
    # await pixabay.open_page()
    # await asyncio.sleep(3)
    await pixabay.search("big mountain")

    await asyncio.sleep(5)
    # await pixabay.filter()
    result = await pixabay.result()
    
    
    await asyncio.sleep(1000)
    # print(result)


async def main():
    async with async_playwright() as playwright:
        await run(playwright)


if __name__ == "__main__":
    print("start scraping")
    asyncio.run(main())
