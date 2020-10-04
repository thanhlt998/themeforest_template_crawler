import os
from urllib.parse import urlparse
from scrapy import Request

from scrapy.pipelines.files import FilesPipeline


class MyFilesPipeline(FilesPipeline):

    def file_path(self, request, response=None, info=None):
        path = 'files/' + urlparse(request.url).path

        return path
    
    # def get_media_requests(self, item, info):
    #     urls = item.get(self.files_urls_field, [])
    #     return [Request(url=u['full'], meta={'origin': u['origin']}) for u in urls]
