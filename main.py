from grab import Scraper

national_scrape = Scraper(national=True,num_pages=10,synced=False)
#local_scrape = Scraper(local=True,num_pages=10,synced=False)
for c in [1,5,7,10,20,40,50,100,200,300,400,500,700,800,1000]:
	national_folder,time_lapse = national_scrape.run(chunking=c)	
#local_folder = local_scrape.run()
	print c,sum(time_lapse)/float(len(time_lapse))
