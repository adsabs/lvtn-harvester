# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from .items import ItemFruit, ItemSeed


class FruitPipeline:
    def process_item(self, item, spider):
        if isinstance(item, ItemSeed):
            return item
        elif isinstance(item, ItemFruit):
            return item
