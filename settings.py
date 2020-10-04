SETTINGS = {
    'LOG_FILE': 'log/crawler.log',

    'ITEM_PIPELINES': {
        # 'scrapy.pipelines.images.ImagesPipeline': 300,
        'pipelines.MyFilesPipeline': 300,
    },

    'DEPTH_PRIORITY': 1,
    # 'CONCURRENT_REQUESTS': 1,
    # 'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
    'LOG_LEVEL': 'INFO',
    'HTTPERROR_ALLOWED_CODES': [301],
    'COOKIES_ENABLED': True,
    'COOKIES_DEBUG': True,
    'TELNETCONSOLE_PORT': None,
    'ROBOTSTXT_OBEY': False,
    'FEED_EXPORT_ENCODING': 'utf-8',
    'FEED_EXPORT': 'jsonlines',
    'REDIRECT_ENABLED': False,
    'FEED_URI': 'data/crawler_data/data.jsonl',
    # 'CLOSESPIDER_ITEMCOUNT': 1000,
    'DOWNLOAD_DELAY': 0.02,
    # 'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',

    'FILES_STORE': 'template/',
}
