import requests
import numpy as np
from bs4 import BeautifulSoup
import urllib.request
import math 
import cv2
import pytesseract
import re
from time import time
from decimal import ROUND_UP
from math import ceil
import pandas as pd
import sys, os

application_path = os.path.dirname(sys.executable)

URL = input('URL: ')
userMaxPrice = input('Enter Maximum Price: ')
priceIterator = input('Price Iterator: ')
minBedNo = input('Minimum number of bedrooms: ')

# splits the URL to the relevant area only and ignores all the features selected on the website
URL = URL.split('&')[0]
generatedURL = URL + '&minBedrooms=' + minBedNo
print('New URL generated!')

# rightmove main URL
### initialise search ### 

allLinksCombined = np.array([])
cleanLinks = np.array([])
minPrice = 50000
maxPrice = minPrice + int(priceIterator)

pageIterator = (int(userMaxPrice)-minPrice)/int(priceIterator)
for x in range(int(pageIterator)):
    URL = generatedURL + '&maxPrice=' + str(maxPrice) + '&minPrice=' + str(minPrice)
    page = requests.get(URL)

    # parse search results card
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id='l-container')

    # index for iterator (remember each page has 24 ads)
    noOfResults = soup.find('div', attrs={'id': 'searchHeader'})
    noOfResults = noOfResults.select('span')[0].text
    noOfResults = re.sub(r',', '', noOfResults)
    noOfResults = ceil(int(noOfResults)/24) # round up to nearest page (note max page no is 42)

    print(noOfResults, " Pages available for min price = ", minPrice, " max price = ", maxPrice)

    i = 0
    all_ids = np.array([])
    for x in range(noOfResults):
        URL = generatedURL + '&maxPrice=' + str(maxPrice) + '&minPrice=' + str(minPrice) + '&sortType=18&index='+ str(i)
        print('Page No.', x)
        page = requests.get(URL)

        # parse search results card
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id='l-container')

        # Extract and store ids
        links = results.select('a')
        for card in links:
            ids = card.get('id')
            ids = ids.strip() if ids is not None else ''
            all_ids = np.append(all_ids, ids)

        # clean array and add links
        all_ids = all_ids[all_ids != '']
        cleanIds = np.char.strip(all_ids, 'prop')
        allLinks = np.char.add(cleanIds, '#/?channel=RES_BUY')
        allLinks = np.char.add('https://www.rightmove.co.uk/properties/', allLinks)
    
        i = i + 24

    allLinksCombined = np.append(allLinksCombined, allLinks)
    minPrice = minPrice + int(priceIterator) 
    maxPrice = maxPrice + int(priceIterator) 

# removes empty and repeated links 
cleanLinks = np.char.replace(allLinksCombined, 'https://www.rightmove.co.uk/properties/0#/?channel=RES_BUY', '')
cleanLinks = cleanLinks[cleanLinks != '']
cleanLinks = np.unique(cleanLinks)

print('Number of links acquired: ', len(cleanLinks))
print(cleanLinks)

i = 0
counter = 0
all_info = np.array([])
data = np.array([])

for property in cleanLinks:
    start = time()
    ad = requests.get(property)
    soup = BeautifulSoup(ad.content, "html.parser")

    # ensures only freehold properties
    if soup.select('p')[4].text.lower() == 'freehold' or soup.select('p')[6].text.lower() == 'freehold':

        # extract property data
        propertyAddress = soup.select('h1')[0].text
        propertyType = soup.select('p')[0].text
        typeOfProperty = soup.select('p')[1].text
        noOfBeds = soup.select('p')[2].text
        priceLink = soup.body.find('div', attrs={'class': '_1gfnqJ3Vtd1z40MlC0MzXu'})
        price = priceLink.select('span')[0].text
        newIds = re.findall(r'\b\d+\b', str(cleanLinks[i])) # use new property id
        mapLocation = np.char.add('https://www.rightmove.co.uk/properties/', str(newIds[0]))
        floorPlan = np.char.add(mapLocation, '#/floorplan?activePlan=1&channel=RES_BUY')
        mapLocation = np.char.add(mapLocation, '#/map?channel=RES_BUY')
        
        # filter through the images to find the floor plan link
        floorPlanImage = requests.get(floorPlan)
        floorPlanImage = BeautifulSoup(floorPlanImage.content, "html.parser")
        floorPlanImage = floorPlanImage.find('div', attrs={'id': 'root'})
        for j in range(len(floorPlanImage.select('img'))):
            nextFloorPlanImage = floorPlanImage.select('img')[j].get_attribute_list('src',str)
            nextFloorPlanImage = ' '.join(nextFloorPlanImage)
            if '_max_296x197' in nextFloorPlanImage:
                foundFloorPlanImage = nextFloorPlanImage.replace('_max_296x197', '')
                break
            else:
                foundFloorPlanImage = 'None'
                pass
        
        i = i+1
        end = time()
        print(str(i)+' out of '+str(len(cleanLinks))+f' It took {round(end - start,2)} seconds!') 

        data = [str(price), str(propertyAddress), str(typeOfProperty), str(noOfBeds), str(foundFloorPlanImage), str(mapLocation)]
        all_info = np.append(all_info, data)
        counter = counter + 1
    else:
        #print('skipped...')
        i = i+1
        end = time()
        print(str(i)+' out of '+str(len(cleanLinks))+f' It took {round(end - start,2)} seconds!') 
        continue

# split the array into equally divided arrays
all_info = np.split(all_info, counter)
print(all_info)

import importlib 
from numpy import empty
import searchFunction
importlib.reload(searchFunction) # forces the definition to reload in case you make changes to it
from searchFunction import search 

updated_info = np.array([])

for info in range(len(all_info)):
    print(str(info+1)+' out of '+str(len(all_info)))
    
    if not all_info[info][4] == 'None':
        # Load the img
        req = urllib.request.urlopen(all_info[info][4])
        arr = np.asarray(bytearray(req.read()))
        img = cv2.imdecode(arr, -1) # 'Load it as it is'

        # Display loaded image
        # cv2.imshow('Floor Plan', img)
        # if cv2.waitKey() & 0xff == 27: quit()

        # OCR
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        configs = r'--psm 6'
        try:
            rawText = pytesseract.image_to_string(img, config=configs)
        except:
            continue
        rawText = rawText.lower()
        rawText = re.sub(r',', '', str(rawText)) # removes all commas 
        rawText = re.sub(r'\b\.\d+\b', '', str(rawText)) # removes all ints
        #print(rawText)

        newText = search(rawText)
        #print(newText)
        newInfo = list(np.append(all_info[info], newText)) # adding list adds the ',' back into the string array    
        updated_info = np.append(updated_info, newInfo)

# split the array into equally divided arrays and convert to pandas for further processing
updated_info = np.split(updated_info, len(updated_info)/7) 
updated_info = pd.DataFrame(updated_info, columns = ['price', 'propertyAddress', 'typeOfProperty', 'noOfBeds', 'foundFloorPlanImage', 'mapLocation', 'area'])
print(updated_info)

# this should load the old file and append any new data found to it making sure it's all unique data
# and not repeated 
loadData = pd.read_csv(r'output.csv')
frames = [loadData, updated_info]
combinedData = pd.concat(frames)
combinedData = combinedData.drop_duplicates(subset=['foundFloorPlanImage'])

updated_info.to_csv('output.csv', index=False)

combinedData['price'] = combinedData['price'].replace('[\£,]', '', regex=True).astype(float)
combinedData['area'] = combinedData['area'].astype(float)
combinedData['priceRank'] = combinedData['price'].rank(ascending=1)
combinedData['areaRank'] = combinedData['area'].rank(ascending=0)
combinedData['Rank Sum'] = combinedData.priceRank + combinedData.areaRank
combinedData = combinedData.sort_values(by = 'Rank Sum', ascending = True)

combinedData.to_csv('output_processed.csv', index=False)
print(combinedData)