from typing import Any
from colab_change_runtime_type import ChangeRuntimeType
from patchright.async_api import Page
import asyncio
from colab_connection import ConnectionStatus


class AdditionalOption:
    def __init__(self, page: Page):
        self.page = page

    async def handle_additional_option(self, connection_status: ConnectionStatus):
        
        await self.page.wait_for_selector(
            selector="#top-toolbar > colab-connect-button >> #connect-dropdown >> #button > span.touch"
        )
        await self.page.click(
            selector="#top-toolbar > colab-connect-button >> #connect-dropdown >> #button > span.touch"
        )

        await asyncio.sleep(3)

        if connection_status is ConnectionStatus.Connecting:
            await self.handle_disconnect_and_delete_runtime()
            await self.handle_change_runtime_type()
        elif connection_status is ConnectionStatus.Reconnect:
            await self.handle_change_runtime_type()
        elif connection_status is ConnectionStatus.Connect:
            await self.handle_change_runtime_type()

    async def handle_change_runtime_type(self):
        print("handle_change_runtime_type")
        change_runtime = ChangeRuntimeType(self.page)
        await change_runtime.click_at_change_runtime_button_by_coordinates()
        await asyncio.sleep(2)
        await change_runtime.select_cpu_by_selector()
        await asyncio.sleep(2)
        await change_runtime.handle_save_by_selector()
        await asyncio.sleep(2)

    async def handle_disconnect_and_delete_runtime(self):
        await self._handle_coordinates_click(
            coordinates={
                "x": 923,
                "y": 333,
                "width": 194.34375,
                "height": 20,
                "top": 333,
                "right": 1117.34375,
                "bottom": 353,
                "left": 923,
            }
        )
        await asyncio.sleep(3)
        await self.page.wait_for_selector(
            selector="body > mwc-dialog > md-text-button:nth-child(3) >> #button > span.touch"
        )
        await self.page.click(
            selector="body > mwc-dialog > md-text-button:nth-child(3) >> #button > span.touch"
        )

    async def _handle_coordinates_click(self, coordinates: dict[str, Any]):
        print("handle_coordinates_click")
        center_x = coordinates["x"] + coordinates["width"] / 2
        center_y = coordinates["y"] + coordinates["height"] / 2
        print(f"Clicking at center: X={center_x:.1f}, Y={center_y:.1f}")
        # Move mouse to the position (optional, but good for visibility)
        await self.page.mouse.move(center_x, center_y)
        await asyncio.sleep(1)
        await self.page.mouse.click(center_x, center_y)
        await asyncio.sleep(2)
