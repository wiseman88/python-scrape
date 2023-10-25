import random
import re

from bs4 import BeautifulSoup


class Product:
    def __init__(self, html_content):
        self.soup = BeautifulSoup(html_content, "html.parser")

    @staticmethod
    def extract_title(soup):
        meta_tag = soup.find("meta", attrs={"property": "og:title"})
        return meta_tag.get("content") if meta_tag else "No title found."

    @staticmethod
    def extract_url(soup):
        url = soup.select_one('link[rel="canonical"]')
        return url.get("data-savepage-href") if url else "No url found."

    @staticmethod
    def extract_o_sku(soup):
        o_sku = re.findall(r'\d+$', Product.extract_url(soup))
        o_sku = ''.join(o_sku)
        return o_sku

    @staticmethod
    def create_sku(soup):
        return '21' + Product.extract_o_sku(soup)

    @staticmethod
    def find_description_section(soup):
        return soup.find('div', attrs={'data-box-name': 'Description'})

    @staticmethod
    def extract_img_tags(desc_section):
        return desc_section.find_all('img')

    @staticmethod
    def description(html):
        if html:
            desc = html.find_all('div', class_='mgn2_16 _0d3bd_am0a-')
            description = ''
            for div in desc:
                div_content = ''.join(map(str, div.contents))
                description += div_content
        else:
            print("Element not found.")

    @staticmethod
    def price(soup):
        price = float(soup.find("meta", attrs={"itemprop": "price"}).get("content"))
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

    @staticmethod
    def extract_images(img_tags):
        return [tag['data-savepage-src'] for tag in img_tags]

    @staticmethod
    def additional_images(images):
        return ",".join(images[1:]) if len(images) > 1 else None

