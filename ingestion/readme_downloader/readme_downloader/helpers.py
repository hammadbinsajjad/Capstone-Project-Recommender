from urllib.parse import urlparse


def repo_user(repo_url):
    parsed_url = urlparse(repo_url)
    return parsed_url.path.split("/")[1].strip("/")


def repo_name(repo_url):
    parsed_url = urlparse(repo_url)
    return parsed_url.path.split("/")[2].strip("/")


def raw_readme_url(repo_url):
    owner_name, repository_name = repo_user(repo_url), repo_name(repo_url)
    return f"https://raw.githubusercontent.com/{owner_name}/{repository_name}/main/README.md"
