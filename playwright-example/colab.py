# from playwright.async_api import async_playwright, Playwright
from typing import Any, List, AsyncGenerator, Dict, Callable, Awaitable, Any
from patchright.async_api import async_playwright, Playwright, Page, ElementHandle
import asyncio
import re
from gradio_client import Client, handle_file
import time
from enum import Enum, auto
from colab_page_event import (
    check_connection_status,
    get_cell_state,
    handle_colab,
    extract_the_connection_string,
    ConnectionStatus,
    handle_page,
)


async def run_cells_with_restart_handling(page: Page):
    """Simplified version with basic restart handling"""

    cells = await page.query_selector_all(".cell")
    cell_index = 0
    max_restarts = 3
    restart_count = 0

    while cell_index < len(cells) and restart_count < max_restarts:
        cell = cells[cell_index]

        print(f"Processing cell {cell_index + 1}/{len(cells)}")

        try:
            # Check for restart dialog before each cell
            restart_dialog = await page.query_selector(
                "body > mwc-dialog > md-text-button:nth-child(3) >> #button > span.touch"
            )
            if restart_dialog:
                print("⚠️  Restart dialog detected! Handling...")
                restart_count += 1

                # Try to click restart button
                await page.evaluate("""() => {
                    document.querySelector("body > mwc-dialog > md-text-button:nth-child(3)").shadowRoot.querySelector("#button > span.touch")
        
                }""")

                # Wait and restart from beginning
                await asyncio.sleep(10)
                await page.wait_for_selector("#top-toolbar", timeout=30000)
                print("🔄 Restarting from cell 1...")
                cell_index = 0
                continue

            # Run the cell
            run_button = await cell.query_selector("colab-run-button")
            if run_button:
                await run_button.evaluate(
                    '(btn) => btn.shadowRoot?.querySelector("div")?.click()'
                )
                print("✅ Run button clicked")

            # Wait for completion with restart checking
            try:
                await page.wait_for_function(
                    """(cell) => {
                    const running = cell.querySelector('.cell-execution, .spinner');
                    const output = cell.querySelector('.output, .output-area');
                    return !running && output;
                }""",
                    timeout=60000,
                    arg=cell,
                )

                print("✅ Cell completed")
                cell_index += 1

            except Exception as e:
                print("⏰ Cell timeout - checking for restart")
                # Check if restart occurred during wait
                if await page.query_selector(
                    "body > mwc-dialog > md-text-button:nth-child(3) >> #button > span.touch"
                ):
                    print("⚠️  Restart occurred during execution")
                    restart_count += 1
                    cell_index = 0  # Restart from beginning
                    await asyncio.sleep(5)
                    continue
                else:
                    print("⚠️  Moving to next cell")
                    cell_index += 1

        except Exception as e:
            print(f"❌ Error: {e}")
            cell_index += 1  # Move to next cell on error

    print(f"Completed {cell_index} cells with {restart_count} restarts")


async def select_additional_connection(page: Page):
    await page.evaluate(
        expression="""() => {
                // Navigate through the shadow roots
                const topToolbar = document.querySelector("#top-toolbar > colab-connect-button");
                if (topToolbar) {
                    const connectDropdown = topToolbar.shadowRoot.querySelector("#connect-dropdown");
                    if (connectDropdown) {
                        const button = connectDropdown.shadowRoot.querySelector("#button > span.touch");
                        if (button) {
                            button.click();
                            return true;
                        }
                    }
                }
                return false;
            }
        """
    )
    await asyncio.sleep(2)


async def select_runtime(page: Page):
    coordinates = {
        "x": 905,
        "y": 141,
        "width": 329.34375,
        "height": 32,
        "top": 141,
        "right": 1234.34375,
        "bottom": 173,
        "left": 905,
    }

    center_x = coordinates["x"] + coordinates["width"] / 2
    center_y = coordinates["y"] + coordinates["height"] / 2
    print(f"Clicking at center: X={center_x:.1f}, Y={center_y:.1f}")
    # Move mouse to the position (optional, but good for visibility)
    await page.mouse.move(center_x, center_y)
    await asyncio.sleep(1)
    await page.mouse.click(center_x, center_y)
    await asyncio.sleep(2)


async def select_gpu_by_selector(page: Page):
    await page.evaluate("""() => {
        const element = document.querySelector("body > mwc-dialog > div > div > colab-runtime-attributes-selector")
            ?.shadowRoot?.querySelector("div:nth-child(4) > mwc-formfield:nth-child(2) > mwc-radio")
            ?.shadowRoot?.querySelector("div > input");
        
        if (element) {
            element.click();
            return true;
        }
        return false;
    }""")
    await asyncio.sleep(3)


async def select_gpu(page: Page):
    # document.querySelector("body > mwc-dialog > div > div > colab-runtime-attributes-selector").shadowRoot.querySelector("div:nth-child(4) > mwc-formfield:nth-child(2) > mwc-radio").shadowRoot.querySelector("div > input")

    coordinates = {
        "x": 500.15625,
        "y": 242.625,
        "width": 48,
        "height": 48,
        "top": 242.625,
        "right": 548.15625,
        "bottom": 290.625,
        "left": 500.15625,
    }

    center_x = coordinates["x"] + coordinates["width"] / 2
    center_y = coordinates["y"] + coordinates["height"] / 2
    print(f"Clicking at center: X={center_x:.1f}, Y={center_y:.1f}")
    # Move mouse to the position (optional, but good for visibility)
    await page.mouse.move(center_x, center_y)
    await asyncio.sleep(1)
    await page.mouse.click(center_x, center_y)
    await asyncio.sleep(2)


async def select_cpu(page: Page):
    coordinates = {
        "x": 400,
        "y": 282.125,
        "width": 48,
        "height": 48,
        "top": 282.125,
        "right": 448,
        "bottom": 330.125,
        "left": 400,
    }

    center_x = coordinates["x"] + coordinates["width"] / 2
    center_y = coordinates["y"] + coordinates["height"] / 2
    print(f"Clicking at center: X={center_x:.1f}, Y={center_y:.1f}")
    # Move mouse to the position (optional, but good for visibility)
    await page.mouse.move(center_x, center_y)
    await asyncio.sleep(1)
    await page.mouse.click(center_x, center_y)
    await asyncio.sleep(2)


async def save_runtime_selection(page: Page):
    # document.querySelector("body > mwc-dialog > md-text-button:nth-child(3)").shadowRoot.querySelector("#button > span.touch")
    await page.evaluate("""() => {
        const button = document.querySelector("body > mwc-dialog > md-text-button:nth-child(3)")
            ?.shadowRoot?.querySelector("#button > span.touch");
        
        if (button) {
            button.click();
            console.log("Button clicked successfully!");
            return true;
        } else {
            console.log("Button not found");
            return false;
        }
    }""")
    await asyncio.sleep(2)


async def click_connect(page: Page):
    result = await page.evaluate("""() => {
        try {
            const connectButton = document.querySelector("#top-toolbar > colab-connect-button");
            if (!connectButton) {
                throw new Error("colab-connect-button not found");
            }
            
            const connectShadow = connectButton.shadowRoot;
            if (!connectShadow) {
                throw new Error("No shadow root on colab-connect-button");
            }
            
            const connectElement = connectShadow.querySelector("#connect");
            if (!connectElement || !connectElement.shadowRoot) {
                throw new Error("#connect element not found or no shadow root");
            }
            
            const buttonElement = connectElement.shadowRoot.querySelector("#button");
            if (!buttonElement || !buttonElement.shadowRoot) {
                throw new Error("#button element not found or no shadow root");
            }
            
            const spanElement = buttonElement.shadowRoot.querySelector("#button > span.touch");
            if (!spanElement) {
                throw new Error("span.touch element not found");
            }
            
            spanElement.click();
            return {success: true, message: "Button clicked successfully!"};
            
        } catch (error) {
            return {success: false, message: error.message};
        }
    }""")
    print(f"Result: {result}")
    await asyncio.sleep(2)


async def get_connection_status(page):
    """Get detailed connection status"""
    return await page.evaluate("""() => {
        try {
            const connectElement = document.querySelector("#top-toolbar > colab-connect-button")
                ?.shadowRoot?.querySelector("#connect");
            
            if (!connectElement) return {status: "not_found", details: "Connect button not found"};
            
            // Check tooltip
            const tooltip = connectElement.shadowRoot?.querySelector("colab-tooltip-trigger");
            const tooltipText = tooltip?.getAttribute("message") || "";
            
            // Check resource displays (only visible when connected)
            const resources = connectElement.querySelector("#connect-button-resource-display");
            const hasResources = resources && resources.children.length > 0;
            
            if (tooltipText.includes("Google Compute Engine") || hasResources) {
                return {
                    status: "connected", 
                    details: tooltipText,
                    hasResources: hasResources
                };
            }
            
            return {status: "disconnected", details: tooltipText};
            
        } catch (error) {
            return {status: "error", details: error.message};
        }
    }""")


async def ensure_colab_connected(page, max_wait=60):
    """Ensure Colab is connected, wait if not"""
    print("Checking Colab connection status...")

    for attempt in range(max_wait // 2):
        status_info = await get_connection_status(page)
        print(f"Status: {status_info['status']} - {status_info['details'][:50]}...")

        if status_info["status"] == "connected":
            print("🎉 Colab is connected and ready!")
            return True

        # If disconnected for a while, try to click connect
        if attempt == 5 and status_info["status"] == "disconnected":
            print("Attempting to connect...")
            await page.evaluate("""() => {
                document.querySelector("#top-toolbar > colab-connect-button")
                    ?.shadowRoot?.querySelector("#connect")
                    ?.click();
            }""")

        await asyncio.sleep(2)

    print("❌ Failed to establish connection within timeout")
    return False


async def select_input_cell(coordinates: dict[str, Any], page: Page):
    # Calculate center point (most reliable click location)
    center_x = coordinates["x"] + coordinates["width"] / 2
    center_y = coordinates["y"] + coordinates["height"] / 2
    print(f"Clicking at center: X={center_x:.1f}, Y={center_y:.1f}")
    # Move mouse to the position (optional, but good for visibility)
    await page.mouse.move(center_x, center_y)
    await asyncio.sleep(1)
    await page.mouse.click(center_x, center_y)
    await asyncio.sleep(2)


async def typing_input_cell(page: Page):
    await page.fill(
        selector="div.editor.flex.lazy-editor > div > div > div.overflow-guard > textarea",
        value='print("test")',
    )


async def run_cell_with_retry(page, cell_selector, max_retries=2):
    """Run cell with retry mechanism in case of failures"""

    for attempt in range(max_retries + 1):
        print(f"🔄 Attempt {attempt + 1}/{max_retries + 1}")

        # Click run button
        clicked = await page.evaluate(f'''() => {{
            const btn = document.querySelector("{cell_selector}")
                ?.shadowRoot?.querySelector("div");
            if (btn) {{
                btn.click();
                return true;
            }}
            return false;
        }}''')

        if not clicked:
            print("❌ Could not find run button")
            continue

        # Wait for completion with timeout
        try:
            await page.wait_for_function(
                f'''() => {{
                const cell = document.querySelector("{cell_selector}").closest(".cell");
                return cell && !cell.querySelector(".spinner") && cell.querySelector(".output");
            }}''',
                timeout=60000,
            )

            print("✅ Success on attempt", attempt + 1)
            return True

        except Exception as e:
            print(f"⏰ Timeout on attempt {attempt + 1}")
            if attempt < max_retries:
                print("Retrying...")
                await asyncio.sleep(3)

    return False


async def run_all_cells_with_progress(page):
    """Run all cells with progress monitoring"""

    # First, get total cell count
    total_cells = await page.evaluate("""() => {
        return document.querySelectorAll('.cell').length;
    }""")

    print(f"📊 Found {total_cells} cells to execute")

    # Click all run buttons
    await page.evaluate("""() => {
        const runButtons = document.querySelectorAll(
            'div.main-content > div > div.codecell-input-output > div.inputarea.horizontal.layout.code > div.cell-gutter > div > colab-run-button'
        );
        
        console.log(`Clicking ${runButtons.length} run buttons...`);
        runButtons.forEach((button, index) => {
            setTimeout(() => {
                button.shadowRoot?.querySelector('div')?.click();
            }, index * 100); // Small delay between clicks
        });
    }""")

    print("⏳ Monitoring execution progress...")

    # Monitor progress
    completed = 0
    while completed < total_cells:
        current_completed = await page.evaluate("""() => {
            let count = 0;
            const cells = document.querySelectorAll('.cell');
            
            cells.forEach(cell => {
                const running = cell.querySelector('.cell-execution') || 
                              cell.querySelector('.spinner');
                const output = cell.querySelector('.output') || 
                             cell.querySelector('.output-area');
                
                if (!running && output) {
                    count++;
                }
            });
            
            return count;
        }""")

        if current_completed > completed:
            completed = current_completed
            print(f"📈 Progress: {completed}/{total_cells} cells completed")

        if completed < total_cells:
            await asyncio.sleep(3)
        else:
            break

    print("🎉 All cells executed successfully!")
    return True


async def run_cells_sequentially_simple(page):
    """Simplified sequential execution with better error handling"""

    # Get all cells
    cells = await page.query_selector_all(".cell")
    print(f"Found {len(cells)} cells")

    for i, cell in enumerate(cells):
        print(f"\n--- Processing Cell {i + 1}/{len(cells)} ---")

        try:
            # Find run button within this specific cell
            run_button = await cell.query_selector(
                "div.main-content > div > div.codecell-input-output > div.inputarea.horizontal.layout.code > div.cell-gutter > div > colab-run-button"
            )

            if not run_button:
                print(f"Cell {i + 1}: No run button found")
                continue

            # Click the run button safely
            await run_button.evaluate("""(button) => {
                try {
                    const div = button.shadowRoot.querySelector('div');
                    if (div) {
                        div.click();
                        return true;
                    }
                    return false;
                } catch (error) {
                    console.error('Click error:', error);
                    return false;
                }
            }""")

            print(f"Cell {i + 1}: Run button clicked")

            # Wait for completion
            try:
                await page.wait_for_function(
                    """(cell) => {
                    if (!cell) return false;
                    const running = cell.querySelector('.cell-execution, .spinner');
                    const output = cell.querySelector('.output, .output-area');
                    return !running && output;
                }""",
                    timeout=60000,
                    arg=cell,
                )

                print(f"Cell {i + 1}: Completed successfully")

            except Exception as e:
                print(f"Cell {i + 1}: Timeout waiting for completion")

            # Small delay between cells
            if i < len(cells) - 1:
                await asyncio.sleep(3)

        except Exception as e:
            print(f"Cell {i + 1}: Error - {e}")
            continue


async def cell_status(page: Page):
    # document.querySelector("div.main-content > div > div.codecell-input-output > div.inputarea.horizontal.layout.code > div.cell-gutter > div > colab-run-button").shadowRoot.querySelector("div").click()
    result = await page.evaluate(
        expression="""() => {
 
  try {
    // 1. Find the run button
    const button = document.querySelector('colab-run-button');
    if (!button) {
      throw new Error('Colab run button not found. Make sure you are in a Colab notebook environment.');
    }

    // 2. Access shadow DOM (may not be available immediately)
    const shadowRoot = button.shadowRoot;
    if (!shadowRoot) {
      throw new Error('Shadow DOM not available. Button might not be fully loaded.');
    }

    // 3. Find execution status div
    const executionDiv = shadowRoot.querySelector('.cell-execution');
    if (!executionDiv) {
      throw new Error('Execution status div (.cell-execution) not found inside shadow root.');
    }

    // 4. Extract output content (optional — may not exist if cell hasn’t run)
    let output = [];
    const outputContainer = document.querySelector(
      'div.codecell-input-output div.output div.output-content div.output-iframe-container'
    );

    if (outputContainer && outputContainer.textContent) {
      output = outputContainer.textContent.trim().split('\n');
    } else {
      console.warn('Output container not found or empty. Cell may not have executed yet.');
    }

    // 5. Build and return structured result
    return {
      success: true,
      data: {
        isRunning: executionDiv.classList.contains('running') || executionDiv.classList.contains('animating'),
        isFocused: executionDiv.classList.contains('focused'),
        hasError: executionDiv.classList.contains('error') || !!executionDiv.querySelector('.error'),
        output: output // Note: corrected typo from "ouput" → "output"
      }
    };

  } catch (error) {
    console.error('Error in getColabExecutionStatus:', error.message);
    return {
      success: false,
      error: error.message,
      data: null
    };
  }

        """
    )

    print(f"cell {result}")

    asyncio.sleep(2)


# document.querySelector("#\\:4k > div")


async def disconnect_and_delete_runtime(coordinates: dict[str, Any], page: Page):
    print("disconnect_and_delete_runtime operation")
    await select_additional_connection(page)
    await asyncio.sleep(3)
    center_x = coordinates["x"] + coordinates["width"] / 2
    center_y = coordinates["y"] + coordinates["height"] / 2
    print(
        f"Clicking at center: X={center_x:.1f}, Y={center_y:.1f} of disconnect_and_delete_runtime"
    )
    # Move mouse to the position (optional, but good for visibility)
    await page.mouse.move(center_x, center_y)
    await asyncio.sleep(1)
    await page.mouse.click(center_x, center_y)
    await asyncio.sleep(2)

    #  i want to check element to available for click for yes
    while True:
        if await is_disconnect_and_delete_runtime_dialog_available(page):
            # click at yes button
            await page.click(
                selector="body > mwc-dialog > md-text-button:nth-child(3) >> #button > span.touch"
            )
            await asyncio.sleep(2)
            break
        else:
            pass

    # document.querySelector("body > mwc-dialog > md-text-button:nth-child(3)").shadowRoot.querySelector("#button > span.touch")
    # {
    #     "x": 848,
    #     "y": 400.5,
    #     "width": 64,
    #     "height": 48,
    #     "top": 400.5,
    #     "right": 912,
    #     "bottom": 448.5,
    #     "left": 848,
    # }


async def is_disconnect_and_delete_runtime_dialog_available(page: Page) -> bool:
    try:
        await page.wait_for_selector(
            selector="body > mwc-dialog > md-text-button:nth-child(3) >> #button > span.touch"
        )
        return True
    except Exception as e:
        print("is_disconnect_and_delete_runtime_dialog_available False")
        return False


class WaitStatus(Enum):
    SUCCESS = auto()
    TIMEOUT = auto()
    ERROR = auto()


async def handle_connect_to_colab_server(page: Page) -> bool:
    # try max 3 and how to check
    # colab-toolbar-button[id="connect"]
    # document.querySelector("#top-toolbar > colab-connect-button").shadowRoot.querySelector('colab-toolbar-button').textContent.trim()
    # possible state connected, connecting, reconnect
    #  if connected state then move to cell operation
    #  if else connecting (there are some wait for to be connect) it will either return connected otherwiese stuck at connecting
    # i will wait for 30 second to second if not connect then move to disconnect_and_delete_runtime if it is successfull return the whole function check state change or not

    pass


async def wait_for_condition(
    condition: Callable[[], Awaitable[bool]],
    timeout: float = 10.0,
    interval: float = 0.5,
) -> bool:
    """
    Wait asynchronously for a condition to become True with a timeout.

    Args:
        condition: Async function returning bool.
        timeout: Max seconds to wait.
        interval: Sleep between checks.

    Returns:
        bool: True if condition met before timeout, False otherwise.
    """
    start = time.monotonic()
    while True:
        if await condition():
            return True
        if time.monotonic() - start > timeout:
            return False
        await asyncio.sleep(interval)


# Example async condition
async def check_something() -> bool:
    """Dummy condition: True if current second is even."""
    return int(time.time()) % 2 == 0


async def main():
    print("⏳ Waiting up to 5s for condition...")
    success = await wait_for_condition(check_something, timeout=5)
    if success:
        print("✅ Condition met!")
    else:
        print("⏰ Timeout!")


async def run(playwright: Playwright):
    chromium = playwright.chromium  # or "firefox" or "webkit".
    browser = await chromium.launch_persistent_context(
        user_data_dir="tmp/deepak",
        channel="chrome",
        headless=False,
    )

    page = await browser.new_page()
    await page.goto(
        "https://colab.research.google.com/drive/1mC9z9XcH3XfqTY8q7bZZLxwZT3hVmh1E"
    )

    await handle_page(page)

    await asyncio.sleep(2000)
    # first we need to check it try to connect automatic if it is the case how to handle
    # function name should be like that automatic_connect->bool
    # if not try to connecet we have to connect by our create function

    await select_additional_connection(page)
    await select_runtime(page)
    await select_gpu_by_selector(page)
    await select_cpu(page=page)
    await save_runtime_selection(page)
    status_info = await get_connection_status(page)
    if status_info["status"] != "connected":
        await click_connect(page)

    await page.wait_for_selector("#top-toolbar", timeout=30000)
    if await ensure_colab_connected(page):
        print("Proceeding with automation...")

        print("▶️ Starting sequential streaming execution...")
        selectors = await page.query_selector_all(".cell")
        # selector = selectors[0]
        await handle_cell(cell=selectors[0])
        await handle_cell_restart(page=page, cell=selectors[1])
        await asyncio.sleep(2)
        await handle_cell(cell=selectors[2])
        url = await handle_cell_last(cell=selectors[3])

        await asyncio.sleep(5)

        if url is not None:
            print(url)
            client = Client(url)
            result = client.predict(
                lang="hi",
                current_ref=handle_file(
                    "https://storage.googleapis.com/chatterbox-demo-samples/mtl_prompts/hi_f1.flac"
                ),
                current_text="पिछले महीने हमने एक नया मील का पत्थर छुआ: हमारे YouTube चैनल पर दो अरब व्यूज़।  पिछले महीने हमने एक नया मील का पत्थर छुआ: हमारे YouTube चैनल पर दो अरब व्यूज़।",
                api_name="/on_language_change",
            )

            print(result)
        # await run_cells_with_restart_handling(page)

        # handle restart document.querySelector("body > mwc-dialog > md-text-button:nth-child(3)").shadowRoot.querySelector("#button > span.touch")

    else:
        print("Cannot proceed without connection")
        await disconnect_and_delete_runtime(
            coordinates={
                "x": 923,
                "y": 333,
                "width": 194.34375,
                "height": 20,
                "top": 333,
                "right": 1117.34375,
                "bottom": 353,
                "left": 923,
            },
            page=page,
        )
        # await browser.close()
        # await run()

    # document.querySelector("div.main-content > div > div.codecell-input-output > div.inputarea.horizontal.layout.code > div.cell-gutter > div > colab-run-button").shadowRoot.querySelector("div").click()
    await asyncio.sleep(2000)


async def handle_cell(cell: ElementHandle):
    await cell.evaluate(
        expression=""" (cell) => {
            const button = cell.querySelector('colab-run-button');
            if(button){
                button.click()
            }
    } """
    )
    await asyncio.sleep(3)
    while True:
        result = await get_cell_state(cell)
        if result["data"]["isRunning"] is False:
            print(result)
            print(type(result["data"]["output"]))
            print("break")
            break

        await asyncio.sleep(1)


async def handle_cell_restart(page: Page, cell: ElementHandle):
    await cell.evaluate(
        expression=""" (cell) => {
            const button = cell.querySelector('colab-run-button');
            if(button){
                button.click()
            }
    } """
    )
    await asyncio.sleep(3)
    while True:
        result = await get_cell_state(cell)
        if result["data"]["isRunning"] is False:
            if await check_restart_dailog(page):
                await page.click(
                    selector="body > mwc-dialog > md-text-button:nth-child(3) >> #button > span.touch"
                )
                print(type(result["data"]["output"]))
                # check restart after connection to connected
                if await ensure_colab_connected(page):
                    print("awaiting for connected to server")
                    break

                print("break 1")
            else:
                # pass
                print(result)
                print(type(result["data"]["output"]))
                print("break 2")
                break

            # break
        else:
            if await check_restart_dailog(page):
                await page.click(
                    selector="body > mwc-dialog > md-text-button:nth-child(3) >> #button > span.touch"
                )
                print(type(result["data"]["output"]))
                print("break 3")
            else:
                # pass
                print(result)
                print(type(result["data"]["output"]))
                print("break 4")
        await asyncio.sleep(1)


# document.querySelector("body > mwc-dialog").shadowRoot.querySelector("div > div.mdc-dialog__container > div")
async def check_restart_dailog(dailog: Page) -> bool:
    try:
        await dailog.wait_for_selector(
            selector="body > mwc-dialog > md-text-button:nth-child(3) >> #button > span.touch",
        )
        return True
    except Exception as e:
        print(e)
        return False


async def handle_cell_last(cell: ElementHandle):
    await cell.evaluate(
        expression=""" (cell) => {
            const button = cell.querySelector('colab-run-button');
            if(button){
                button.click()
            }
    } """
    )
    await asyncio.sleep(3)
    url = ""
    hasUrl = False
    while True:
        result = await get_cell_state(cell)
        if result["data"]["isRunning"] is True:
            print(type(result["data"]["output"]))
            for log in result["data"]["output"]:
                if "Running on public URL" in log:
                    print(extract_url(log))
                    url = extract_url(log)
                    hasUrl = True
                    break
        if hasUrl:
            break
        await asyncio.sleep(1)

    return url


def extract_url(text):
    match = re.search(r"https?://[^\s]+", text)
    return match.group(0) if match else None


async def main():  # noqa: F811
    async with async_playwright() as playwright:
        await run(playwright)


if __name__ == "__main__":
    # print(segments)
    asyncio.run(main())
