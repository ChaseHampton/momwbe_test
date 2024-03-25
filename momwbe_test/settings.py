# Scrapy settings for momwbe_test project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "momwbe_test"

SPIDER_MODULES = ["momwbe_test.spiders"]
NEWSPIDER_MODULE = "momwbe_test.spiders"

ITEM_PIPELINES = {
    "momwbe_test.pipelines.MomwbeTestPipeline": 300,
    "momwbe_test.common.common_pipes.PhoneReplacePipeline": 350,
    "momwbe_test.common.common_pipes.StringStripperPipeline": 375,
    "momwbe_test.common.common_pipes.NullRemovalPipeline": 380,
    # "common-pipes.common_pipes.PhoneReplacePipeline": 350,
    # "common-pipes.common_pipes.StringStripperPipeline": 375,
    # "common-pipes.common_pipes.NullRemovalPipeline": 380,
    "momwbe_test.pipelines.MongoPipeline": 400,
}

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
