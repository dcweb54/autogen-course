from pixabay_scraper import PixabayScraper
import os


class VisualImageDownloader(PixabayScraper):
    def __init__(self, browser):
        super().__init__(browser)

    async def transcript_path(self, path: str):
        if not os.path.exists(path):
            print("not exist")
            return

    async def start_scraping(self):
        pass

    async def results(self):
        pass

    async def download(self):
        pass
