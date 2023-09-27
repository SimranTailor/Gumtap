import scrapy
import re
from scrapy.exporters import CsvItemExporter

class Project1Spider(scrapy.Spider):
    name = 'project_1'
    base_url = 'https://www.amazon.com'

    # Defining the category URLs and names
    category_urls = [
        ('https://www.amazon.com/gp/new-releases/amazon-devices/ref=zg_bsnr_nav_amazon-devices_0', 'Amazon Devices & Accessories'),
        ('https://www.amazon.com/gp/new-releases/amazon-renewed/ref=zg_bsnr_nav_amazon-renewed_0', 'Amazon Renewed'),
        ('https://www.amazon.com/gp/new-releases/appliances/ref=zg_bsnr_nav_appliances_0', 'Appliances'),
        ('https://www.amazon.com/gp/new-releases/mobile-apps/ref=zg_bsnr_nav_mobile-apps_0', 'Apps & Games'),
        ('https://www.amazon.com/gp/new-releases/arts-crafts/ref=zg_bsnr_nav_arts-crafts_0', 'Arts, Crafts & Sewing'),
        ('https://www.amazon.com/gp/new-releases/audible/ref=zg_bsnr_nav_audible_0', 'Audible Books & Originals'),
        ('https://www.amazon.com/gp/new-releases/automotive/ref=zg_bsnr_nav_automotive_0', 'Automotive'),
        ('https://www.amazon.com/gp/new-releases/baby-products/ref=zg_bsnr_nav_baby-products_0', 'Baby'),
        ('https://www.amazon.com/gp/new-releases/beauty/ref=zg_bsnr_nav_beauty_0', 'Beauty & Personal Care'),
        ('https://www.amazon.com/gp/new-releases/books/ref=zg_bsnr_nav_books_0', 'Books'),
        ('https://www.amazon.com/gp/new-releases/photo/ref=zg_bsnr_nav_photo_0', 'Camera & Photo Products'),
        ('https://www.amazon.com/gp/new-releases/music/ref=zg_bsnr_nav_music_0', 'CDs & Vinyl'),
        ('https://www.amazon.com/gp/new-releases/wireless/ref=zg_bsnr_nav_wireless_0', 'Cell Phones & Accessories'),
        ('https://www.amazon.com/gp/new-releases/climate-pledge/ref=zg_bsnr_nav_climate-pledge_0', 'Climate Pledge Friendly'),
        ('https://www.amazon.com/gp/new-releases/fashion/ref=zg_bsnr_nav_fashion_0', 'Clothing, Shoes & Jewelry'),
        ('https://www.amazon.com/gp/new-releases/coins/ref=zg_bsnr_nav_coins_0', 'Collectible Coins'),
        ('https://www.amazon.com/gp/new-releases/pc/ref=zg_bsnr_nav_pc_0', 'Computers & Accessories'),
        ('https://www.amazon.com/gp/new-releases/digital-educational-resources/ref=zg_bsnr_nav_digital-educational-resources_0', 'Digital Educational Resources'),
        ('https://www.amazon.com/gp/new-releases/dmusic/ref=zg_bsnr_nav_dmusic_0', 'Digital Music'),
        ('https://www.amazon.com/gp/new-releases/electronics/ref=zg_bsnr_nav_electronics_0', 'Electronics'),
        ('https://www.amazon.com/gp/new-releases/entertainment-collectibles/ref=zg_bsnr_nav_entertainment-collectibles_0', 'Entertainment Collectibles'),
        ('https://www.amazon.com/gp/new-releases/handmade/ref=zg_bsnr_nav_handmade_0', 'Handmade Products'),
        ('https://www.amazon.com/gp/new-releases/home-garden/ref=zg_bsnr_nav_home-garden_0', 'Home & Kitchen'),
        ('https://www.amazon.com/gp/new-releases/digital-text/ref=zg_bsnr_nav_digital-text_0', 'Kindle Store'),
        ('https://www.amazon.com/gp/new-releases/kitchen/ref=zg_bsnr_nav_kitchen_0', 'Kitchen & Dining'),
        ('https://www.amazon.com/gp/new-releases/movies-tv/ref=zg_bsnr_nav_movies-tv_0', 'Movies & TV'),
        ('https://www.amazon.com/gp/new-releases/musical-instruments/ref=zg_bsnr_nav_musical-instruments_0', 'Musical Instruments'),
        ('https://www.amazon.com/gp/new-releases/office-products/ref=zg_bsnr_nav_office-products_0', 'Office Products'),
        ('https://www.amazon.com/gp/new-releases/lawn-garden/ref=zg_bsnr_nav_lawn-garden_0', 'Patio, Lawn & Garden'),
        ('https://www.amazon.com/gp/new-releases/pet-supplies/ref=zg_bsnr_nav_pet-supplies_0', 'Pet Supplies'),
        ('https://www.amazon.com/gp/new-releases/sporting-goods/ref=zg_bsnr_nav_sporting-goods_0', 'Sports & Outdoors'),
        ('https://www.amazon.com/gp/new-releases/sports-collectibles/ref=zg_bsnr_nav_sports-collectibles_0', 'Sports Collectibles'),
        ('https://www.amazon.com/gp/new-releases/hi/ref=zg_bsnr_nav_hi_0', 'Tools & Home Improvement'),
        ('https://www.amazon.com/gp/new-releases/toys-and-games/ref=zg_bsnr_nav_toys-and-games_0', 'Toys & Games'),
        ('https://www.amazon.com/gp/new-releases/boost/ref=zg_bsnr_nav_boost_0', 'Unique Finds'),
        ('https://www.amazon.com/gp/new-releases/videogames/ref=zg_bsnr_nav_videogames_0', 'Video Games'),
    ]

    def __init__(self):
        self.visited_asins = set()  # Initialized a set to store visited ASINs
        self.current_category_index = 0  # Initialized the current category index

    def start_requests(self):
        # Start with the first category
        category_url, category_name = self.category_urls[self.current_category_index]
        yield scrapy.Request(url=category_url, meta={'category_name': category_name}, callback=self.parse)

    def parse(self, response):
    
        category_name = response.meta.get('category_name', '')

        # Extracting ASINs using a more specific regex
        page_content = response.text
        asin_matches = re.findall(r'/dp/([A-Z0-9]+)/', page_content)
        for asin in asin_matches:
            if asin not in self.visited_asins:  # Check for duplicates
                self.visited_asins.add(asin)
                yield {
                    'Category': category_name,
                    'ASIN': asin
                }

        # Extracting next page URL
        next_page = response.css('li.a-last a::attr(href)').extract_first()
        if next_page:
            next_page_url = self.base_url + next_page
            yield scrapy.Request(url=next_page_url, meta={'category_name': category_name}, callback=self.parse)
        else:
            # If there is no next page, move to the next category
            self.current_category_index += 1
            if self.current_category_index < len(self.category_urls):
                category_url, category_name = self.category_urls[self.current_category_index]
                yield scrapy.Request(url=category_url, meta={'category_name': category_name}, callback=self.parse)
