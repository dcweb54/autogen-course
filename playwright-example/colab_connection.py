from enum import Enum, auto
from patchright.async_api import Page
import asyncio
import time


class ConnectionStatus(Enum):
    Connect = auto()
    Connected = auto()
    Connecting = auto()
    Reconnect = auto()
    Unknow = auto()


class ColabConnection:
    def __init__(self, page: Page):
        self.page = page

    async def click_at_connect_by_selector(self):
        print("click method should be implemented")
        # document.querySelector("#top-toolbar > colab-connect-button").shadowRoot.querySelector("#connect").shadowRoot.querySelector("#button").shadowRoot.querySelector("#button > span.touch")
        await self.page.wait_for_selector(
            selector="#top-toolbar > colab-connect-button >> #connect >> #button >> #button > span.touch"
        )
        await self.page.click(
            selector="#top-toolbar > colab-connect-button >> #connect >> #button >> #button > span.touch"
        )
        
        await self.handle_connot_connect_to_this_backend()

    async def handle_connot_connect_to_this_backend(self):
        if await self.is_cannot_connect_to_gpu_backend_element():
            print("cannot_connect_to_gpu_backend")
            await self.page.click(
                selector="body > mwc-dialog > md-text-button:nth-child(3) >> #button > span.touch"
            )

    async def is_cannot_connect_to_gpu_backend_element(self) -> bool:
        try:
            await self.page.wait_for_selector(
                selector="body > mwc-dialog > md-text-button:nth-child(3) >> #button > span.touch"
            )
            return True
        except Exception as e:
            return False

    async def wait_for_colab_toolbar_button_status(self, timeout: float = 30):
        start = time.monotonic()
        while True:
            await self.get_colab_toolbar_button_status()
            if time.monotonic() - start > timeout:
                print("break 1")
                return await self.get_colab_toolbar_button_status()
            else:
                print("break 2")
                await self.get_colab_toolbar_button_status()
            #     return None
            await asyncio.sleep(2)

    async def get_colab_toolbar_button_status(self) -> ConnectionStatus:
        if await self.is_colab_toolbar_button_disable():
            print("true")
            return ConnectionStatus.Connecting
        else:
            get_status = await self.get_colab_toolbar_text()
            # print(get_status)
            if "Connect to a new runtime" in get_status:
                print("Connect to a new runtime => connect")
                return ConnectionStatus.Connect
            elif "Click to connect" in get_status:
                print("Click to connect => Reconnect")
                return ConnectionStatus.Reconnect
            elif "Connected to" in get_status:
                print("Connected to => already connected")
                return ConnectionStatus.Connected

    async def is_colab_toolbar_button_disable(self) -> bool:
        # document.querySelector('#top-toolbar > colab-connect-button').shadowRoot.querySelector('colab-toolbar-button').disabled
        return await (
            await self.page.query_selector(
                selector="#top-toolbar > colab-connect-button >> colab-toolbar-button"
            )
        ).evaluate(expression="node => node.disabled")

    async def get_colab_toolbar_text(self) -> str:
        return await (
            await self.page.query_selector(
                selector="#top-toolbar > colab-connect-button >> colab-toolbar-button"
            )
        ).get_attribute("tooltiptext")

        # evaluate(expression=" node => node.getAttribute('tooltiptext').trim().split('\n')")

    # document.querySelector('#top-toolbar > colab-connect-button').shadowRoot.querySelector('colab-toolbar-button').getAttribute('tooltiptext').trim().split('\n')

    #     [
    #     "Connected to",
    #     "Python 3 Google Compute Engine backend",
    #     "RAM: 0.94 GB/12.67 GB",
    #     "Disk: 39.05 GB/107.72 GB"
    # ]

    # (4) ['Waiting to finish the current execution.', 'Python 3 Google Compute Engine backend', 'RAM: 0.99 GB/12.67 GB', 'Disk: 39.06 GB/107.72 GB']0: "Waiting to finish the current execution."1: "Python 3 Google Compute Engine backend"2: "RAM: 0.99 GB/12.67 GB"3: "Disk: 39.06 GB/107.72 GB"length: 4[[Prototype]]: Array(0)

    # document.querySelector('#top-toolbar > colab-connect-button').shadowRoot.querySelector('colab-toolbar-button').disabled
    # connecting

    # document.querySelector('#top-toolbar > colab-connect-button').shadowRoot.querySelector('colab-toolbar-button').getAttribute('tooltiptext')
    # 'Click to connect' in case of reconect

    # document.querySelector('#top-toolbar > colab-connect-button').shadowRoot.querySelector('colab-toolbar-button').getAttribute('tooltiptext')
    # 'Connect to a new runtime'

    async def wait_for_connection_status(
        self,
        timeout: float = 60.0,
    ) -> ConnectionStatus | None:
        start = time.monotonic()
        try:
            while True:
                connection = await self.extract_the_connection_string()
                status = await self.is_colab_toolbar_button_disable()
                print(f"button status {status}")
                await self.get_colab_toolbar_button_status()
                if connection is ConnectionStatus.Connected:
                    return ConnectionStatus.Connected
                elif connection is ConnectionStatus.Reconnect:
                    return ConnectionStatus.Reconnect
                elif connection is ConnectionStatus.Connect:
                    return ConnectionStatus.Connect
                elif time.monotonic() - start > timeout:
                    if connection is ConnectionStatus.Connecting:
                        return ConnectionStatus.Connecting
                    else:
                        return ConnectionStatus.Unknow
                await asyncio.sleep(3)
        except Exception as e:
            print(e)
            return None

    async def check_tooltip_text(self):
        pass

    async def extract_the_connection_string(self) -> ConnectionStatus:
        await self.page.wait_for_selector(
            selector="#top-toolbar > colab-connect-button >> colab-toolbar-button"
        )
        # document.querySelector("#top-toolbar > colab-connect-button").shadowRoot.querySelector('colab-toolbar-button').textContent.trim()
        connection_element = await self.page.query_selector(
            selector="#top-toolbar > colab-connect-button >> colab-toolbar-button"
        )
        connection_string = await connection_element.evaluate(
            expression="node => node.textContent.trim()"
        )

        if "Connecting" in connection_string:
            print("connecting")
            return ConnectionStatus.Connecting
        elif "Connected" in connection_string:
            print("Connected")
            return ConnectionStatus.Connected
        elif "Reconnect" in connection_string:
            print("Reconnect")
            return ConnectionStatus.Reconnect
        elif "Connect" in connection_string:
            print("connect")
            return ConnectionStatus.Connect
        else:
            print("Unknow")
            return ConnectionStatus.Unknow
