from flask import Flask, render_template, request, jsonify, make_response
from flask_mail import Mail, Message
import mailConfig
from get_projects import allProjects
from get_issues import getIssues
from get_email import fetch_email
import logging.config
logging.config.fileConfig('flaskLogger.conf')

local_server = True
app = Flask(__name__)
mailConfig.app_config(app)
mail = Mail(app)

@app.route('/', methods=["GET"])
def index():
    try:
        projects = allProjects()
        for project in projects:
            projectName = project['projectName']
            projectKey = project['projectKey']
            allAssignee = getIssues(projectKey)
            if allAssignee == None:
                continue
            
            for assignee in allAssignee:
                if assignee != 'notAssigned':
                    accountId = assignee
                    email,displayName = fetch_email(accountId)
                    logging.info(f"{email},{displayName}")
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
                    msg.html = render_template('index.html', displayName=displayName,allStatusTypes=allStatusTypes)
                    
                    mail.send(msg)

        data = {
            "message":f"Email sent to all users"
        }
        status_code = 200
        response = make_response(jsonify(data),status_code)
        response.headers['Content-Type'] = 'appplication/json'
        return response
    except Exception as e:
        data = {
            "message":f"Failed to send the email error - {e}"
        }
        status_code = 500
        response = make_response(jsonify(data),status_code)
        response.headers['Content-Type'] = 'appplication/json'
        return response
        
        # return f'An error occurred while sending the email: {str(e)}'


if __name__ == '__main__':
    app.run(debug=True)
    