from itemadapter import ItemAdapter
from pathlib import Path
from unidecode import unidecode
import yaml
import re


class PhoneReplacePipeline:
    def __init__(self):
        config_path = Path(__file__).parent / "regs.yaml"
        self.config = yaml.safe_load(config_path.open())
        self.phone_regex = re.compile(self.config["regex"][0]["pattern"])

    def process_item(self, item, spider):
        i = ItemAdapter(item)
        for k, v in i.items():
            if not isinstance(v, str):
                continue
            i[k] = self._parse_phone(k, v)
        return i.asdict()

    def _parse_phone(self, key: str, val: str) -> str:
        phone_match = re.match(self.phone_regex, val)
        if not phone_match:
            return val
        if any([x in key.lower() for x in ["naics", "commodity", "certification"]]):
            return val
        if not any([x in key.lower() for x in ["phone", "fax", "cell", "contact"]]):
            return val
        country_code = (
            re.sub(r"[^\d]", "", phone_match.group("ccode").strip())
            if phone_match.group("ccode")
            else ""
        )
        area_code = (
            re.sub(r"[^\d]", "", phone_match.group("acode").strip())
            if phone_match.group("acode")
            else ""
        )
        primary_number = (
            re.sub(r"[^\d]", "", phone_match.group("primnum").strip())
            if phone_match.group("primnum")
            else ""
        )
        return f"{country_code}{area_code}{primary_number}"


class UnidecodePipeline:
    def process_item(self, item, spider):
        i = ItemAdapter(item)
        for k, v in i.items():
            if isinstance(v, str):
                i[k] = unidecode(v)
        return i.asdict()


class StringStripperPipeline:
    def process_item(self, item, spider):
        i = ItemAdapter(item)
        for k, v in i.items():
            if isinstance(v, str):
                i[k] = v.strip()
        return i.asdict()


class NullRemovalPipeline:
    def process_item(self, item, spider):
        i = ItemAdapter(item)
        for k, v in i.items():
            if v is None:
                i[k] = ""
            elif isinstance(v, str) and v.lower() == "null" or v.lower() == "none":
                i[k] = ""
        return i.asdict()
