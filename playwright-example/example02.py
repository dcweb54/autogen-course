import asyncio
from playwright.async_api import Playwright, async_playwright, expect


async def run(playwright: Playwright) -> None:
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()
    
    await page.goto("https://playwright.dev/")
    await page.get_by_role("link", name="Docs").click()
    await page.get_by_role("link", name="Generating tests").click()
    await page.get_by_role("link", name="Setting up CI").click()
    await page.get_by_text("Playwright tests can be run").click()
    # await expect(page.get_by_role("article")).to_contain_text("Playwright tests can be run on any CI provider. This guide covers one way of running tests on GitHub using GitHub Actions. If you would like to learn more, or how to configure other CI providers, check out our detailed doc on Continuous Integration.")
    print(await page.get_by_role('article').text_content())
    
    await expect(page.get_by_text("Playwright tests can be run")).to_be_visible()
    await page.get_by_role("button", name="Node.js").click()
    await page.get_by_role("link", name="Java", exact=True).click()
    await page.get_by_role("link", name="Videos", exact=True).click()
    await page.get_by_text("With Playwright you can").click()

    # ---------------------
    await context.close()
    await browser.close()


async def main() -> None:
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())
