# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from itemadapter import ItemAdapter
import pymongo
from momwbe_test.db import Db
from momwbe_test.items import MomwbeTestItem
from unidecode import unidecode


class MomwbeTestPipeline:
    def __init__(self):
        self.db = Db()

    def process_item(self, item, spider):
        yielded_item = ItemAdapter(item)
        mod = yielded_item.get("modal")
        i = MomwbeTestItem()

        # Extracting and populating the values into the item
        i["FirmName"] = mod.xpath(
            '//input[@name="ctl00$MainContent$ucBusinessInformationPopup$tbFirmName"]/@value'
        ).get()
        i["CertificationType"] = mod.xpath(
            '//input[@name="ctl00$MainContent$ucBusinessInformationPopup$tbCertificationType"]/@value'
        ).get()
        i["Region"] = mod.xpath(
            '//input[@name="ctl00$MainContent$ucBusinessInformationPopup$tbRegion"]/@value'
        ).get()
        i["FirmAddress"] = mod.xpath(
            '//input[@name="ctl00$MainContent$ucBusinessInformationPopup$tbFirmAddress"]/@value'
        ).get()
        i["FirmPhone"] = mod.xpath(
            '//input[@name="ctl00$MainContent$ucBusinessInformationPopup$tbFirmPhone"]/@value'
        ).get()
        i["FirmEmail"] = mod.xpath(
            '//input[@name="ctl00$MainContent$ucBusinessInformationPopup$tbFirmEmail"]/@value'
        ).get()
        i["PrimaryCommodityOrServiceProvided"] = mod.xpath(
            '//textarea[@name="ctl00$MainContent$ucBusinessInformationPopup$tbPrimaryCommodityOrService"]/text()'
        ).get()
        i["PrimaryContact"] = mod.xpath(
            '//input[@name="ctl00$MainContent$ucBusinessInformationPopup$tbPrimaryContact"]/@value'
        ).get()
        i["PrimaryPhone"] = mod.xpath(
            '//input[@name="ctl00$MainContent$ucBusinessInformationPopup$tbPrimaryContactPhone"]/@value'
        ).get()
        i["PrimaryEmail"] = mod.xpath(
            '//input[@name="ctl00$MainContent$ucBusinessInformationPopup$tbPrimaryContactEmail"]/@value'
        ).get()
        i["SecondaryContact"] = mod.xpath(
            '//input[@name="ctl00$MainContent$ucBusinessInformationPopup$tbSecondaryContact"]/@value'
        ).get()
        i["SecondaryPhone"] = mod.xpath(
            '//input[@name="ctl00$MainContent$ucBusinessInformationPopup$tbSecondaryContactPhone"]/@value'
        ).get()
        i["SecondaryEmail"] = mod.xpath(
            '//input[@name="ctl00$MainContent$ucBusinessInformationPopup$tbSecondaryContactEmail"]/@value'
        ).get()
        i["Website"] = mod.xpath(
            '//input[@name="ctl00$MainContent$ucBusinessInformationPopup$tbWebsite"]/@value'
        ).get()
        i["CertificationDate"] = mod.xpath(
            '//input[@name="ctl00$MainContent$ucBusinessInformationPopup$tbCertificationDate"]/@value'
        ).get()
        i["ExpirationDate"] = mod.xpath(
            '//input[@name="ctl00$MainContent$ucBusinessInformationPopup$tbExpirationDate"]/@value'
        ).get()
        i["CertificationNumber"] = mod.xpath(
            '//input[@name="ctl00$MainContent$ucBusinessInformationPopup$tbCertificationID"]/@value'
        ).get()
        i["SuspendedFromDate"] = mod.xpath(
            '//input[@name="ctl00$MainContent$ucBusinessInformationPopup$tbSuspendedFromDate"]/@value'
        ).get()
        i["SuspendedToDate"] = mod.xpath(
            '//input[@name="ctl00$MainContent$ucBusinessInformationPopup$tbSuspendedToDate"]/@value'
        ).get()
        i["NaicsCodes"] = self._get_codes(mod)

        self.db.mark_searched(yielded_item["id"])
        return i

    def _get_codes(self, mod) -> str:
        code_rows = mod.xpath('.//table[contains(@class, "table-striped")]/tbody/tr')
        codes = []
        for row in code_rows:
            codes.append(row.xpath(".//td[1]/text()").get())
        return ";".join(codes)


class MongoPipeline:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["momwbe"]

    def process_item(self, item, spider):
        col = self.db[f"momwbe_{spider.run_id}"]
        col.insert_one(ItemAdapter(item).asdict())
        return item
