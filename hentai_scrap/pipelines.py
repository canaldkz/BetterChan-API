# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exceptions import DropItem
from database.models import Manga, Drop, Error
from hentai_scrap.utils import mdb
from typing import Union


class HentaiScrapPipeline:
    def __init__(self):
        pass

    def close_spider(self, spider):
        mdb.close()

    def process_item(self, item: Union[Manga, Drop, Error], spider):
        if isinstance(item, Error):
            raise DropItem(f"An unexpected exception while parsing {item.url}")

        if isinstance(item, Drop):
            raise DropItem(f"Duplicate found of {item.Id}")

        mdb.save(item)
        return item
