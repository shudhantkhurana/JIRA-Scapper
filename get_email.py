import requests
import json
from config import *
import logging.config
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
app_logger = logging.getLogger('app')


def fetch_email(accountId):
    
    # Set up authentication credentials
    username = JIRA_USERNAME
    api_token = JIRA_API_KEY
    base_url = JIRA_URL
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
        app_logger.info(f'Requesting Response for accountId : {accountId}')
        response = requests.get(search_url, auth=(username, api_token), headers=headers, params=query)
        
        # Check if the request was successful
        if response.status_code == 200:
            
            app_logger.info(f'Response Recieved for accountId : {accountId}')
            
            # Retrieve the JSON response
            json_response = response.json()
            
            # Fetching the e-mail Address
            userEmail = json_response[0]['emailAddress']
            displayName = json_response[0]['displayName']
            
            # verifying
            if userEmail != 'null':
                app_logger.info(f'e-mail Address found for accountId : {accountId} ')
                return userEmail,displayName
                # type - str
            else:
                app_logger.error(f'No e-mail Address found for accountId : {accountId} ')
                return None
        
        else:
            app_logger.error(f"Request failed with status code {response.status_code}")
            return None
    except:
        app_logger.error(f'Something went Wrong while fetching e-mail Address for accountId : {accountId}')    
        return None

