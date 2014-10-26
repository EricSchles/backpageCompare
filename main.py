from grab import Scraper

national_scrape = Scraper(national=True,num_pages=10,synced=False)
local_scrape = Scraper(national=True,num_pages=10,synced=False)

national_folder = national_scrape.run()
local_folder = local_scrape.run()

