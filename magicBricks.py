#!/usr/bin/env python

"""
Sample Script to Scrap a site using python lxml and request module.
"""

from lxml import html
import requests
import time


place = raw_input('Enter city: ').capitalize()
area = raw_input('Enter area (For Multiple area enter , seprated): ')
AREAS = area.split(',')
HEADERS = {'User-Agent':
           'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0'}

# with open('HTML/2.html', 'r') as page:

for area in AREAS:

    print "Searching result in " + area

    url_str = 'http://www.magicbricks.com/property-for-rent/residential-real-estate?' \
        'proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,' \
        'Studio-Apartment,Service-Apartment&Locality=%s&cityName=%s&BudgetMin=5,000&BudgetMax=10,000' % (area, place)

    user_page = requests.get(url_str, headers=HEADERS)
    tree = html.fromstring(user_page.text)

    product_urls = tree.xpath(
        '//div[contains(@class,"srpBlock") and contains(@class, "srpContentImageWrap")]/@onclick')

    for link in product_urls:
        link_url = link.split("'")
        print "Search Result: http://www.magicbricks.com" + link_url[1]
        time.sleep(10)

        page = requests.get(
            'http://www.magicbricks.com' + link_url[1], headers=HEADERS)

        html_string = html.fromstring(page.text)

        from_site = html_string.xpath('//meta[@property="og:title"]/@content')[0]
        description = html_string.xpath('//meta[@name="Description"]/@content')[0]
        price = html_string.xpath(
            '//*[@id="rightAgentH"]/div[2]/div[2]/div[3]/div[2]/ul/li[1]/div/span/text()')[0]
        property_id = html_string.xpath(
            '//span[@class="lastPart"]/text()')[0].split(':')[1]

        print 'from_site:', from_site
        print 'description:', description
        print 'price:', price
        print 'property_id:', property_id
        print '\n\n'
