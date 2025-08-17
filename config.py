# config.py

# BASE_URL = "https://www.theknot.com/marketplace/wedding-reception-venues-atlanta-ga"
# CSS_SELECTOR = "[class^='info-container']"
# REQUIRED_KEYS = [
#     "name",
#     "price",
#     "location",
#     "capacity",
#     "rating",
#     "reviews",
#     "description",
# ]

BASE_URL = "https://www.weddingwire.com/shared/search?id_grupo=1&id_sector=&id_region=&id_provincia=10022&id_poblacion=&id_geozona=&geoloc=&latitude=&longitude=&isBrowseByImagesEnabled=&keyword=&faqs%5B%5D=&capacityRange%5B%5D=&txtStrSearch=Wedding+Venues&txtLocSearch=Atlanta+%28Area%29"

# CSS selector for WeddingWire venue listings (targeting just the essential venue info)
CSS_SELECTOR = "[class*='vendorTile__content'] h2, [class*='vendorTile__content'] div:nth-child(2), [class*='vendorTile__content'] div:nth-child(4)"

# This targets: venue name (h2), location (2nd div), and price/capacity (4th div)

# Alternative: Just the main content area
# CSS_SELECTOR = "[class*='vendorTile__content']"

# Alternative selectors to try if needed:
# CSS_SELECTOR = ".vendorTile__content"
# CSS_SELECTOR = "[class*='vendorTile']"

# Alternative selectors to try if needed:
# CSS_SELECTOR = ".vendorTile__content"
# CSS_SELECTOR = "[class*='vendorTile']"
REQUIRED_KEYS = [
    "name",
    "price",
    "location",
    "capacity",
    "rating",
    "reviews",
    "description",
]
