import re
import scrapy
from scrapy.exceptions import CloseSpider
from momwbe_test.db import Db


class SearchException(Exception):
    pass


class MomwbeSpider(scrapy.Spider):
    name = "momwbe"
    allowed_domains = ["apps1.mo.gov"]
    start_urls = ["https://apps1.mo.gov/MWBCertifiedFirms/"]

    def __init__(self, reset=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = Db()
        if isinstance(reset, str):
            reset = reset.lower() in ("true", "1")
        if reset:
            self.db.drop_table()
        self.db.create_table()
        self.run_id = self.db.log_run()

    def parse(self, response):
        formdata = {
            "ctl00$ctl12": "ctl00$MainContent$upMain|ctl00$MainContent$btnSearch",
            "ctl00$MainContent$btnSearch": "Search",
        }
        yield scrapy.FormRequest.from_response(
            response,
            formdata=formdata,
            meta={"page": 1},
            dont_filter=True,
            callback=self.dispatch_details,
        )

    async def dispatch_details(self, response):
        if "orig_response" in response.meta:
            for r in self.business_details(response, response.meta["orig_response"]):
                yield r
        else:
            for r in self.business_details(response, response):
                yield r

        page_form = {}
        async for x in self._form_parse(response):
            page_form.update(x)
        page_form.update(
            {
                "ctl00$ctl12": f"ctl00$MainContent$upMain|ctl00$MainContent$lvFirms$ucULDFirms$ctl02$ctl00",
                "ctl00$MainContent$ddlCertificationType": "",
                "ctl00$MainContent$ddlRegion": "",
                "__EVENTTARGET": f"ctl00$MainContent$lvFirms$ucULDFirms$ctl02$ctl00",
            }
        )
        pager = (
            response.xpath('//ul[contains(@class, "pagination")]/li')[-1]
            if response.xpath('//ul[contains(@class, "pagination")]/li')
            else None
        )
        if not pager:
            raise CloseSpider("End of pages.")

        if (
            response.xpath('//ul[contains(@class, "pagination")]/li/@class')[-1]
            != "disabled"
        ):
            yield scrapy.FormRequest(
                url="https://apps1.mo.gov/MWBCertifiedFirms/FirmSearch.aspx",
                formdata=page_form,
                headers={
                    # "X-MicrosoftAjax": "Delta=true",
                    "X-Requested-With": "XMLHttpRequest",
                },
                method="POST",
                meta={"orig_response": response},
                dont_filter=True,
                callback=self.dispatch_details,
            )
        else:
            raise CloseSpider("No more pages to search.")

    def get_details(self, response):
        mod = response.xpath('//div[contains(@class, "modal-content")]')
        yield {
            "modal": mod,
            "id": response.meta["id"],
        }

    async def _form_parse(self, response):
        for input in [
            x
            for x in response.xpath("//input")
            if re.match(r"^__|^ctl", x.attrib["name"]) and x.attrib["type"] != "submit"
        ]:
            yield {
                input.attrib["name"]: (
                    input.attrib["value"] if "value" in input.attrib else ""
                ),
            }

    def business_details(self, response, orig_response):
        businesses = response.xpath(
            '//table[contains(@class, "table-striped")]//tbody//tr'
        )
        for ix, b in enumerate(businesses):
            business = b.xpath(".//td[2]//text()").get().strip()
            id = self.db.insert_search(business)
            if not id:
                id = self.db.lookup_id(business)
                if not id:
                    self.logger.error(
                        f"Failed to insert or lookup ({id=}, {business=})"
                    )
                self.logger.info(
                    f"Skipping ({id=}, {business=}) as it was already searched."
                )
                continue
            formdata = {
                "ctl00$ctl12": f"ctl00$MainContent$upMain|ctl00$MainContent$lvFirms$ctrl{ix}$btnMoreInformation",
                f"ctl00$MainContent$lvFirms$ctrl{ix}$btnMoreInformation": "More Information",
            }
            m = {"id": id, "bus_name": business}
            yield scrapy.FormRequest.from_response(
                orig_response,
                formdata=formdata,
                meta=m,
                dont_filter=True,
                callback=self.get_details,
            )
