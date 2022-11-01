import re
import numpy

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
            searchOne = max([int(searchOne) for searchOne in searchOne])
            if searchOne < 185:
                searchOne = searchOne*10.7
            else:
                pass

    searchTwo = [str(searchTwo) for searchTwo in re.findall(r'\b\d+\s*ft2?\b', inputText)]
    if searchTwo == []:
        searchTwo = 0
    else:
        searchTwo = re.findall(r'\b\d+\b', str(searchTwo))
        searchTwo = max([int(searchTwo) for searchTwo in searchTwo])

    searchThree = [str(searchThree) for searchThree in re.findall(r'\b\d+\s*sq. ft.?\b', inputText)]
    if searchThree == []:
        searchThree = 0
    else:
        searchThree = re.findall(r'\b\d+\b', str(searchThree))
        searchThree = max([int(searchThree) for searchThree in searchThree])

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
            searchFour = max([int(searchFour) for searchFour in searchFour])

    searchFive = [str(searchFive) for searchFive in re.findall(r'\b\d+\s*sqft?\b', inputText)]
    if searchFive == []:
        searchFive = 0
    else:
        searchFive = re.findall(r'\b\d+\b', str(searchFive))
        searchFive = max([int(searchFive) for searchFive in searchFive])
    
    try:
        searchOutput = max(searchOne, searchTwo, searchThree, searchFour, searchFive)
    except:
        searchOutput = 'N/A'

    #print(searchOne, searchTwo, searchThree, searchFour, searchFive)

    return(searchOutput)