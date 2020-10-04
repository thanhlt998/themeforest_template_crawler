from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerProcess
import os

from spiders import ThemeForest
from settings import SETTINGS


def crawl_imdb():
    process.crawl(ThemeForest, name='theme_crawler',)


if __name__ == '__main__':
    if not os.path.exists('log'):
        os.makedirs('log')

    if os.path.exists(SETTINGS['LOG_FILE']):
        os.remove(SETTINGS['LOG_FILE'])

    settings = get_project_settings()
    settings.update(SETTINGS)

    process = CrawlerProcess(settings)

    configure_logging()

    crawl_imdb()
    process.start()
