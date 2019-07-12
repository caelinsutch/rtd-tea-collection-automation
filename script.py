import pandas as pd
import requests
import xml.etree.ElementTree as ET
from xmljson import badgerfish as bf
import json
import xlsxwriter


data = pd.read_excel (r'rtd.xlsx', sheet_name='Sheet1')

dataFrame = pd.DataFrame(data, columns=['Product'])

dataInList = dataFrame.values.tolist()
finalDataArray = []

sampleData = ''
plus = "+"
writer = pd.ExcelWriter('result-data.xlsx', engine='xlsxwriter')


# TODO create a better way to do this that preserves dataframe type
for count, element in enumerate(dataInList, 1):
    # Iterate through list created from xcel sheet
    if count % 10 == 0:
        productName = ''
        # globals for nutrition count
        calories = ''
        protein = ''
        fat = ''
        carbs = ''
        sugar = ''

        # Make new xcel file
        xmlFile = open("res{}.xml".format(count), "w+")
        # Get first 4 words from spreadsheet and put to sample data
        sampleData = element[0].split()[:4]
        productName = element[0]
        # Join sample data into string with + for spaces
        sampleData = plus.join(sampleData)
        # API call and get content returned
        xml = (requests.get("https://api.nal.usda.gov/ndb/search/?format=xml&q={}&api_key=c7bdD3Mz5KQjggqv5B8hNpeov3fsBnlBB7Gb3wPU".format(sampleData)).content)
        # Decode data
        decodedXML = xml.decode('utf-8')
        # Writes to a new file
        xmlFile.write(decodedXML)
        # Adds space
        xmlFile.write("\n \n")
        # Save data
        xmlFile.close()

        # Gets XML from file
        try:
            parsedXML = ET.parse('./res{}.xml'.format(count))
            root = parsedXML.getroot()
            # Root is a xml.etree.ElementTree.element type

            listOfDbNumbers = []
            # If there are no errors (http return response bad)
            if root.tag != 'errors':
                # Put database numbers in array (for future reference)
                for dbno in root.iter('ndbno'):
                    listOfDbNumbers.append(dbno.text)

                # Request data for individual product
                if listOfDbNumbers:
                    resjson = requests.get("https://api.nal.usda.gov/ndb/V2/reports?ndbno={}&format=json&api_key=c7bdD3Mz5KQjggqv5B8hNpeov3fsBnlBB7Gb3wPU".format(int(listOfDbNumbers[0])))
                    # Turn into dictionary
                    object = json.loads(resjson.content)
                    # Get nutrients
                    nutrients = object.get("foods", {})[0].get('food', {}).get('nutrients', {})

                    for i in range(len(nutrients)):
                        # List of Possible Names:
                        # - Energy
                        # - Protein
                        # - Total lipid (fat)
                        # - Carbohydrate, by difference
                        # - Sugars, total
                        # - Sodium, Na
                        # - Vitamin C, total ascorbic acid
                        # - Iron, Fe
                        # - Calcium, Ca
                        # - Fatty acids, total saturated
                        # - Fatty acids, total trans
                        # - Cholesterol
                        if nutrients[i].get('name') == 'Energy':
                            calories = nutrients[i].get('value')
                        elif nutrients[i].get('name') == 'Sugars, total':
                            sugar = nutrients[i].get('value')
                        elif nutrients[i].get('name') == 'Protein':
                            protein = nutrients[i].get('value')
                        elif nutrients[i].get('name') == 'Total lipid (fat)':
                            fat = nutrients[i].get('value')
                        elif nutrients[i].get('name') == 'Carbohydrate, by difference':
                            carbs = nutrients[3].get('value')

                    # Assign
                    servingSize = str(nutrients[0].get('measures')[0].get('eqv')) + nutrients[0].get('measures')[0].get('eunit')
                    dataToWrite = {'Product Name': productName, 'Serving Size': servingSize, 'Calories': calories, 'Protein': protein, 'Fat': fat, 'Carbs': carbs, 'Sugar': sugar}
                    finalDataArray.append(dataToWrite)
        except:
            print('Malformed XML')

dataFrameFinal = pd.DataFrame(finalDataArray)
dataFrameFinal.to_excel(writer, sheet_name='Sheet1')
writer.save()







# sampleData.replace("")
