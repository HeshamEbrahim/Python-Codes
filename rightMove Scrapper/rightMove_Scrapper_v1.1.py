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

#application_path = os.path.dirname(sys.executable)

URL = input('URL: ')
userMaxPrice = input('Enter Maximum Price: ')
priceIterator = input('Price Iterator: ')
minBedNo = input('Minimum number of bedrooms: ')

print("\n")
#userMaxPrice = '800000'
#priceIterator = '50000'
#minBedNo = '2'

# splits the URL to the relevant area only and ignores all the features selected on the website
beforeURL = URL.split('%')[0] + '%'
afterURL = URL.split('%')[1]
URL = afterURL.split('&')[0]
generatedURL = beforeURL + URL + '&minBedrooms=' + minBedNo
print(generatedURL)
print("\n")

# rightmove main URL
### initialise search ### 

allLinks = np.array([])
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
        print('Scrapped Page No.', x+1)
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

print("\n")
print('Number of links acquired: ', len(cleanLinks))
print("\n")
# print(cleanLinks)

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
        adDateLink = soup.body.find('div', attrs={'class': '_2nk2x6QhNB1UrxdI5KpvaF'})
        date = re.sub('<div class="_2nk2x6QhNB1UrxdI5KpvaF">', '', str(adDateLink))
        date = re.sub('</div>', '', str(date))
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

        data = [str(price), str(propertyAddress), str(typeOfProperty), str(noOfBeds), str(foundFloorPlanImage), str(mapLocation), str(date)]
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
#print(all_info)
print("\n")
print("Filtering freehold properties complete...")
print("\n")

def search(inputText):
    searchOne = [str(searchOne) for searchOne in re.findall(r'\b\d+\s*sq?\b', inputText)]
    if searchOne == []:
        searchOne = 0
    else:
        searchOne = re.findall(r'\b\d+\b', str(searchOne))
        searchOne = [int(i) for i in searchOne]
        searchOne = [int(searchOne) for searchOne in searchOne if searchOne <= 2000]

        if searchOne == []:
            searchOne = 0
        else:
            try:
                searchOne = max([int(searchOne) for searchOne in searchOne])
                if searchOne < 185:
                    searchOne = searchOne*10.7
                else:
                    pass
            except:
                searchOne = 0

    searchTwo = [str(searchTwo) for searchTwo in re.findall(r'\b\d+\s*ft2?\b', inputText)]
    if searchTwo == []:
        searchTwo = 0
    else:
        searchTwo = re.findall(r'\b\d+\b', str(searchTwo))
        try:
            searchTwo = max([int(searchTwo) for searchTwo in searchTwo])
        except:
            searchTwo = 0

    searchThree = [str(searchThree) for searchThree in re.findall(r'\b\d+\s*sq. ft.?\b', inputText)]
    if searchThree == []:
        searchThree = 0
    else:
        searchThree = re.findall(r'\b\d+\b', str(searchThree))
        try:
            searchThree = max([int(searchThree) for searchThree in searchThree])
        except:
            searchThree = 0

    searchFour = [str(searchFour) for searchFour in re.findall(r'\b\d+\s*saft?\b', inputText)]
    if searchFour == []:
        searchFour = 0
    else:
        searchFour = re.findall(r'\b\d+\b', str(searchFour))
        searchFour = [int(i) for i in searchFour]
        searchFour = [int(searchFour) for searchFour in searchFour if searchFour <= 2500]
        if searchFour == []:
            searchFour = 0
        else:
            try:
                searchFour = max([int(searchFour) for searchFour in searchFour])
            except: 
                searchFour = 0

    searchFive = [str(searchFive) for searchFive in re.findall(r'\b\d+\s*sqft?\b', inputText)]
    if searchFive == []:
        searchFive = 0
    else:
        searchFive = re.findall(r'\b\d+\b', str(searchFive))
        try:
            searchFive = max([int(searchFive) for searchFive in searchFive])
        except:
            searchFive = 0

    try:
        searchOutput = max(searchOne, searchTwo, searchThree, searchFour, searchFive)
    except:
        searchOutput = 'N/A'

    #print(searchOne, searchTwo, searchThree, searchFour, searchFive)

    return(searchOutput)

import importlib 
from numpy import empty
import searchFunction
importlib.reload(searchFunction) # forces the definition to reload in case you make changes to it
from searchFunction import search 

updated_info = np.array([])

for info in range(len(all_info)):
    print(str(info+1)+' out of '+str(len(all_info)))
    try:
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
    except:
        continue        

# split the array into equally divided arrays and convert to pandas for further processing
updated_info = np.split(updated_info, len(updated_info)/8) 
updated_info = pd.DataFrame(updated_info, columns = ['price', 'propertyAddress', 'typeOfProperty', 'noOfBeds', 'foundFloorPlanImage', 'mapLocation', 'date', 'area'])
updated_info = updated_info.drop(columns='foundFloorPlanImage')
print("\n")
# print(updated_info)
print('Processing images complete...')
print("\n")
# this should load the old file and append any new data found to it making sure it's all unique data
# and not repeated 

datahandling = input('Would you like to combine the data? (yes/no): ')
print("\n")

if datahandling == 'yes':
    print("\n")
    pathOfOldFile = input('Enter path of the file.csv you would like to combine the data to: ')
    loadData = pd.read_csv(pathOfOldFile)
    frames = [loadData, updated_info]
    combinedData = pd.concat(frames)
    combinedData = combinedData.drop_duplicates(subset=['mapLocation'])
else:
    updated_info.to_csv('output_basic.csv', index=False) 
    combinedData = updated_info.drop_duplicates(subset=['mapLocation'])

print("\n")

combinedData['price'] = combinedData['price'].replace('[\£,]', '', regex=True).astype(float)
combinedData['area'] = combinedData['area'].astype(float)
combinedData['priceRank'] = combinedData['price'].rank(ascending=1)
combinedData['areaRank'] = combinedData['area'].rank(ascending=0)
combinedData['Rank Sum'] = combinedData.priceRank + combinedData.areaRank
combinedData = combinedData.sort_values(by = 'Rank Sum', ascending = True)

combinedData.to_csv('output_processed.csv', index=False)
print(combinedData)

print("\n")
endCode = input('Press enter to end code...')