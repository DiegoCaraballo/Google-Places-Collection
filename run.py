# Contact: diegocaraballo84@gmail.com
# www.pythondiario.com

import csv
import requests
import xml.etree.ElementTree as ET

def getRequest(keyword):

    api_key = "Enter API-KEY"
    
    url = "https://maps.googleapis.com/maps/api/place/textsearch/xml?query=" + keyword + "&radius=50000&key=" + api_key

    row = []

    try:
        # sending get request and saving the response as response object 
        response = requests.get(url) 
  
        root = ET.fromstring(response.content)

        for result in root.findall('./result'):

            row.append(keyword)
            row.append(result.find('name').text)
            row.append(result.find('type').text)
            row.append(result.find('formatted_address').text)
            row.append(result.find('geometry')[0][0].text)
            row.append(result.find('geometry')[0][1].text)
            row.append(result.find('rating').text)
            row.append(result.find('id').text)

            print(row)

            # Add row in output-file.csv
            addResultCsv(row, 'output-file.csv')

            row = []
                    
    except Exception as e:
        print(e)
        pass

def addResultCsv(row, output_file):
    try:
        
        with open(output_file, 'a', newline='') as writeFile:
            
            writer = csv.writer(writeFile)
            writer.writerow(row)

    except Exception as e:
        print(e)
    
    finally:
        writeFile.close()

def getKeywords(csv_file):
    try:

        list_keywords = []

        # Open File and Iterate in Keywords
        with open(csv_file) as csvfile:
            spamreader = csv.reader(csvfile)
            for row in spamreader:
                list_keywords.append(row[0].replace(" ", "+"))

            return list_keywords

    except Exception as e:
        print(e)
    
    finally:
        csvfile.close()

def main():
    try:
        
        print("Please Wait...")

        # List Keyword - input-file.csv
        keyword_list = getKeywords('input-file.csv')
        keyword_list.pop(0)

        head = ['Search Phrase', 'Name', 'Type', 'Address', 'Lat','Long' ,'Rating' ,'Place ID']
        
        # Add head in CSV
        addResultCsv(head, 'output-file.csv')

        # Iterate in keyword_list
        for keyword in keyword_list:
            getRequest(keyword)

        print("Finish... Press enter to exist")
        input("")

    except Exception as e:
        print(e)
        input("")


# Run Script
main()
