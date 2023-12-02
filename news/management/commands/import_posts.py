import json

import requests
from django.core.management.base import BaseCommand
from lxml import html

from news.models import Post

class Command(BaseCommand):
    help = 'Import posts into the database'

    def handle(self, *args, **kwargs):
        self.insert_database()

    def insert_database(self):
        data = self.extract_posts()

        for item in data:
            existing_post = Post.objects.filter(url=item['url']).first()
            if existing_post is None:
                post = Post(
                    url=item['url'],
                    name=item['name'],
                    tags=item['tags'],
                    image=item['image']
                )
                post.save()
                self.stdout.write(self.style.SUCCESS(f'Added post with URL {item["url"]}'))
            else:
                existing_post.name = item['name']
                existing_post.tags = item['tags']
                existing_post.image = item['image']
                existing_post.save()
                self.stdout.write(self.style.SUCCESS(f'Updated post with URL {item["url"]}'))

    def extract_posts(self):
        clean_text = lambda text: ','.join(text)
        output = []
        base_url = 'https://www.goal.com/en-ke'
        fieldnames = ['url', 'image', 'tags', 'name']
        response = requests.get(base_url)
        text = response.content
        doc = html.fromstring(text)

        list = doc.xpath(
            ".//ol[@class='grid-9-cards-double-mpu-breaking-news_layout__c7N6A']/li[contains(@data-type, 'CardComponent')]")

        for content in list:
            url = 'https://www.goal.com' + clean_text(
                content.xpath(".//a[contains(@data-testid,'card-image-url')]/@href"))
            image = clean_text(content.xpath('.//img/@src'))
            tags = content.xpath(".//div[contains(@class,'component-tag-list')]/a/text()")
            tags_links = ['https://www.goal.com'+i for i in content.xpath(".//div[contains(@class,'component-tag-list')]/a/@href")]
            tags = json.dumps([{'name': name, 'url': url} for name, url in zip(tags, tags_links)])
            name = clean_text(content.xpath(".//h3[contains(@class,'title')]/span/text()"))
            values = [url, image, tags, name]
            response = dict(zip(fieldnames, values))
            output.append(response)
        return output
