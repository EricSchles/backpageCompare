import requests
import lxml.html
import pickle
import grequests
import os
import pandas as pd
import time
import hashlib

"""
To Do:
national scrape is not being written to
fix formatting for local scrape
"""
class Scraper:
    def __init__(self,national=False,local=False,num_pages=5,synced=True):
        if national:
            assert local == False
        if local:
            assert national == False
        
        self.national = national
        self.local = local
        if national:
            if not os.path.exists("backpages"):
                self.get_all_backpages()
        if local:
            if not os.path.exists("nynj_backpages"):
                self.get_nynj_backpages()
        self.num_pages = num_pages
        self.synchronous = synced

    def get_all_backpages(self):
        r = requests.get("http://www.backpage.com/")
        html = lxml.html.fromstring(r.text)
        backpages = html.xpath('//div[@class="united-states geoBlock"]//a/@href')
        links = []
        for i in backpages:
            if "backpage" in i:
                if not "www" in i: 
                    i = str(i)
                    links.append(i)

        with open("backpages","w") as f:
            pickle.dump(links,f)

    def get_nynj_backpages(self):
        ny_nj_backpage = ["newyork","bronx","brooklyn","longisland","manhattan","queens","statenisland","newjersey","centraljersey","jerseyshore","northjersey","southjersey"]
        r = requests.get("http://www.backpage.com/")
        html = lxml.html.fromstring(r.text)
        backpages = html.xpath("//a/@href")
        links = []
        for i in backpages:
            if "backpage" in i:
                for area in ny_nj_backpage:
                    if area in i:
                        if not "www" in i: 
                            i = str(i)
                            links.append(i)

        with open("nynj_backpages","w") as f:
            pickle.dump(links,f)

    def save(self,r):
        if self.national:
            if not os.path.exists("recruitment"):
                os.mkdir("recruitment")
            os.chdir("recruitment")
        elif self.local:
            if not os.path.exists("ads"):
                os.mkdir("ads")
            os.chdir("ads")

        name = "".join(r.url.split("/")[-2:])
        with open(name+".html","w") as f:
            text = r.text.encode("ascii","ignore")
            f.write(text)
        os.chdir("../")
        return name+".html"

    def setup_all(self,index):
        backpages = pickle.load(open("backpages","rb"))
        female_escorts = []
        body_rubs = []
        strippers = []
        dominatrixes = []
        transsexual_escorts = []
        male_escorts = []
        websites = []
        adult_jobs = []
        for page in backpages:
            for i in xrange(1,index):
                if i == 1:
                    female = page + "FemaleEscorts/"
                    female_escorts.append(female)
                    bodyrub = page + "BodyRubs/"
                    body_rubs.append(bodyrub)
                    stripper = page + "Strippers/"
                    strippers.append(stripper)
                    dominatrix = page + "Domination/"
                    dominatrixes.append(dominatrix)
                    transsexual = page + "TranssexualEscorts/"
                    transsexual_escorts.append(transsexual)
                    male = page + "MaleEscorts/"
                    male_escorts.append(male)
                    website = page + "Datelines/"
                    websites.append(website)
                    adult = page + "AdultJobs/"
                    adult_jobs.append(adult)
                else:
                    female = page + "FemaleEscorts/?page="+str(i)
                    female_escorts.append(female)
                    bodyrub = page + "BodyRubs/?page="+str(i)
                    body_rubs.append(bodyrub)
                    stripper = page + "Strippers/?page="+str(i)
                    strippers.append(stripper)
                    dominatrix = page + "Domination/?page="+str(i)
                    dominatrixes.append(dominatrix)
                    transsexual = page + "TranssexualEscorts/?page="+str(i)
                    transsexual_escorts.append(transsexual)
                    male = page + "MaleEscorts/?page="+str(i)
                    male_escorts.append(male)
                    website = page + "Datelines/?page="+str(i)
                    websites.append(website)
                    adult = page + "AdultJobs/?page="+str(i)
                    adult_jobs.append(adult)

        all_pages = female_escorts + body_rubs + strippers + dominatrixes + transsexual_escorts + male_escorts + websites + adult_jobs
        return all_pages

    def setup_nynj(self,index):
        backpages = pickle.load(open("nynj_backpages","rb"))
        adult_jobs = []
        for page in backpages:
            for i in xrange(1,index):
                if i == 1:
                    adult = page + "AdultJobs/"
                    adult_jobs.append(adult)
                else:
                    adult = page + "AdultJobs/?page="+str(i)
                    adult_jobs.append(adult)

        return adult_jobs

    #gets all the ads on a given backpage, page
    def grab_ads(self,page,asynchronous=False):
        if not asynchronous:
            r = requests.get(page)
            html = lxml.html.fromstring(r.text)
            ads = html.xpath('//div[@class="cat"]/a/@href')
            final = []
            for ad in ads:
                ad = str(ad)
                final.append(ad)
            return final
        else:
            responses = page
            results = []
            for r in responses:
                html = lxml.html.fromstring(r.text)
                ads = html.xpath('//div[@class="cat"]/a/@href')
                final = []
                for ad in ads:
                    ad = str(ad)
                    final.append(ad)
                results += final
            return results

    def get_information_from_page(self,url_list,asynchronous=False):

        if asynchronous:
            results = []
            for urls in url_list:
                rs = (grequests.get(u,stream=False) for u in urls)
                responses = grequests.map(rs)
                for r in responses:
                    
                    name = self.save(r)
                    if self.national:
                    	if not os.path.exists("recruitment"):
                            os.mkdir("recruitment")
                        os.chdir("recruitment")
                    elif self.local:
                    	if not os.path.exists("ads"):
                            os.mkdir("ads")
                        os.chdir("ads")
                    hash_value = hashlib.sha224(name)
                    os.chdir("../")
                    result = {}
                    html = lxml.html.fromstring(r.text)
                    posting_body = html.xpath('//div[@class="postingBody"]')
                    result["textbody"] = " ".join([i.text_content() for i in posting_body]).encode("ascii","ignore")
                    result['pictures'] = html.xpath('//ul[@id="viewAdPhotoLayout"]/li/a/@href')
                    result['url'] = r.url
                    result["phone_number"] = self.phone_number_grab(result["textbody"])
                    result["emails"] = self.email_grab(result["textbody"])
                    result["file_hash"] = hash_value
                    result["filename"] = name
                    results.append(result)
                    r.close()
            return results

        else:
            result = {}
            r = requests.get(url_list)
            self.save(r)
            if self.national:
                if not os.path.exists("recruitment"):
                    os.mkdir("recruitment")
                os.chdir("recruitment")
            elif self.local:
                if not os.path.exists("ads"):
                    os.mkdir("ads")
                os.chdir("ads")
            hash_value = hashlib.sha224(name)
            os.chdir("../")
            html = lxml.html.fromstring(r.text)
            posting_body = html.xpath('//div[@class="postingBody"]')
            result["textbody"] = [i.text_content() for i in posting_body]
            result["pictures"] = html.xpath('//ul[@id="viewAdPhotoLayout"]/li/a/@href')
            result["url"] = r.url
            result["phone_number"] = self.phone_number_grab(result["textbody"])
            result["emails"] = self.email_grab(result["textbody"])
            result["file_hash"] = hash_value
            result["filename"] = name
            return result

    def letter_to_number(self,text):
        text= text.upper()
        text = text.replace("ONE","1")
        text = text.replace("TWO","2")
        text = text.replace("THREE","3")
        text = text.replace("FOUR","4")
        text = text.replace("FIVE","5")
        text = text.replace("SIX","6")
        text = text.replace("SEVEN","7")
        text = text.replace("EIGHT","8")
        text = text.replace("NINE","9")
        text = text.replace("ZERO","0")
        return text
        
    def phone_number_grab(self,text):
        text = self.letter_to_number(text)
        phone = []
        counter = 0
        found = False
        for ind,letter in enumerate(text):
            if letter.isdigit():
                phone.append(letter)
                found = True
            else:
                counter += 1
            if counter > 5 and found:
                phone = []

        if len(phone) == 9 or len(phone) == 10:
            return ''.join(phone)
        else:
            return ''
        
    def email_grab(self,text):
        text = text.split(" ")
        emails = []
        for word in text:
            if "@" in word and "." in word:
                emails.append(word)
        return emails

    def run(self):
        print "setting up..."
        if self.national:
            pages = self.setup_all(self.num_pages) #tune this
        if self.local:
            pages = self.setup_nynj(self.num_pages) #tune this
        links = []
        now = time.strftime("%m_%d_%y_%H")
        folder = "backpage"+now
        if not os.path.exists(folder):
            os.mkdir(folder)
        os.chdir(folder)

        print "grabbing pages..."
        if self.synchronous:
            for page in pages:
                links += self.grab_ads(page)
        else:
            print len(pages)
            for i in xrange(0,len(pages),10):
                rs = (grequests.get(page,stream=False) for page in pages[i-10:i])
                responses = grequests.map(rs)
                links += self.grab_ads(responses,asynchronous=True)
        
        print "grabbing individual pages..."
        if not self.synchronous:
            #chunking requests because grequests can't handle that many at once
            url_list = []
            for i in xrange(0,len(links),10):
                url_list.append(links[i-10:i])

            data = self.get_information_from_page(url_list,asynchronous=True)
        else:
            data = []
            for link in links:
                data.append(get_information_from_page(link))
        final_data = pd.DataFrame(columns=["url","textbody","phone_number","pictures","emails","filename","file_hash"])
        
        for datum in data:
            final_data = final_data.append(datum,ignore_index=True)
        
        print "writing out to csv.."
        if self.national:
            final_data.to_csv("national_data.csv")
        if self.local:
            final_data.to_csv("ny_nj_data.csv")
        os.chdir("../")
        return folder
