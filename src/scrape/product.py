import random
import re

from bs4 import BeautifulSoup


class Product:
    def __init__(self, html_content):
        self.soup = BeautifulSoup(html_content, "html.parser")

    def extract_title(self):
        meta_tag = self.soup.find("meta", attrs={"property": "og:title"})
        return meta_tag.get("content") if meta_tag else "No title found."

    def extract_url(self):
        url = self.soup.select_one('link[rel="canonical"]')
        return url.get("data-savepage-href") if url else "No url found."

    def extract_o_sku(self):
        o_sku = re.findall(r'\d+$', self.extract_url())
        o_sku = ''.join(o_sku)
        return o_sku

    def create_sku(self):
        return '21' + self.extract_o_sku()

    def find_description_section(self):
        return self.soup.find('div', attrs={'data-box-name': 'Description'})

    def extract_img_tags(self):
        return Product.find_description_section(self).find_all('img')

    def description(self):
        description_section = self.find_description_section()

        if not description_section:
            print("Element not found.")
            return

        # Find all div tags within parent tag of specified class
        divs = description_section.find_all('div', class_='mgn2_16 _0d3bd_am0a-')
        # For each div extract its html tags with content and merge them in single description
        description = ''.join(''.join(map(str, div.contents)) for div in divs)

        return description

    def price(self):
        price = float(self.soup.find("meta", attrs={"itemprop": "price"}).get("content"))
        return round(price / 2 * 20) / 20

    @staticmethod
    def generate_additional_attributes(skladom, original_sku, original_url, rating, sold, incoming):
        return (f'xxx_skladom={skladom},xxx_original_sku={original_sku},xxx_original_url={original_url},'
                f'xxx_rating={rating},xxx_sold={sold},xxx_incoming={incoming}')

    @staticmethod
    def rating():
        return round(random.uniform(4.65, 4.99), 2)

    @staticmethod
    def sold():
        return round(random.uniform(10, 200))

    def extract_images(self):
        return [tag['data-savepage-src'] for tag in self.extract_img_tags()]

    @staticmethod
    def additional_images(images):
        return ",".join(images[1:]) if len(images) > 1 else None

