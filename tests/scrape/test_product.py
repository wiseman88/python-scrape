import unittest

from src.scrape.product import Product


class TestProduct(unittest.TestCase):

    def setUp(self):
        self.html = """
        <html>
        <head>
            <meta property="og:title" content="Test Title" />
            <meta itemprop="price" content="69.99">
            <link rel="canonical" data-savepage-href="https://example.com/product-one-123456789" />
        </head>
        <body>
            <h1>Welcome to my website</h1>
            <div data-box-name="Description"><img data-savepage-src="https://img-1"/><img data-savepage-src="https://img-2"/><div class="mgn2_16 _0d3bd_am0a-"><h1>Test scrape</h1></div></div>
        </body>
        </html>
        """
        self.product_html = Product(self.html)
        self.description = '<div data-box-name="Description"><img data-savepage-src="https://img-1"/><img data-savepage-src="https://img-2"/><div class="mgn2_16 _0d3bd_am0a-"><h1>Test scrape</h1></div></div>'
        self.images_url = ['https://img-1', 'https://img-2', 'https://img-3']

    def test_extract_valid_title(self):
        self.assertEqual(self.product_html.extract_title(), "Test Title")

    def test_extract_url(self):
        url = Product.extract_url(self.product_html)
        self.assertEqual(url, "https://example.com/product-one-123456789")

    def test_extract_o_sku(self):
        o_sku = Product.extract_o_sku(self.product_html)
        self.assertEqual(o_sku, "123456789")

    def test_create_sku(self):
        sku = Product.create_sku(self.product_html)
        self.assertEqual(sku, "21123456789")

    def test_find_description_section(self):
        description = Product.find_description_section(self.product_html)
        self.assertEqual(str(description), str(self.description))

    def test_extract_img_tags(self):
        img_tags = Product.extract_img_tags(self.product_html)
        self.assertEqual(str(img_tags), str('[<img data-savepage-src="https://img-1"/>, <img data-savepage-src="https://img-2"/>]'))

    def test_description(self):
        description = Product.description(self.product_html)
        self.assertEqual(str(description), str('<h1>Test scrape</h1>'))

    def test_price(self):
        price = Product.price(self.product_html)
        self.assertEqual(price, 35.00)

    def test_extract_images(self):
        images = Product.extract_images(self.product_html)
        self.assertEqual(images, ['https://img-1', 'https://img-2'])

    def test_additional_images(self):
        additional_images = Product.additional_images(self.images_url)
        self.assertEqual(additional_images, 'https://img-2,https://img-3')

    def test_generate_additional_attributes(self):
        additional_attributes = Product.generate_additional_attributes(0, 123456, 'https://example.com', 4.65, 15, 0)
        expected = ("xxx_skladom=0,xxx_original_sku=123456,xxx_original_url=https://example.com,"
                    "xxx_rating=4.65,xxx_sold=15,xxx_incoming=0")
        self.assertEqual(additional_attributes, expected)


if __name__ == '__main__':
    unittest.main()
