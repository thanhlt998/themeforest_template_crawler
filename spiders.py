from scrapy import Request, Spider
from scrapy.responsetypes import Response
import re


def check_image(path):
    return re.match(r'.+(png|jpg|jpeg)$', path)


def check_relative_url(path: str):
    return not path.startswith('https://')


class ThemeForest(Spider):
    html_url = "//a[contains(@href,'.html') and not(contains(@href,'#'))]/@href"
    js_script_url = "//script[@src]/@src"
    css_url = "//link[@rel='stylesheet']/@href"
    img_src = "//img/@src"
    icon = "//link[@rel='icon']/@href"

    def __init__(self, name=None, **kwargs):
        super(ThemeForest, self).__init__(name=name, **kwargs)
        self.start_urls = [
            'http://themescare.com/demos/filmoja-view/',
        ]
        self.visited_urls = set()
        self.not_visited_urls = set()
        self.js_urls = set()
        self.css_urls = set()
        self.image_urls = set()

    def start_requests(self):
        yield Request(
            url=self.start_urls[0],
            callback=self.parse,
            meta={'url': 'index.html'}
        )

    def parse(self, response: Response):
        self.parse_html(response)

        meta = response.meta
        if meta.get('url') is not None:
            self.visited_urls.add(response.urljoin(meta.get('url')))
        html_urls = response.xpath(self.html_url).getall()
        html_urls = list(set(html_urls))
        html_urls = [response.urljoin(url) for url in html_urls]

        for html_url in html_urls:
            if html_url not in self.visited_urls and html_url not in self.not_visited_urls:
                self.not_visited_urls.add(html_url)

        if len(self.not_visited_urls) > 0:
            url = self.not_visited_urls.pop()
            # print(url, type(url))
            self.visited_urls.add(url)
            yield Request(
                url=response.urljoin(url),
                callback=self.parse,
            )
        else:
            if len(self.css_urls) == 0:
                yield {
                    'file_urls': [
                        *self.visited_urls,
                        *self.js_urls,
                        *self.css_urls,
                        *self.image_urls,
                    ],
                }
            else:
                css_urls = list(set(self.css_urls))
                yield Request(
                    url=css_urls[0],
                    callback=self.parse_img_from_css,
                    meta={'css_urls': css_urls[1:]}
                )

    def parse_html(self, response: Response):
        self.js_urls.update([response.urljoin(url) for url in response.xpath(self.js_script_url).getall()])
        self.css_urls.update([response.urljoin(url) for url in response.xpath(self.css_url).getall()])

        img_srcs = response.xpath(self.img_src).getall()
        icon = response.xpath(self.icon).get()
        self.image_urls.update([response.urljoin(url) for url in [*img_srcs, icon]])

    def parse_img_from_css(self, response: Response):
        css_content = response.text
        img_urls = [s[1] for s in re.findall(r"url\(('?)([^)]+)\1\)", css_content)]
        self.image_urls.update([response.urljoin(url) for url in img_urls if check_relative_url(url)])

        css_urls = response.meta.get('css_urls', [])

        if len(css_urls) > 0:
            yield Request(
                url=css_urls[0],
                callback=self.parse_img_from_css,
                meta={'css_urls': css_urls[1:]}
            )
        else:
            yield {
                'file_urls': [
                    *self.visited_urls,
                    *self.js_urls,
                    *self.css_urls,
                    *self.image_urls,
                ],
            }

