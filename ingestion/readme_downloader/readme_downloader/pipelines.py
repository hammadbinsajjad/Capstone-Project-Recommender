from scrapy.pipelines.files import FilesPipeline

from readme_downloader.helpers import raw_readme_url, repo_user, repo_name


class RawReadmeUrlsPipeline:
    def process_item(self, item, spider):
        return {"file_urls": list(map(raw_readme_url, item["repo_urls"]))}


class FilterReadmeUrlsPipeline:
    def process_item(self, item, spider):
        urls = item["file_urls"]
        return {"file_urls": urls[:spider.readme_limit or len(urls) + 1]}


class ReadmeFilesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        readme_url = request.url
        return f"{repo_user(readme_url)}_{repo_name(readme_url)}.md"
