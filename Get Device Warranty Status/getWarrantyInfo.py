import sys
import requests
import json
import logging
import csv
import time

# authentication code modified from https://docs.informatica.com/integration-cloud/cloud-api-manager/current-version/api-manager-guide/authentication-and-authorization/oauth-2-0-authentication-and-authorization/python-3-example--invoke-a-managed-api-with-oauth-2-0-authentica.html

# function to obtain a new OAuth 2.0 token from the authentication server
def get_new_token():

    auth_server_url = "authentication_link"
    client_id = 'client_id'
    client_secret = 'client_secret'

    token_req_payload = {'grant_type': 'client_credentials'}

    token_response = requests.post(auth_server_url, data=token_req_payload, verify=False, allow_redirects=False, auth=(client_id, client_secret))
                
    if token_response.status_code !=200:
        print("Failed to obtain token from the OAuth 2.0 server", file=sys.stderr)
        sys.exit(1)

    print("Successfuly obtained a new token")
    tokens = json.loads(token_response.text)
    return tokens['access_token']



logging.captureWarnings(True)
# setting variables
test_api_url = "api_url"

# get list of serials from file
fileData = list(csv.reader(open("DeviceSerials.csv")))
serialList = []
increment = 1


# put column headers in csv for data output
with open("WarrantyInfo.csv", mode="w", newline="") as csvFile:
    # put column headers in csv for data input
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(["Serial Code", "Warranty Expiration Date", "Coverage Level"])

    # put device serials in a list
    for data in fileData:
        serialList.append(data[0])
    
    # get length of list of serial numbers
    listLength = round(len(serialList) / 100, 2)
    if listLength < 1:
        listLength = 1
    

    # break list into groups of 100
    while listLength >= 1:
        tempList = serialList[0:99]

        # add serial codes to url for api request
        for code in tempList:
            if increment == 1:
                test_api_url += code
                increment += 1
            else:
                test_api_url += "," + code
            
            # remove serial code from list
            serialList.remove(code)
 


        # obtain a token before calling the API for the first time
        token = get_new_token()

        # call the API with the token
        api_call_headers = {'Authorization': 'Bearer ' + token}
        api_call_response = requests.get(test_api_url, headers=api_call_headers, verify=False)

        # call API with token
        if	api_call_response.status_code == 401:
            token = get_new_token()
        else:
            # get data from API response
            userData = json.loads(api_call_response.text)
        
        # get serial number, warranty expiration date, and level of coverage for each device and write it to file
        for item in userData:
            serial = item["serviceTag"]
            
            try:
                entitlements = item["entitlements"][1]
            except IndexError:
                entitlements = "Expired"

            try:
                warrantyEnd = entitlements["endDate"][0:10]
            except TypeError:
                warrantyEnd = "Expired"

            try:
                serviceLevel = entitlements["serviceLevelDescription"]
            except TypeError:
                serviceLevel = "No Warranty"
            
            # enter device informatino into .csv
            csvWriter.writerow([serial, warrantyEnd, serviceLevel])
        
        # decrement list length for next batch of 100 serial codes and reset variables
        listLength -= 1
        increment = 1
        tempList = []
        test_api_url = "api_url"
        if listLength > 0 and listLength < 1:
            listLength = 1