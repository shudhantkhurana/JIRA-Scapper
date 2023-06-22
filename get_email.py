import requests
import json
from config import *
import logging.config
logging.config.fileConfig('logging.conf')


def fetch_email(accountId):
    
    # Set up authentication credentials
    username = jira_username()
    api_token = jira_keys()
    base_url = jira_url()
    api_url = base_url + '/rest/api/3'


    # Set up headers with authentication
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
    }
    
    
    # Construct the API request URL
    search_url = api_url + '/user/search'
    
    # Setting up Parameters
    query = {
    'accountId': f'{accountId}'
    }
    try:
        # Make the API request
        logging.info(f'Requesting Response for accountId : {accountId}')
        response = requests.get(search_url, auth=(username, api_token), headers=headers, params=query)
        
        # Check if the request was successful
        if response.status_code == 200:
            
            logging.info(f'Response Recieved for accountId : {accountId}')
            
            # Retrieve the JSON response
            json_response = response.json()
            
            # Fetching the e-mail Address
            userEmail = json_response[0]['emailAddress']
            
            # verifying
            if userEmail != 'null':
                logging.info(f'e-mail Address found for accountId : {accountId} ')
                return userEmail
                # type - str
            else:
                logging.error(f'No e-mail Address found for accountId : {accountId} ')
                return None
        
        else:
            logging.error(f"Request failed with status code {response.status_code}")
            return None
    except:
        logging.error('Something went Wrong!')    
        return None

