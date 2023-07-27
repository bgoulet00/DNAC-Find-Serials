# locating a single serial in the DNAC GUI is a simple tasks but if there are a half dozen or more it can be manually tedious
# this scrip takes an input file serials.csv with a single column A containing serials numbers to search for
# it will search the DNA center inventory for those serials numbers and output the finding to file serials-found.csv
# serials-found.csv will have the serials listed in column A and the device where found in column B
# in addition to the output file, the findings will be printed interactively to the screen
#
# execute the program by issueing the command 'pyhton3 dnac-find-serials.py' without quotes from the linux command line

#deleloped with Python 3.6 

import requests
from requests.auth import HTTPBasicAuth
import json
import csv
import os
import sys

# Disable SSL warnings
import urllib3
urllib3.disable_warnings()

# Variables
BASE_URL = 'https://10.216.3.110'
AUTH_URL = '/dna/system/api/v1/auth/token'
INVENTORY_URL = '/dna/intent/api/v1/network-device'
inFile = 'serials.csv'
outFile = 'serials-found.csv'
# list to store data from input file
dataInput = []
# list of dictionaries.  each dictionary contains key-value pairs for serial and devicename
dataOutput = []
dataOutput_columns = ["Serial", "DeviceName"]

# Get Authentication Token and return the token value as a string
# exit with an error message if a valid response is not received
def get_token():
    print('\n\nEnter DNA Center Credentials')
    user = input("USERNAME: ").strip()
    passwd = input("PASSWORD: ").strip()
    response = requests.post(
       BASE_URL + AUTH_URL,
       auth=HTTPBasicAuth(username=user, password=passwd),
       headers={'content-type': 'application/json'},
       verify=False,
    )
    data = response.json()
    if response:
        return data['Token']
    else:
        sys.exit('Unable to connect to ' + BASE_URL + ' using supplied credentials')

# Get Device Inventory.  The returned data will be a list of dictionaries
# each device is a dictionary in the list. json() is used to convert it to json format
def get_inventory(token):
    response = requests.get(
       BASE_URL + INVENTORY_URL,
       headers = {'X-Auth-Token': token, 'Content-Type': 'application/json'},
       verify=False,
    )
    return response.json()


def main():

    Token = get_token()
    Inventory = get_inventory(Token)

    # open the input file, read each row and add the contents of row index 0 (column A) to the dataInput list
    with open(inFile, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            dataInput.append(row[0])

    # for each item in the dataInput list, search for it's presence in the device inventory	
    # update the hostname value based on if the item was found on a host or not
    # append the dataOutput list with a new dictionary item containint serial and hostname
    # print the search finding to the screen
    for  item in dataInput:
        found = False
        for device in Inventory['response']:
            if item in device['serialNumber']:
                found = True
                hostname = device['hostname']
        if found == False:
            hostname = "NONE"
        dataOutput.append({"Serial": item,"DeviceName": hostname})
        print('serial ' + item + " found on device " + hostname)

    # for each dictionary item in dataOutput list, write the dictionary element values to a row in the output csv file
    # any existing version of the output file should be removed first
    if os.path.isfile(outFile):
        os.remove(outFile)
    with open(outFile, "w") as file:
        writer = csv.DictWriter(file, fieldnames=dataOutput_columns)
        for item in dataOutput:
            writer.writerow(item)

if __name__ == "__main__":
    main()
