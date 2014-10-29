from grab import Scraper

#national_scrape = Scraper(national=True,num_pages=10,synced=False)
local_scrape = Scraper(local=True,num_pages=10,synced=False)
#for c in [200,300,400,500,700,800,1000]:
	#national_folder,time_lapse = national_scrape.run(chunking=c)	
local_folder = local_scrape.run(chunking=10,debug=True)
	#print c,sum(time_lapse)/float(len(time_lapse))
