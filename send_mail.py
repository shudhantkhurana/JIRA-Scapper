from flask import Flask, render_template, request, jsonify, make_response
from flask_mail import Mail, Message
import mailConfig
from get_issues import getIssues
from get_projects import allProjects
from get_email import fetch_email
from config import JIRA_URL
from fetch_managers import getManagers
import logging.config
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
flask_logger = logging.getLogger('flask')
import os
import socket

local_server = True
app = Flask(__name__)
mailConfig.app_config(app)
mail = Mail(app)

@app.route('/', methods=["GET"])
def index():
    flask_logger.info(f"request -- Send email to all users")
    
    try:
        # fetching all projects
        projects = allProjects()
        for project in projects:
            projectName = project['projectName']
            projectKey = project['projectKey']
            
            # getting all issues and assignees
            allAssignee = getIssues(projectKey)
            if allAssignee == None:
                continue
            
            for assignee in allAssignee:
                if assignee != 'notAssigned':
                    accountId = assignee
                    
                    # fetching emailId and displayName
                    email,displayName = fetch_email(accountId)
                    
                    # creating a dict of the format
                    
                    # {
                    #     'status1' : [
                    #         {
                    #             'key' : 'issueId1',
                    #             'summary' : "Issue summary 1",
                    #         },
                    #         {
                    #             'key' : 'issueId2',
                    #             'summary' : "Issue summary 2",
                    #         },
                    #     ],
                    #     'status2' : [
                    #         {
                    #             'key' : 'issueId3',
                    #             'summary' : "Issue summary 3",
                    #         },
                    #         {
                    #             'key' : 'issueId4',
                    #             'summary' : "Issue summary 4",
                    #         },
                    #     ]
                    # }
                    
                    allStatusTypes = dict()
                    for issue in allAssignee[assignee]:
                        if issue['status'] not in allStatusTypes:
                            allStatusTypes[issue['status']] = None
                    
                    for issue in allAssignee[assignee]:
                        if allStatusTypes[issue['status']] == None:
                            allStatusTypes[issue['status']] = [issue]
                        else:
                            allStatusTypes[issue['status']].append(issue)
        

    
                    recipients = [email]
                    
                    subject = f'Assigned issues for project - {projectName}'

                    # Render the template with the desired data
                    msg = Message(subject=subject, recipients=recipients, sender='demo.shudhant@gmail.com')
                    msg.html = render_template('index.html', displayName=displayName,allStatusTypes=allStatusTypes,url=f'{JIRA_URL}/jira/software/projects/ES/boards/1?selectedIssue=')
                    
                    mail.send(msg)
                    flask_logger.info(f"Email sent to accountId : {accountId}")

        data = {
            'success' : True,
            "message":f"Email sent to all users"
        }
        status_code = 200
        response = make_response(jsonify(data),status_code)
        response.headers['Content-Type'] = 'appplication/json'
        
        
        flask_logger.info("Email Sent to all Users")
        
        return response
    
    
    except Exception as e:
        data = {
            'succcess' : False,
            "message":f"Failed to send the email error - {e}"
        }
        status_code = 500
        response = make_response(jsonify(data),status_code)
        response.headers['Content-Type'] = 'appplication/json'
        
        flask_logger.error(f"Failed to send email, error : {e}")
        
        return response
    
    
    
    
    
@app.route('/managers',methods=['GET'])
def sendEmailToManagers():
    flask_logger.info("request -- Send mail to all managers")
    
    try:
        projects = allProjects()
        for project in projects:
            projectName = project['projectName']
            projectKey = project['projectKey']
            
            issues = getIssues(projectKey)
            AllStatus =dict()
            
            for assignee in issues:
                for issue in issues[assignee]:
                    if issue['status'] not in AllStatus:
                        AllStatus[issue['status']] = []
            
            for assignee in issues:
                for issue in issues[assignee]:
                    AllStatus[issue['status']].append(issue)
            
        
            allManagers = getManagers(projectKey)
            
            if allManagers == -1:
                flask_logger.error(f"No manager found for project : {projectName}")
            else:
                for manager in allManagers:
                    managerName = manager[0]
                    managerEmail = manager[1]
                    
                    
                    recipients = [managerEmail]
                    
                    subject = f'All issues for project - {projectName}'
                    
                    msg = Message(subject=subject, recipients=recipients, sender='demo.shudhant@gmail.com')
                    msg.html = render_template('manager.html', managerName=managerName, AllStatus=AllStatus, url=f'{JIRA_URL}/jira/software/projects/ES/boards/1?selectedIssue=',projectName=projectName)
                    
                    mail.send(msg)
                    flask_logger.info(f'Email sent to {managerEmail}')
                    
        data = {
            'success' : True,
            'message' : 'Email sent to all managers'
        }
        status_code = 200
        response = make_response(jsonify(data),status_code)
        response.headers['Content-Type'] = 'appplication/json'
        
        flask_logger.info("Email sent to all Managers")

        return response
                    
    except Exception as e:
        data = {
            'succcess' : False,
            "message":f"Failed to send the email to manager, error - {e}"
        }
        status_code = 500
        response = make_response(jsonify(data),status_code)
        response.headers['Content-Type'] = 'appplication/json'
        
        flask_logger.error(f"Failed to send email to manager, error : {e}")
        
        return response
    
    
    
    
    
    

@app.route('/shutdown', methods=['GET'])
def stopServer():
    try:
        os._exit(0)
    
    except Exception as e:
        
        data = {
                'success' : True,
                "message":f"Server Shutdown Unsuccessful"
            }
        status_code = 500
        response = make_response(jsonify(data),status_code)
        response.headers['Content-Type'] = 'appplication/json'
    
        return response 

        
def setPort():
    
    sock = socket.socket()
    sock.bind(('',0))
    port = sock.getsockname()[1]
    
    return port

if __name__ == '__main__':
    
    port = setPort()
    
    with open('port.txt','w') as f:
        f.write(str(port))
    
    flask_logger.info(f"Server Running on Port Number {port}")
    flask_logger.info(f"Running on http://localhost:{port}")

    app.run(port=port)
    
    
    
    