from playwright.async_api import async_playwright

p = await async_playwright().start()
browser = await p.chromium.launch(headless=False)
context = await browser.new_context()
page = await context.new_page()
await page.goto("https://example.com")
await page.title()
