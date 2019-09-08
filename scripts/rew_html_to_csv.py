import os
from bs4 import BeautifulSoup
import re
import pandas as pd
import csv

html_path = 'C:\\Users\\chira\PycharmProjects\\test\\bigdata2\\project\\parser'

csv_path = ''

def extract_elements(soup):
    dict = {}
    dict['price'] = extract_price(soup)
    dict['postal_code'] = extract_postalcode(soup)
    dict['street_address'] = extract_streetaddress(soup)
    dict['listing_id'] = extract_id(soup)
    dict['bed'] = extract_bed(soup)
    dict['bath'] = extract_bath(soup)
    dict['area_sqft'] = extract_sqft(soup)
    dict['type'] = extract_type(soup)
    dict['age'] = extract_age(soup)
    dict['taxes'] = extract_taxes(soup)
    dict['subarea'] = extract_sub_area(soup)
    dict['style'] = extract_style(soup)
    dict['features'] = extract_features(soup)
    dict['amenities'] = extract_amenities(soup)
    dict['fireplaces'] = extract_fireplaces(soup)

    return dict

def extract_features(soup):
    reg = re.compile(r'Features')
    features = ""
    try:
        # elements = soup.body.findAll(text='Listing ID')
        th_tag = [e for e in soup.find_all('th') if reg.match(e.text)]
        features_tag = th_tag[0].findNext('td')
        features = features_tag.getText()
        features = features.strip()
    except Exception as e:
        print(e)
        print("features not found. Moving on")

    return features

def extract_amenities(soup):
    reg = re.compile(r'Amenities')
    amenities = ""
    try:
        # elements = soup.body.findAll(text='Listing ID')
        th_tag = [e for e in soup.find_all('th') if reg.match(e.text)]
        amenities_tag = th_tag[0].findNext('td')
        amenities = amenities_tag.getText()
        amenities = amenities.strip()
    except Exception as e:
        print(e)
        print("amenities not found. Moving on")

    return amenities


def extract_fireplaces(soup):
    reg = re.compile(r'Fireplaces')
    fireplaces = ""
    try:
        # elements = soup.body.findAll(text='Listing ID')
        th_tag = [e for e in soup.find_all('th') if reg.match(e.text)]
        fireplaces_tag = th_tag[0].findNext('td')
        fireplaces = fireplaces_tag.getText()
        fireplaces = fireplaces.strip()
    except Exception as e:
        print(e)
        print("firepplaces not found. Moving on")

    return fireplaces

def extract_taxes(soup):
    reg = re.compile(r'Gross Taxes')
    taxes = ""
    try:
        # elements = soup.body.findAll(text='Listing ID')
        th_tag = [e for e in soup.find_all('th') if reg.match(e.text)]
        tax_tag = th_tag[0].findNext('td')
        tax_tag = tax_tag.getText()
    except Exception as e:
        print(e)
        print("tax not found. Moving on")

    return taxes

def extract_sub_area(soup):
    reg = re.compile(r'Sub-Area')
    sub_area = ""
    try:
        # elements = soup.body.findAll(text='Listing ID')
        th_tag = [e for e in soup.find_all('th') if reg.match(e.text)]
        sub_area_tag = th_tag[0].findNext('td')
        sub_area = sub_area_tag.getText()
        sub_area = sub_area.strip()
    except Exception as e:
        print(e)
        print("subarea not found. Moving on")

    return sub_area


def extract_style(soup):
    reg = re.compile(r'Style')
    style = ""
    try:
        # elements = soup.body.findAll(text='Listing ID')
        th_tag = [e for e in soup.find_all('th') if reg.match(e.text)]
        style_tag = th_tag[0].findNext('td')
        style = style_tag.getText()
        style = style.strip()
    except Exception as e:
        print(e)
        print("style not found. Moving on")

    return style

def extract_age(soup):
    reg = re.compile(r'Property Age')
    age = ""
    try:
        # elements = soup.body.findAll(text='Listing ID')
        th_tag = [e for e in soup.find_all('th') if reg.match(e.text)]
        age_tag = th_tag[0].findNext('td')
        age = age_tag.getText()
    except Exception as e:
        print(e)
        print("age not found. Moving on")

    return age

def extract_id(soup):
    reg = re.compile(r'Listing ID')
    id = ""
    try:
        #elements = soup.body.findAll(text='Listing ID')
        th_tag = [e for e in soup.find_all('th') if reg.match(e.text)]
        id_tag = th_tag[0].findNext('td')
        id = id_tag.getText()
    except Exception as e:
        print(e)
        print("id not found. Moving on")

    return id

def extract_bed(soup):
    bed = ""
    try:
        elements = soup.select('.summarybar-label')
        bed = elements[0].getText()
    except Exception as e:
        print("bed not found. Moving on")

    return bed

def extract_bath(soup):
    bath = ""
    try:
        elements = soup.select('.summarybar-label')
        bath = elements[1].getText()
    except Exception as e:
        print("bath not found. Moving on")

    return bath

def extract_sqft(soup):
    area = ""
    try:
        elements = soup.select('.summarybar-label')
        area = elements[2].getText()
        area = area.strip()
    except Exception as e:
        print("Area not found. Moving on")

    return area

def extract_type(soup):
    reg = re.compile(r'Property Type')
    type = ""
    try:
        # elements = soup.body.findAll(text='Listing ID')
        th_tag = [e for e in soup.find_all('th') if reg.match(e.text)]
        id_tag = th_tag[0].findNext('td')
        type = id_tag.getText()
    except Exception as e:
        print(e)
        print("type not found. Moving on")

    return type


def extract_price(soup):
    price = ""
    try:
        elements = soup.select('.propertyheader-price')
        price = elements[0].getText()
    except Exception as e:
        print("Price not found. Moving on")

    return price


def extract_postalcode(soup):
    postal_code = ""
    try:
        elements = soup.select('span[itemprop="postalCode"]')
        postal_code = elements[0].getText()
    except Exception as e:
        print(e)
        print("Postal code not found. Moving on")

    return postal_code

def extract_streetaddress(soup):
    streetaddress = ""
    try:
        elements = soup.select('span[itemprop="streetAddress"]')
        streetaddress = elements[0].getText()
    except Exception as e:
        print(e)
        print("Street address not found. Moving on")

    return streetaddress


with open('property_listing.csv', 'w') as csv_file:
    filewriter = csv.DictWriter(csv_file, delimiter = ',' ,fieldnames=['price', 'postal_code', 'street_address','listing_id', 'bed','bath','area_sqft','type','age','taxes','subarea','style','features','amenities','fireplaces'])
    filewriter.writeheader()
    for filename in os.listdir(html_path):
        if filename.endswith('.html'):
            with open(filename, 'r', encoding='utf-8') as htmlfile:
                content = htmlfile.read()
                soup = BeautifulSoup(content, "html.parser")
                dict_record = extract_elements(soup)
                filewriter.writerow(dict_record)


