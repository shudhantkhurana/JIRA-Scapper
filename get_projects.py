import requests
from config import *
import json
import logging.config
logging.config.fileConfig('logging.conf')


def allProjects():
    
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
    search_url = api_url + '/project/search'
    try:
        # Make the API request
        logging.info('Requesting projects for given Config')
        response = requests.get(search_url, auth=(username, api_token), headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            
            logging.info('Response recieved for given Config')
            
            # Retrieve the JSON response
            json_response = response.json()
            
            if len(json_response['values']) == 0:
                logging.error('No Projects found for given Config')
                return None
            else:
                # Fetching Project Keys and names
                project_key_list = []
                
                # appending values in the list
                for value in json_response['values']:
                    
                    project_key_list.append(
                        { 
                            'projectKey' : f"{value['key']}",
                            'projectName' : f"{value['name']}"
                        }
                    )
                logging.info('All projects Scraped for given')
                return project_key_list
                # type list of dict
        else:
            logging.error(f"Request to fetch all projects with given Config failed with status code {response.status_code}")
            return None
        
    except:
        logging.error('Something went wrong while fetching projects with given Config')
        return None
    
    