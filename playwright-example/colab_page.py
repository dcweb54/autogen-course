from gradio_client import Client, handle_file
from colab_additional_option import AdditionalOption
from patchright.async_api import Page
from colab_connection import ColabConnection, ConnectionStatus
from colab_notebook import ColabNoteBook


class ColabPage:
    def __init__(self, page: Page):
        self.page = page
        self.max_try_connection = 3

    async def handle_page_v2(self):
        print("handle_page_v2")
        connection = self.connection()
        addition = self.additional_optional()
        
        connect_status = await connection.wait_for_colab_toolbar_button_status(
            timeout=10
        )
        
        if connect_status is ConnectionStatus.Connected:
            print("already connected")
            notebook = self.notebook()
            # await notebook.handle_notebook()
            selectors = await self.page.query_selector_all(".cell")
            await notebook.handle_cell(cell=selectors[0])
            await notebook.handle_cell_with_restart(cell=selectors[1])
            # await notebook.handle_restart()
            if await notebook.is_cell_restart():
                await self.page.click(
                    selector="body > mwc-dialog > md-text-button:nth-child(3) >> #button > span.touch"
                )
                await self.handle_page_v2()

            await notebook.handle_cell(cell=selectors[2])
            url = await notebook.handle_cell_with_url(cell=selectors[3])

            print(f"get url {url}")
            return  url
        elif connect_status is ConnectionStatus.Connect:
            print("Connect to a new runtime")
            await connection.click_at_connect_by_selector()
            await self.handle_page_v2()
        elif connect_status is ConnectionStatus.Reconnect:
            print("click to connect")
            await connection.click_at_connect_by_selector()
            await self.handle_page_v2()
        elif connect_status is ConnectionStatus.Connecting:
            print("wait for connection established")
            if self.max_try_connection == 0:
                print(f"max try finished {self.max_try_connection}")
                print("needs to be disconnected and deleted")
                await addition.handle_additional_option(connect_status)
                await self.handle_page_v2()
            else:
                print(f"current try {self.max_try_connection}")
                self.max_try_connection -= 1
                await self.handle_page_v2()
        elif connect_status is None:
            print("unkwon")

    async def handle_page(self):
        connection_status = await self.connection().wait_for_connection_status()
        if connection_status is not None:
            if connection_status is ConnectionStatus.Connected:
                print(f"Result {connection_status}")
                print("cell operation must be started")

            elif connection_status is ConnectionStatus.Connect:
                print(f"Result {connection_status}")
                # await self.additional_optional().handle_additional_option(
                #     connection_status=connection_status
                # )
                # await self.connection().click_at_connect_by_selector()
                # await self.handle_page()

            elif connection_status is ConnectionStatus.Reconnect:
                print(f"Result {connection_status}")
                print("click the reconnet button")
                # await self.additional_optional().handle_additional_option(
                #     connection_status=connection_status
                # )
                # await self.connection().click_at_connect_by_selector()
                # await self.handle_page()

            elif connection_status is ConnectionStatus.Connecting:
                print(f"Result {connection_status}")
                print("we need to disconnect and delete runtime")
                await self.additional_optional().handle_additional_option(
                    connection_status=connection_status
                )
                await self.connection().click_at_connect_by_selector()
                await self.handle_page()

            else:
                print(f"Result {connection_status}")
                print("unkwron operation should be handle later")
        else:
            print("something Error from connection ")

    def connection(self):
        return ColabConnection(self.page)

    def additional_optional(self):
        return AdditionalOption(self.page)

    def notebook(self):
        return ColabNoteBook(self.page)
