import requests
from config import *
import json
# Set up authentication credentials
username = username()
api_token = keys()
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
jql = 'project = ES'

# Make the API request
response = requests.get(search_url, auth=(username, api_token), headers=headers, params={'jql': jql})

# storing the information
tasks = {
    'null' : []
}

# Check if the request was successful
if response.status_code == 200:
    # Retrieve the JSON response
    json_response = response.json()

    # Extract the list of issues
    issues = json_response['issues']
    count = 0
    for issue in range(len(issues)-1,-1,-1):
        if issues[issue]['fields']['issuetype']['name'] == 'Task':    # Only Tasks not Epics

            # segregating the tasks on the basis of account Id
            if issues[issue]['fields']['assignee'] == None:
                tasks['null'].append({'key': f"{issues[issue]['key']}", 'summary': f"{issues[issue]['fields']['summary']}", 'status' : f"{issues[issue]['fields']['status']['name']}" })
            else:
                if  issues[issue]['fields']['assignee']['accountId'] not in tasks:
                    # creating a list of issues
                    tasks[issues[issue]['fields']['assignee']['accountId']] = [{'key': f"{issues[issue]['key']}", 'summary': f"{issues[issue]['fields']['summary']}", 'status' : f"{issues[issue]['fields']['status']['name']}" }]
                else:
                    # appending in the list
                    tasks[issues[issue]['fields']['assignee']['accountId']].append({'key': f"{issues[issue]['key']}", 'summary': f"{issues[issue]['fields']['summary']}", 'status' : f"{issues[issue]['fields']['status']['name']}" })

            count += 1

    # Storing the total number of issues
    total_issues = json_response['total']

    tasks = json.loads(json.dumps(tasks, indent=4))
    print(tasks)
else:
    print(f"Request failed with status code {response.status_code}")
