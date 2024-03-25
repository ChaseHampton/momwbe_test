# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MomwbeTestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    FirmName = scrapy.Field()
    CertificationType = scrapy.Field()
    Region = scrapy.Field()
    FirmAddress = scrapy.Field()
    FirmPhone = scrapy.Field()
    FirmEmail = scrapy.Field()
    PrimaryCommodityOrServiceProvided = scrapy.Field()
    PrimaryContact = scrapy.Field()
    PrimaryPhone = scrapy.Field()
    PrimaryEmail = scrapy.Field()
    SecondaryContact = scrapy.Field()
    SecondaryPhone = scrapy.Field()
    SecondaryEmail = scrapy.Field()
    Website = scrapy.Field()
    CertificationDate = scrapy.Field()
    ExpirationDate = scrapy.Field()
    CertificationNumber = scrapy.Field()
    SuspendedFromDate = scrapy.Field()
    SuspendedToDate = scrapy.Field()
    NaicsCodes = scrapy.Field()
