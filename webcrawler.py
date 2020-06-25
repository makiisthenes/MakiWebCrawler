import scrapy  # Check if works with Python 37.
import threading
import requests
from bs4 import BeautifulSoup
import pickle
import pyspider
import face_recognition
from storage_checker import storage_left
import time
from google_images_download import google_images_download


# Mass Google Image Downloader Example
# https://google-images-download.readthedocs.io/en/latest/installation.html#install-using-pip - Mass Google Image Downloading.
def google_mass_downloader(topic):
    response = google_images_download.googleimagesdownload()
    query_arguement = {"keywords":str(topic.strip()), "limit":20, "print_urls":True}
    absolute_image_paths = response.download(query_arguement)
    print(absolute_image_paths)
    

storage_left()
# Make sure we are not collecting /indexing data from sources where not of significance.
avoid_terms = ["fb-messenger", "whatsapp", "youtube.com", "ebay", "amazon", "twitter", "store", "privacy", "cookies", "contact", "terms", "help", "guidance", "contact"]
# We will look for image tags and also




# This scraper is not used currently, but will be later on.
class thirdpartybot(scrapy.Spider):  # Inherit Scrapy bot class into this class.
    # Read the documentation for this class.
    name = 'spidermanbot'
    start_urls = ['https://blog.scrapinghub.com']
    def parse(self, response):
        for title in response.css('.post-header>h2'):
            yield {'title': title.css('a ::text').get()}

        for next_page in response.css('a.next-posts-link'):
            yield response.follow(next_page, self.parse)


class CrawlerBot:
    def __init__(self, base_url):
        self.time_created = 0  # epoch time.
        self.base_url = base_url
        self.domain = self.domain_finder(self.base_url)
        self.base_soup_obj = None
        self.status_code = 000
        self.current_url = ''
        self.url_list  = []  # List of temporary url's found on a base list.
        self.internal_url_list = []
        self.external_url_list = []
        self.image_list = []  # These are permanent storage places for image url objects.
        self.video_list = []  # These are permanent storage places for video url objects.
        self.obj_list1 = []  # Temporary Storing of Object URL's.
        self.obj_list2 = []  # Temporary Storing of Object URL's [intermediate]
        self.exception = []  # Storage of known errors passed through this object.
    def get_source_code(self):
        try:
            r = requests.get(self.base_url)
            self.status_code = r.status_code
            # print(r.text)
            self.current_url = r.url
            print(self.current_url)
            if str(r.status_code)[0] == '2':  # Good Response 2XX
                self.time_created = time.time()
                html_doc = r.text
                soup = BeautifulSoup(html_doc, 'html.parser')
                self.base_soup_obj = soup
                # Finding Links for webpages.
                print("Redirect Links ---")
                for link in soup.find_all('a'):
                    if link.get("href") != '#':
                        if "#" not in link.get("href"):
                            # print(link.get("href"))
                            # print(self.url_list)
                            if link.get("href") not in self.url_list:
                                self.url_list.append(link.get("href"))
                                # print(link.get('href'))
                print("Images Links ---")
                for images in soup.find_all("img"):
                    print(images['src'])
                    if images['src'] not in self.image_list:
                        self.image_list.append(images["src"])
                print("Videos Link ---")
                for videos in soup.find_all("video"):
                    print(videos)
                    if videos['src'] not in self.video_list:
                        self.video_list.append(videos["src"])
                # Now that all the videos and images have been saved, we can now look into the URL's that we have found.
                length = len(self.url_list)
                # Find the length of how many urls we have and then decide how many threads we want to start running to perform these actions simultaneously.
                print(f"We have found {length} URL's on this website.")
                for link in self.url_list:
                    filtered_out = False
                    # print(link)
                    for indx in avoid_terms:
                        if indx in link:
                            filtered_out = True
                    if not filtered_out:
                        # This link is ok and will give us decent information for data extraction.
                        if "http" in link:
                            # External Links that go to different websites go here.
                            print(f"External --> {link}")
                            self.external_url_list.append(link)
                        elif "http" not in link:
                            # This links to the same page and will lead to more results on this page.
                            # Same website link here.
                            link = self.internal_url_creator(link)
                            print(f"Internal --> {link}")
                            self.internal_url_list.append(link)

            elif r.status_code == 403:
                self.exception.append("403 HTTP Client Error")
            elif r.status_code == 404:
                self.exception.append("404 Page not Found")
            else:
                self.exception.append(r.status_code)  # If all cases fail and tge first website gives this error.
        except Exception as e:
            print(f"There was an error {e}")
            
            self.exception.append(str(e))
    def find_url_length(self):
        length = len(self.url_list)
        return length
    def find_obj1_length(self):
        length = len(self.obj_list1)
        return length
    def find_obj2_length(self):
        length = len(self.obj_list2)
        return length
    def domain_finder(self, url):
        url_split = url.split("/")
        return url_split
    def internal_url_creator(self, link):
        # ['https:', '', 'www.bbc.com', 'news', 'uk-53031072']
        found_index = False
        hasCompleted = False
        url_builder = ""
        link_sep = self.domain_finder(link)
        for x in range(len(self.domain)):
            new_x = True
            for y in range(len(link_sep)):
                if not found_index:
                    if link_sep[y] != '':
                        if link_sep[y] == self.domain[x]:
                            found_index = True
                            if link_sep[y] != link_sep[-1]:
                                url_builder += link_sep[y] + '/'
                            # These are the index's where they join.
                        elif new_x:
                            url_builder += self.domain[x]+'/'
                            new_x = False
                elif found_index and not hasCompleted:
                    if link_sep[y] != '':
                        if link_sep[y] != link_sep[-1]:
                            url_builder += link_sep[y] + '/'
                        else:
                            url_builder += link_sep[y]
                            hasCompleted = True
        if not found_index:
            if link[0] == '/' or self.current_url[-1] == "/":
                url_builder = self.current_url + link
            else:
                url_builder = self.current_url + '/' + link
        return url_builder


# Starting Base URL. To spread from.
bot = CrawlerBot("https://www.bbc.com/news/uk-53031072")
bot.get_source_code()
print(bot.domain)



# Yield, lamba, @ not sure what these mean and also __magic__ functions.
# https://scrapy.org/
