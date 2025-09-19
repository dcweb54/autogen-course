from typing import Any
from patchright.async_api import Page
import asyncio


class ChangeRuntimeType:
    def __init__(self, page: Page):
        self.page = page

    async def click_at_change_runtime_button_by_coordinates(self):
        await self._handle_coordinates_click(
            coordinates={
                "x": 905,
                "y": 141,
                "width": 329.34375,
                "height": 32,
                "top": 141,
                "right": 1234.34375,
                "bottom": 173,
                "left": 905,
            },
        )

    async def select_cpu_by_coordinates(self):
        await self._handle_coordinates_click(
            coordinates={
                "x": 400,
                "y": 282.125,
                "width": 48,
                "height": 48,
                "top": 282.125,
                "right": 448,
                "bottom": 330.125,
                "left": 400,
            }
        )

    async def select_cpu_by_selector(self):
        await self.page.click(
            selector="body > mwc-dialog > div > div > colab-runtime-attributes-selector >> div:nth-child(4) > mwc-formfield:nth-child(1) > mwc-radio >> div > input"
        )

    async def select_T4_GPU_by_coordinates(self):
        await self._handle_coordinates_click(
            coordinates={
                "x": 500.15625,
                "y": 242.625,
                "width": 48,
                "height": 48,
                "top": 242.625,
                "right": 548.15625,
                "bottom": 290.625,
                "left": 500.15625,
            },
        )

    async def select_T4_GPU_by_selector(self):
        await self.page.click(
            selector="body > mwc-dialog > div > div > colab-runtime-attributes-selector >> div:nth-child(4) > mwc-formfield:nth-child(2) > mwc-radio >> div > input"
        )

    async def select_TPU_v5e_by_coordinates(self):
        await self._handle_coordinates_click(
            coordinates={
                "x": 400,
                "y": 328.125,
                "width": 48,
                "height": 48,
                "top": 328.125,
                "right": 448,
                "bottom": 376.125,
                "left": 400,
            },
        )

    async def select_TPU_v5e_by_selector(self):
        await self.page.click(
            selector="body > mwc-dialog > div > div > colab-runtime-attributes-selector >> div:nth-child(4) > mwc-formfield:nth-child(5) > mwc-radio >> div > input"
        )

    async def handle_save_by_coordinates(self):
        await self._handle_coordinates_click(
            coordinates={
                "x": 848,
                "y": 568.875,
                "width": 64,
                "height": 48,
                "top": 568.875,
                "right": 912,
                "bottom": 616.875,
                "left": 848,
            },
        )

    async def handle_save_by_selector(self):
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
