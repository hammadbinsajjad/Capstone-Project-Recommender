# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html


class BranchFallbackMiddleware:
    def process_response(self, request, response, spider):
        if not request.url.endswith("/README.md"):
            return response

        if not response.status == 404:
            return response

        if "main" in response.url:
            fallback_url = request.url.replace("/main/", "/master/")
            return request.replace(url=fallback_url)

        return response
