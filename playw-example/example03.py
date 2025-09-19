import asyncio
import csv
from openpyxl import Workbook
from playwright.async_api import async_playwright


async def scrape_hackernews():
    async with async_playwright() as p:
        # Launch headless browser
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        print("Navigating to Hacker News...")
        await page.goto("https://news.ycombinator.com/")

        # Wait until articles are loaded
        await page.wait_for_selector("td:nth-child(3) > span > a")

        # Extract titles & links
        items = await page.query_selector_all("td:nth-child(3) > span > a")
        results = []
        for item in items:
            title = await item.inner_text()
            link = await item.get_attribute("href")
            results.append((title, link))
            
        
        await asyncio.sleep(200)

        await browser.close()
        return results


async def main():
    data = await scrape_hackernews()

    # Save to CSV
    # with open("hackernews.csv", "w", newline="", encoding="utf-8") as f:
    #     writer = csv.writer(f)
    #     writer.writerow(["Title", "Link"])
    #     writer.writerows(data)
    # print("✅ Data saved to hackernews.csv")

    # Save to Excel
    wb = Workbook()
    ws = wb.active
    ws.append(["Title", "Link"])
    for row in data:
        ws.append(row)
    wb.save("hackernews.xlsx")
    print("✅ Data saved to hackernews.xlsx")


if __name__ == "__main__":
    asyncio.run(main())
