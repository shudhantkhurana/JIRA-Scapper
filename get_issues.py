import requests
from config import *
import json
import logging.config
logging.config.fileConfig('logging.conf')


def getIssues(projectKey):
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
    search_url = api_url + '/search'

    # Set up the JQL query to retrieve all issues
    jql = f'project = {projectKey}'

    # Make the API request
    try:
        response = requests.get(search_url, auth=(username, api_token), headers=headers, params={'jql': jql})
        logging.info(f'Requesting for issues for projectKey : {projectKey}')


        # Check if the request was successful
        if response.status_code == 200:
            logging.info(f'Response Recieved for projectKey : {projectKey}')
            # Retrieve the JSON response
            json_response = response.json()

            # storing the information
            tasks = {
            'notAssigned' : []
            }
            # Extract the list of issues
            issues = json_response['issues']
            
            # Scrapping the response
            count = 0       # couting the number of current tasks
            
            for issue in range(len(issues)-1,-1,-1):
                
                # Only Tasks not Epics
                if issues[issue]['fields']['issuetype']['name'] == 'Task':    

                    # segregating the tasks on the basis of account Id
                    if issues[issue]['fields']['assignee'] == None:
                        tasks['notAssigned'].append({'key': f"{issues[issue]['key']}", 'summary': f"{issues[issue]['fields']['summary']}", 'status' : f"{issues[issue]['fields']['status']['name']}" })
                    else:
                        if  issues[issue]['fields']['assignee']['accountId'] not in tasks:
                            # creating a list of issues
                            tasks[issues[issue]['fields']['assignee']['accountId']] = [{'key': f"{issues[issue]['key']}", 'summary': f"{issues[issue]['fields']['summary']}", 'status' : f"{issues[issue]['fields']['status']['name']}" }]
                        else:
                            # appending in the list
                            tasks[issues[issue]['fields']['assignee']['accountId']].append({'key': f"{issues[issue]['key']}", 'summary': f"{issues[issue]['fields']['summary']}", 'status' : f"{issues[issue]['fields']['status']['name']}" })

                    count += 1
            logging.info(f"{count} issuse(s) found for projectKey : {projectKey}")
            # Storing the total number of issues
            total_issues = json_response['total']
            tasks = json.loads(json.dumps(tasks, indent=4))
            logging.info(f'Response Scrapped Successfully for projectKey : {projectKey}')
            return tasks
            # type dict
        else:
            logging.error(f"Request to fetch issues for projectKey:{projectKey} failed with status code {response.status_code}")
            return None
            
    except:
        logging.error(f"Something went Wrong while fetching issues for projectKey : {projectKey}")
        return None
        
getIssues('ES')