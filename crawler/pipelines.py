from scrapy.exceptions import DropItem
import pandas as pd


class DuplicatesPipeline:
    def __init__(self):
        self.courses = pd.read_csv("courses.csv")

    def process_item(self, item, spider):
        item_exists = (
                (self.courses['title'] == item['title']) &
                (self.courses['course_url'] == item['course_url'])
        ).any()
        if item_exists:
            raise DropItem(f"Duplicate item found: {item}")
        else:
            self.courses.loc[len(self.courses)] = list(item.values())
            return item

    def close_spider(self, spider):
        self.courses.to_csv("courses.csv", index=False)
