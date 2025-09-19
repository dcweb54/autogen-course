from typing import Any, List, AsyncGenerator, Dict, Callable, Awaitable, Any
from patchright.async_api import Playwright, Page, ElementHandle
import asyncio
import time
from enum import Enum, auto
from colab_change_runtime_type import ChangeRuntimeType


async def get_cell_state(cell: ElementHandle):
    """
    Get detailed execution state of a cell — matching JS getColabExecutionStatus() logic.
    Returns dict with:
        - success: bool
        - data: { isRunning, isFocused, hasError, output } or None
        - error: str (if failed)
    """
    try:
        state = await cell.evaluate("""(cell) => {
            const button = cell.querySelector('colab-run-button');
            if (!button) {
                return { success: false, error: 'Run button not found in cell' };
            }

            const shadowRoot = button.shadowRoot;
            if (!shadowRoot) {
                return { success: false, error: 'Shadow DOM not available. Button might not be fully loaded.' };
            }

            const executionDiv = shadowRoot.querySelector('.cell-execution');
            if (!executionDiv) {
                return { success: false, error: 'Execution status div (.cell-execution) not found inside shadow root.' };
            }

            const isRunning = executionDiv.classList.contains('running') || executionDiv.classList.contains('animating');
            const isFocused = executionDiv.classList.contains('focused');
            const hasError = executionDiv.classList.contains('error') || !!executionDiv.querySelector('.error');

            let output = [];
            const outputContainer = cell.querySelector(
                'div.codecell-input-output div.output div.output-content div.output-iframe-container'
            );

            if (outputContainer && outputContainer.textContent) {
                output = outputContainer.textContent.trim().split('\\n');
            }

            return {
                success: true,
                data: {
                    isRunning,
                    isFocused,
                    hasError,
                    output
                }
            };
        }""")

        if not state.get("success", False):
            return {
                "success": False,
                "error": state.get("error", "Unknown error in JS evaluation"),
                "data": None,
            }

        return state

    except Exception as e:
        return {
            "success": False,
            "error": f"Python exception: {str(e)}",
            "data": None,
        }


class WaitStatus(Enum):
    SUCCESS = auto()
    TIMEOUT = auto()
    ERROR = auto()


class ConnectionStatus(Enum):
    Connect = auto()
    Connected = auto()
    Connecting = auto()
    Reconnect = auto()
    Unknow = auto()


async def handle_notebook_cell(page: Page):
    print("handle_notebook_cell")
    pass


async def handle_addition_connection_option(
    page: Page, connection_status: ConnectionStatus
):
    # document.querySelector("#top-toolbar > colab-connect-button").shadowRoot.querySelector("#connect-dropdown").shadowRoot.querySelector("#button > span.touch")
    #  handle addition option connection button click
    await page.wait_for_selector(
        selector="#top-toolbar > colab-connect-button >> #connect-dropdown >> #button > span.touch"
    )
    await page.click(
        selector="#top-toolbar > colab-connect-button >> #connect-dropdown >> #button > span.touch"
    )

    if connection_status is ConnectionStatus.Connecting:
        await handle_disconnect_and_delete_runtime(page)
    elif connection_status is ConnectionStatus.Reconnect:
        await handle_change_runtime_type(page)
    elif connection_status is ConnectionStatus.Connect:
        await handle_change_runtime_type(page)


async def handle_disconnect_and_delete_runtime(page: Page):
    print("handle_disconnect_and_delete_runtime")
    # await page.wait_for_selector()
    await handle_coordinates_click(
        page=page,
        coordinates={
            "x": 905,
            "y": 327,
            "width": 329.34375,
            "height": 32,
            "top": 327,
            "right": 1234.34375,
            "bottom": 359,
            "left": 905,
        },
    )
    await asyncio.sleep(3)

    async def handle_yes_no(page: Page):
        # document.querySelector("body > mwc-dialog > md-text-button:nth-child(3)").shadowRoot.querySelector("#button > span.touch")
        await page.wait_for_selector(
            selector="body > mwc-dialog > md-text-button:nth-child(3) >> #button > span.touch"
        )
        await page.click(
            selector="body > mwc-dialog > md-text-button:nth-child(3) >> #button > span.touch"
        )

    await handle_yes_no(page=page)
    await asyncio.sleep(3)


async def handle_change_runtime_type(page: Page):
    print("handle_change_runtime_type")
    change_runtime = ChangeRuntimeType(page)
    await change_runtime.click_at_change_runtime_button_by_coordinates()
    await asyncio.sleep(2)
    await change_runtime.select_TPU_v5e_by_selector()
    await asyncio.sleep(2)
    await change_runtime.handle_save_by_selector()
    await asyncio.sleep(2)


async def handle_coordinates_click(page: Page, coordinates: dict[str, Any]):
    print("handle_coordinates_click")
    center_x = coordinates["x"] + coordinates["width"] / 2
    center_y = coordinates["y"] + coordinates["height"] / 2
    print(f"Clicking at center: X={center_x:.1f}, Y={center_y:.1f}")
    # Move mouse to the position (optional, but good for visibility)
    await page.mouse.move(center_x, center_y)
    await asyncio.sleep(1)
    await page.mouse.click(center_x, center_y)
    await asyncio.sleep(2)


async def handle_page(page: Page):
    connection_status = await check_connection_status(page)
    if connection_status is not None:
        if connection_status is ConnectionStatus.Connected:
            print(f"Result {connection_status}")
            print("cell operation must be started")
            await handle_notebook_cell(page)
        elif connection_status is ConnectionStatus.Connect:
            print(f"Result {connection_status}")
            await handle_addition_connection_option(
                page, connection_status=connection_status
            )
            # await handle_page(page=page)
        elif connection_status is ConnectionStatus.Reconnect:
            print(f"Result {connection_status}")
            print("click the reconnet button")
            await handle_addition_connection_option(
                page, connection_status=connection_status
            )
            # await handle_page(page=page)
        elif connection_status is ConnectionStatus.Connecting:
            print(f"Result {connection_status}")
            print("we need to disconnect and delete runtime")
            await handle_addition_connection_option(
                page, connection_status=connection_status
            )
            # await handle_page(page=page)
        else:
            print(f"Result {connection_status}")
            print("unkwron operation should be handle later")
    else:
        print("something Error from connection ")


async def check_connection_status(
    page: Page,
    timeout: float = 60.0,
) -> ConnectionStatus | None:
    start = time.monotonic()
    try:
        while True:
            connection = await extract_the_connection_string(page)
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



async def extract_the_connection_string(page: Page) -> ConnectionStatus:
    await page.wait_for_selector(
        selector="#top-toolbar > colab-connect-button >> colab-toolbar-button"
    )
    # document.querySelector("#top-toolbar > colab-connect-button").shadowRoot.querySelector('colab-toolbar-button').textContent.trim()
    connection_element = await page.query_selector(
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


async def wait_for_condition(
    condition: Callable[[], Awaitable[bool]],
    timeout: float = 10.0,
    interval: float = 0.5,
) -> WaitStatus:
    """
    Asynchronously wait for a condition to be True within a timeout.

    Args:
        condition: Async function returning bool.
        timeout: Max seconds to wait.
        interval: Sleep time between checks.

    Returns:
        WaitStatus: SUCCESS, TIMEOUT, or ERROR.
    """
    start = time.monotonic()
    try:
        while True:
            if await condition():
                return WaitStatus.SUCCESS
            if time.monotonic() - start > timeout:
                return WaitStatus.TIMEOUT
            await asyncio.sleep(interval)
    except Exception:
        return WaitStatus.ERROR


# Example async condition
async def check_something() -> bool:
    await asyncio.sleep(3)
    """Dummy condition: True if current second is even."""
    return int(time.time()) % 2 == 0


async def handle_colab():
    pass


async def main():
    print("⏳ Waiting up to 5s for condition...")

    status = await wait_for_condition(check_something, timeout=30)

    if status is WaitStatus.SUCCESS:
        print("✅ Condition met!")
    elif status is WaitStatus.TIMEOUT:
        print("⏰ Timeout reached without condition.")
    else:
        print("❌ Error occurred while checking condition.")


if __name__ == "__main__":
    asyncio.run(main())
