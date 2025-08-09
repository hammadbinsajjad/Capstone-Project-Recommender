from csv import DictReader

from scrapy.spiders import Spider


class ReadmeSpider(Spider):
    name = "readme-spider"
    start_urls = [
        "https://datatalksclub-projects.streamlit.app/~/+/media/"
        "7b948d81e15dee2f7779dec468f18dad36345efba3cbb7ba7ec90c09.csv"
    ]

    def __init__(self, limit=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.readme_limit = limit

    def parse(self, response):
        project_data_reader = DictReader(response.text.split("\n"))
        return {"repo_urls": [project_data["project_url"] for project_data in project_data_reader]}
