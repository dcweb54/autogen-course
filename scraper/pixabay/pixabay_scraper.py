from patchright.async_api import async_playwright, Playwright, Page, BrowserContext,Response
import asyncio
import json
from pathlib import Path
import os

class PixabayScraper:
    def __init__(self, browser: BrowserContext,curr_dir:str):
        self.browser = browser
        self.curr_dir = curr_dir

    async def open_page(self):
        # https://pixabay.com/photos/search/mountain/?content_type=authentic&orientation=horizontal
        await self.page.goto("https://pixabay.com/")
        
    async def download_photo_response(self,response:Response):
        url = response.url
        if url.startswith('https://cdn.pixabay.com/photo') and url.endswith("1280.jpg"):
            img_data = await response.body()
            filename = Path(url.split("/")[-1])
            save_path = self.output_dir / filename
            with open(save_path, "wb") as f:
                f.write(img_data)
                print(f"🖼️ Saved image: {save_path}")

    async def search(self, query: str):
        
        self.page = await self.browser.new_page()
        
        self.output_dir = Path(os.path.join(self.curr_dir,Path("filtered_images")))
        
        self.output_dir.mkdir(exist_ok=True)
        
        
        # self.page.on("response",self.download_photo_response)
        
        # self.page.on(
        #     "request", lambda request: print(">>", request.method, request.url)
        # )
        # self.page.on(
        #     "response", lambda response: print("<<", response.status, response.url)
        # )

        await self.page.goto(
            f"https://pixabay.com/photos/search/{query}/?content_type=authentic&orientation=horizontal"
        )
        await (await self.page.query_selector(selector="input[type='search']")).fill(
            query
        )
        await self.page.evaluate(
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

    async def filter(self):
        # photo => div[class^="filters"] div[class^="lhs"]  div[class^="container"]:nth-child(1) > div[class^="triggerWrapper"] > button
        await (
            await self.page.query_selector(
                'div[class^="filters"] div[class^="lhs"]  div[class^="container"]:nth-child(1) > div[class^="triggerWrapper"] > button'
            )
        ).click()

        await asyncio.sleep(2)
        # dropdown photo click => div[class^="filters"] div[class^="lhs"]  div[class^="container"]:nth-child(1) > div[class^="dropdown"]  div[class^="dropdownMenuItem"]:nth-child(2)
        await (
            await self.page.query_selector(
                'div[class^="filters"] div[class^="lhs"]  div[class^="container"]:nth-child(1) > div[class^="dropdown"]  div[class^="dropdownMenuItem"]:nth-child(2)'
            )
        ).click()
        await asyncio.sleep(2)
        # horizontal => div[class^="filters"] div[class^="lhs"]  div[class^="container"]:nth-child(2) > div[class^="triggerWrapper"] >button
        await (
            await self.page.query_selector(
                'div[class^="filters"] div[class^="lhs"]  div[class^="container"]:nth-child(2) > div[class^="triggerWrapper"] >button'
            )
        ).click()
        await asyncio.sleep(2)
        # div[class^="filters"] div[class^="lhs"]  div[class^="container"]:nth-child(2) > div[class^="dropdown"]  div[class^="dropdownMenuItem"]:nth-child(2)
        await (
            await self.page.query_selector(
                'div[class^="filters"] div[class^="lhs"]  div[class^="container"]:nth-child(2) > div[class^="dropdown"]  div[class^="dropdownMenuItem"]:nth-child(2)'
            )
        ).click()
        await asyncio.sleep(2)
        # authencity => div[class^="filters"] div[class^="lhs"]  div[class^="container"]:nth-child(6) > div[class^="triggerWrapper"] >button
        await (
            await self.page.query_selector(
                'div[class^="filters"] div[class^="lhs"]  div[class^="container"]:nth-child(6) > div[class^="triggerWrapper"] >button'
            )
        ).click()
        await asyncio.sleep(2)
        # div[class^="filters"] div[class^="lhs"]  div[class^="container"]:nth-child(6) > div[class^="dropdown"]  div[class^="dropdownMenuItem"]:nth-child(2)
        await (
            await self.page.query_selector(
                'div[class^="filters"] div[class^="lhs"]  div[class^="container"]:nth-child(6) > div[class^="dropdown"]  div[class^="dropdownMenuItem"]:nth-child(2)'
            )
        ).click()
        await asyncio.sleep(2)

    async def result(self):
        images = await self.page.query_selector_all(
            'div[class^="results"] div[class^="verticalMasonry"] script[type="application/ld+json"]'
        )
        images_result = []
        for image in images:
            img = json.loads(await image.text_content())
            images_result.append(img)
            print(img["contentUrl"])

        return images_result

    async def download(self):
        pass
