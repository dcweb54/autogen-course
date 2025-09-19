import asyncio
import re
from playwright.async_api import Page, async_playwright
from typing import AsyncGenerator, Dict, Any, List

class ColabSequentialExecutor:
    def __init__(self):
        self._last_output = {}  # For diffing output between polls
        self.cell_outputs = []
        self.current_cell_index = 0
        self.execution_history = []

    async def get_cell_state(self, cell):
        """
        Get detailed execution state of a cell — matching JS getColabExecutionStatus() logic.
        Returns dict with:
          - success: bool
          - data: { isRunning, isFocused, hasError, output } or None
          - error: str (if failed)
        """
        try:
            state = await cell.evaluate('''(cell) => {
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
            }''')

            if not state.get("success", False):
                return {
                    "success": False,
                    "error": state.get("error", "Unknown error in JS evaluation"),
                    "data": None
                }

            return state

        except Exception as e:
            return {
                "success": False,
                "error": f"Python exception: {str(e)}",
                "data": None
            }

    async def extract_urls_from_text(self, text: str) -> List[str]:
        """Extract URLs from text"""
        if not text:
            return []

        url_patterns = [
            r'Running on public URL:?\s*([^\s]+)',
            r'Running on\s*([^\s]+)',
            r'Public URL:?\s*([^\s]+)',
            r'URL:?\s*([^\s]+)',
            r'(https?://[^\s]+)'
        ]

        urls = []
        for pattern in url_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                url = match[0] if isinstance(match, tuple) else match
                url = url.strip().rstrip('.,;:)\'"')
                if url and url not in urls:
                    urls.append(url)
        return urls

    async def run_cells_sequentially_streaming(self, page: Page) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Execute Colab cells STRICTLY one-by-one, with 2s polling and restart handling.
        Yields real-time events for UI/log consumption.
        """

        # ➤ Fetch all cells once
        cells = await page.query_selector_all(".cell")
        total_cells = len(cells)
        cell_index = 0
        max_restarts = 3
        restart_count = 0

        # ➤ Emit start event
        yield {
            "type": "execution_start",
            "data": {
                "total_cells": total_cells,
                "max_restarts": max_restarts
            }
        }

        # ➤ Process cells one-by-one
        while cell_index < total_cells and restart_count < max_restarts:
            current_cell = cells[cell_index]

            # ➤ Emit cell start
            yield {
                "type": "cell_start",
                "data": {
                    "cell_index": cell_index + 1,
                    "total_cells": total_cells
                }
            }

            try:
                # ▼▼▼ CHECK FOR RESTART BEFORE RUNNING ▼▼▼
                restart_dialog = await page.query_selector(
                    "body > mwc-dialog > md-text-button:nth-child(3) >> #button > span.touch"
                )
                if restart_dialog:
                    restart_count += 1
                    yield {
                        "type": "restart_detected",
                        "data": {
                            "restart_count": restart_count,
                            "message": "⚠️ Restart dialog detected before cell execution!"
                        }
                    }

                    # Click restart
                    await page.evaluate("""() => {
                        const btn = document.querySelector("body > mwc-dialog > md-text-button:nth-child(3)");
                        if (btn && btn.shadowRoot) {
                            const span = btn.shadowRoot.querySelector("#button > span.touch");
                            if (span) span.click();
                        }
                    }""")

                    # Wait for page to reload
                    await asyncio.sleep(10)
                    await page.wait_for_selector("#top-toolbar", timeout=30000)

                    yield {
                        "type": "restart_completed",
                        "data": {
                            "message": "🔄 Page restarted — restarting from Cell 1"
                        }
                    }

                    # Reset and restart from Cell 1
                    cells = await page.query_selector_all(".cell")  # Re-fetch cells after restart
                    total_cells = len(cells)
                    cell_index = 0
                    continue

                # ▼▼▼ CLICK RUN BUTTON ▼▼▼
                run_button = await current_cell.query_selector("colab-run-button")
                if run_button:
                    await run_button.evaluate(
                        '(btn) => btn.shadowRoot?.querySelector("div")?.click()'
                    )
                    yield {
                        "type": "run_button_clicked",
                        "data": {
                            "cell_index": cell_index + 1
                        }
                    }

                # ▼▼▼ POLL EVERY 2 SECONDS UNTIL CELL FINISHES ▼▼▼
                start_time = asyncio.get_event_loop().time()
                poll_timeout = 120  # 2 minutes max per cell
                finished = False

                while not finished and (asyncio.get_event_loop().time() - start_time) < poll_timeout:
                    try:
                        # Get detailed cell state
                        cell_status = await self.get_cell_state(current_cell)

                        if not cell_status["success"]:
                            yield {
                                "type": "cell_status_error",
                                "data": {
                                    "cell_index": cell_index + 1,
                                    "error": cell_status["error"]
                                }
                            }
                            # Break polling, move to next or retry
                            break

                        data = cell_status["data"]
                        is_running = data["isRunning"]
                        has_error = data["hasError"]
                        output_lines = data["output"] or []
                        current_output_text = "\n".join(output_lines)
                        print(current_output_text)

                        # ➤ Determine high-level status
                        if has_error:
                            status = "error"
                        elif not is_running and len(output_lines) > 0:
                            status = "completed"
                        elif is_running:
                            status = "running"
                        else:
                            status = "idle"

                        elapsed = int(asyncio.get_event_loop().time() - start_time)

                        # ➤ Emit status update
                        yield {
                            "type": "cell_status",
                            "data": {
                                "cell_index": cell_index + 1,
                                "status": status,
                                "is_running": is_running,
                                "has_error": has_error,
                                "is_focused": data.get("isFocused", False),
                                "output_line_count": len(output_lines),
                                "elapsed_seconds": elapsed
                            }
                        }

                        # ➤ Emit output update if changed
                        cell_key = f"cell_{cell_index}"
                        last_text = self._last_output.get(cell_key, "")

                        if current_output_text != last_text:
                            self._last_output[cell_key] = current_output_text

                            yield {
                                "type": "output_update",
                                "data": {
                                    "cell_index": cell_index + 1,
                                    "output_lines": output_lines,
                                    "full_text": current_output_text
                                }
                            }

                            # ➤ Extract and emit new URLs
                            all_urls = []
                            for line in output_lines:
                                urls_in_line = self.extract_urls_from_text(line)
                                for url in urls_in_line:
                                    if url not in all_urls:
                                        all_urls.append(url)
                                        yield {
                                            "type": "url_found",
                                            "data": {
                                                "cell_index": cell_index + 1,
                                                "url": url
                                            }
                                        }

                        # ▼▼▼ CHECK FOR RESTART DURING EXECUTION ▼▼▼
                        if await page.query_selector(
                            "body > mwc-dialog > md-text-button:nth-child(3) >> #button > span.touch"
                        ):
                            raise Exception("RESTART_DURING_EXECUTION")

                        # Wait 2 seconds before next poll
                        await asyncio.sleep(2)

                        # Check if done
                        if status in ("completed", "error"):
                            finished = True
                            break

                    except Exception as poll_error:
                        if "RESTART_DURING_EXECUTION" in str(poll_error):
                            restart_count += 1
                            yield {
                                "type": "restart_during_execution",
                                "data": {
                                    "restart_count": restart_count,
                                    "cell_index": cell_index + 1,
                                    "message": "⚠️ Restart detected during cell execution!"
                                }
                            }

                            await asyncio.sleep(5)
                            # Re-fetch cells and restart from Cell 1
                            cells = await page.query_selector_all(".cell")
                            total_cells = len(cells)
                            cell_index = 0
                            finished = True  # break inner loop
                            continue  # continue outer loop
                        else:
                            raise  # re-raise unexpected errors

                # ▲▲▲ END POLLING ▲▲▲

                if not finished:
                    # Timeout
                    yield {
                        "type": "cell_timeout",
                        "data": {
                            "cell_index": cell_index + 1,
                            "message": f"⏰ Cell execution timed out after {poll_timeout} seconds"
                        }
                    }
                    cell_index += 1
                    continue

                # ▼▼▼ FINAL STATE CHECK ▼▼▼
                final_check = await self.get_cell_state(current_cell)
                if final_check["success"]:
                    final_data = final_check["data"]
                    success = not final_data["hasError"] and not final_data["isRunning"]
                else:
                    success = False

                elapsed_final = int(asyncio.get_event_loop().time() - start_time)

                yield {
                    "type": "cell_finished",
                    "data": {
                        "cell_index": cell_index + 1,
                        "success": success,
                        "has_error": final_data.get("hasError", True) if final_check["success"] else True,
                        "elapsed_seconds": elapsed_final
                    }
                }

                if success:
                    cell_index += 1  # Move to next only on success
                else:
                    yield {
                        "type": "cell_failed",
                        "data": {
                            "cell_index": cell_index + 1,
                            "reason": "execution error or exception"
                        }
                    }
                    cell_index += 1

            except Exception as e:
                if "RESTART_DURING_EXECUTION" in str(e):
                    continue  # already handled
                yield {
                    "type": "error",
                    "data": {
                        "cell_index": cell_index + 1,
                        "error": str(e),
                        "message": f"❌ Unexpected error in cell {cell_index + 1}: {e}"
                    }
                }
                cell_index += 1

        # ➤ Final summary
        yield {
            "type": "execution_done",
            "data": {
                "completed_cells": cell_index,
                "total_cells": total_cells,
                "restarts": restart_count,
                "message": f"✅ Execution finished: {cell_index}/{total_cells} cells completed with {restart_count} restarts"
            }
        }


# ▶️ USAGE EXAMPLE — CLI CONSUMER
async def main():
    executor = ColabSequentialExecutor()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            # ⚠️ REPLACE WITH YOUR NOTEBOOK URL
            await page.goto("https://colab.research.google.com/drive/YOUR_NOTEBOOK_ID", timeout=60000)
            await page.wait_for_selector("#top-toolbar", timeout=30000)

            print("▶️ Starting sequential streaming execution...")

            async for event in executor.run_cells_sequentially_streaming(page):
                etype = event["type"]
                data = event["data"]

                if etype == "execution_start":
                    print(f"📋 Total cells: {data['total_cells']}, Max restarts: {data['max_restarts']}")

                elif etype == "cell_start":
                    print(f"\n--- 🚀 CELL {data['cell_index']} / {data['total_cells']} ---")

                elif etype == "run_button_clicked":
                    print("🖱️ Run button clicked — waiting for completion...")

                elif etype == "cell_status":
                    icon = "⏳" if data["status"] == "running" else "✅" if data["status"] == "completed" else "❌"
                    print(f"   {icon} [{data['elapsed_seconds']}s] Status: {data['status'].upper()} | Output lines: {data['output_line_count']}")

                elif etype == "output_update":
                    # Print only last 1-2 lines to avoid flooding
                    lines = data["output_lines"]
                    if len(lines) > 0:
                        last_line = lines[-1].strip()
                        if len(last_line) > 100:
                            last_line = last_line[:97] + "..."
                        print(f"   📝 {last_line}")

                elif etype == "url_found":
                    print(f"   🌐 URL → {data['url']}")

                elif etype == "restart_detected" or etype == "restart_during_execution":
                    print(f"🔁 {data['message']} (Total restarts: {data['restart_count']})")

                elif etype == "restart_completed":
                    print(f"   {data['message']}")

                elif etype == "cell_finished":
                    mark = "✅" if data["success"] else "❌"
                    print(f"{mark} Cell {data['cell_index']} finished in {data['elapsed_seconds']}s")

                elif etype == "cell_failed" or etype == "cell_timeout":
                    print(f"   ⚠️ {data['message']}")

                elif etype == "execution_done":
                    print(f"\n🎉 {data['message']}")

        except Exception as e:
            print(f"💥 Fatal error: {e}")
        finally:
            print("👋 Closing browser...")
            await browser.close()


if __name__ == "__main__":
    asyncio.run(main())