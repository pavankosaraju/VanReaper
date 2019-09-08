import requests
import re
import csv
from bs4 import BeautifulSoup
import random
import time
import numpy as np
import urllib.parse

pages = 1  # number of pages to scrape
distance = 3  # search radius in km within an area
items = 120

base_url = 'https://www.rew.ca/sitemap/real-estate'
rew_url = 'https://www.rew.ca'

# USER AGENTS

# Checkout https://developers.whatismybrowser.com/useragents/explore/

useragents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'Mozilla/5.0 (Linux; U; Android 4.1.2; de-de; GT-I8190 Build/JZO54K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
    'Mozilla/5.0 (Linux; U; Android 4.1.2; de-de; ME371MG Build/JZO54K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30',
    'Mozilla/5.0 (Linux; U; Android 4.2.2; pl-pl; GT-P5110 Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30',
    'Mozilla/5.0 (Linux; U; Android 4.1.1; de-de; SGPT12 Build/TJDSU0177) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30',
    'Opera/9.80 (J2ME/MIDP; Opera Mini/7.1.32052/29.3417; U; en) Presto/2.8.119 Version/11.10',
    'Opera/9.80 (J2ME/MIDP; Opera Mini/7.1.32052/29.3594; U; en) Presto/2.8.119 Version/11.10',
    'Opera/9.80 (J2ME/MIDP; Opera Mini/4.2.23449/28.2144; U; en) Presto/2.8.119 Version/11.10',
    'Opera/9.80 (J2ME/MIDP; Opera Mini/4.2.20464/28.3950; U; en) Presto/2.8.119 Version/11.10',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
    'Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0	',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15'
]


def get_proxies():
    proxies = []
    url = 'https://free-proxy-list.net/'
    r = requests.get(url)
    s = BeautifulSoup(r.content, 'html.parser')
    dt = s.find_all("tr")
    for i in range(80):
        if dt[i + 1].find_all("td")[4].text == "elite proxy":
            px = dt[i + 1].find_all("td")[0].text + ":" + dt[i + 1].find_all("td")[1].text
            proxies.append(px)
    return proxies


def get_postal_codes():
    area = []
    aname = []
    l = "https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_V"
    r = requests.get(l)
    s = BeautifulSoup(r.content, 'html.parser')
    dt = s.find_all("td", limit=180)
    for a in dt:
        area.append(a.find("b").text)
        names = a.find_all("a")
        n = ""
        for na in names:
            n = n + na.text + ", "
        n = n.strip(" ,")
        aname.append(n)
    return area, aname


proxies = get_proxies()

raw_site_response = requests.get(base_url)

soup = BeautifulSoup(raw_site_response.content, 'html.parser')

#great_van_areas = soup.select('a[class = "gridblock-link"]')

great_van_areas = soup.findAll('a', 'gridblock-link')

great_van_areas = great_van_areas[0:14]                          # take only greater 	vancouver


'''
1. The outer for loop is for areas. eg: burnaby, chinatown etc.
2. The next for loop is for iterating subareas
3. The next while loop for iterating pages
3. The fourth while loop is till you get http response. fucking proxies. dont touch this loop
4. The fifth for loop is for getting access to details page and saving the details page as a file
'''
for x in range(len(great_van_areas)):
    area_relative_url = great_van_areas[x].attrs['href']
    area_name = area_relative_url.split('/')[-1]

    area_temp = 'sitemap' + '/real-estate/' + area_name
    area_url = urllib.parse.urljoin(rew_url, area_temp)

    print(area_url)
    rest = requests.get(area_url)
    sep = BeautifulSoup(rest.content, 'html.parser')
    elements = sep.select('a[class = "gridblock-link"]')

    href = [element.attrs['href'] for element in elements]

    st = np.random.randint(2, 10, size=len(href))
    updateproxy = np.random.randint(0, 2, size=len(href))

    for y in range(len(href)):
        subareas_url = urllib.parse.urljoin(rew_url, href[y])
        print("subareas: " + subareas_url)

        if updateproxy[y]:
            proxies = get_proxies()

        print(proxies)
        user_agent = random.choice(useragents)
        headers = {'User-Agent': user_agent}
        proxy = random.choice(proxies)

        time.sleep(st[y])
        property_file_number = 0
        i = 0

        while True:     # iterate pages
            i = i + 1
            print("Scraping properties in " + href[y].split('/')[-1] + " regions. Page >> " + str(i))

            while True:  # get new proxy for each page. dont change this.it works
                try:
                    r = requests.get(subareas_url, headers=headers, proxies={"http": proxy, "https": proxy},timeout=60)
                    if r.status_code < 400:
                        print("-> Scrape successful.")
                        break
                except Exception as e:
                    print("-> Scrape unsuccessful. Retrying...")
                    time.sleep(random.randint(0, 7))
                    print("woke up from sleep")
                    proxy = random.choice(proxies)

            s = BeautifulSoup(r.content, 'html.parser')
            details = s.select('a[title]')

            hrs = [detail.attrs['href'] for detail in details]
            hrs = hrs[1:]
            hrs = hrs[::2]

            ##### loops for downloading properties on the page #####
            for hr in hrs:
                property_url = urllib.parse.urljoin(rew_url, hr)
                while True:  # get new proxy for each page. dont change this.it works
                    try:
                        res = requests.get(property_url, headers=headers, proxies={"http": proxy, "https": proxy},timeout = 60)
                        if res.status_code < 400:
                            print("-> Scrape successful.")
                            break
                    except Exception as e:
                        print("-> Scrape unsuccessful. Retrying...")
                        time.sleep(random.randint(0, 7))
                        print("woke up from sleep. properties")
                        proxy = random.choice(proxies)

                file_name = 'listing_' + href[y].split('/')[-1] + "_" + str(property_file_number) + ".html"
                print("saving file for : " + file_name)
                html_file = open(file_name, 'wb')
                for slabs in res.iter_content(1000000):  # write to file in chunks so that even if downloaded content is huge, it does not clog up the ram
                    html_file.write(slabs)
                html_file.close()
                property_file_number += 1
            ## download listings and saving finished for that page

            t = s.select('li > a[total_pages]')

            if len(t) == 0:
                break

            if t is not None or t != []:  # when not to break. update the link
                subareas_url = urllib.parse.urljoin(rew_url, href[y])
                subareas_url = subareas_url + '/page/' + str(i+1)
                print(subareas_url)
                continue
