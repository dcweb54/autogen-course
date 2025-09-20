from typing import Awaitable, Callable
from patchright.async_api import Page, ElementHandle
import asyncio
import re


class ColabNoteBook:
    def __init__(self, page: Page):
        self.page = page

    async def handle_cell(self, cell: ElementHandle):
        await (await cell.query_selector(selector="colab-run-button")).click()
        await asyncio.sleep(2)
        while True:
            if await self.is_cell_running(cell=cell):
                output = (await self.get_cell_output(cell=cell)).strip().split("\n")
                print(output)
            else:
                await asyncio.sleep(2)
                print("cell execuation finished")
                output = await self.get_cell_output(cell=cell)
                print(output.strip().split("\n"))
                break

            await asyncio.sleep(2)

    def extract_url(self, text):
        match = re.search(r"https?://[^\s]+", text)
        return match.group(0) if match else None

    async def handle_cell_with_restart(self, cell: ElementHandle):
        await (await cell.query_selector(selector="colab-run-button")).click()
        await asyncio.sleep(3)
        while True:
            if await self.is_cell_running(cell=cell):
                print("restart runing")
                output = (await self.get_cell_output(cell=cell)).strip().split("\n")
                print(output)
            else:
                await asyncio.sleep(2)
                print("cell execuation finished")
                output = await self.get_cell_output(cell=cell)
                print(output.strip().split("\n"))
                break

            await asyncio.sleep(2)

    # async def handle_restart(self):
    #     if await self.is_cell_restart():
    #         await self.page.click(
    #             selector="body > mwc-dialog > md-text-button:nth-child(3) >> #button > span.touch"
    #         )

    async def is_cell_restart(self) -> bool:
        try:
            await self.page.wait_for_selector(
                selector="body > mwc-dialog > md-text-button:nth-child(3) >> #button > span.touch",
            )
            return True
        except:  # noqa: E722
            return False

    async def handle_cell_with_url(self, cell: ElementHandle):
        await (await cell.query_selector(selector="colab-run-button")).click()
        await asyncio.sleep(3)
        url = ""
        hasUrl = False
        while True:
            if hasUrl:
                break
            if await self.is_cell_running(cell=cell):
                output = (await self.get_cell_output(cell=cell)).strip().split("\n")
                
                if hasUrl:
                    break
                
                for log in output:
                    if "Running on public URL" in log:
                        print(self.extract_url(log))
                        url = self.extract_url(log)
                        hasUrl = True
                        break
            else:
                await asyncio.sleep(2)
                print("cell execuation finished")
                output = await self.get_cell_output(cell=cell)
                print(output.strip().split("\n"))
                break

            await asyncio.sleep(2)
        return url

    async def is_cell_running(self, cell: ElementHandle):
        # selectors[0].querySelector('.cell-ui-refresh').shadowRoot.querySelector('colab-tooltip-trigger').getAttribute('message')
        # Run cell (Ctrl+Enter)
        # check cell message value
        status = await (
            await cell.query_selector(
                selector=".cell-ui-refresh >> colab-tooltip-trigger",
            )
        ).get_attribute("message")

        if "Run cell" in status:
            return False
        elif "Interrupt execution" in status:
            return True

    async def get_cell_output(self, cell: ElementHandle):
        return await (
            await cell.query_selector(selector=".output-iframe-sizer")
        ).text_content()
