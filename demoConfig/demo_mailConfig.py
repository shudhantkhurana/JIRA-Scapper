def app_config(app):
    app.config['MAIL_SERVER'] = 'Eg. smtp.office365.com'
    app.config['MAIL_PORT'] = 587  # or your mail server port
    app.config['MAIL_USE_TLS'] = True  # enable if required
    app.config['MAIL_USERNAME'] = 'your Email Id'
    app.config['MAIL_PASSWORD'] = 'password of your email id'
    # app.config['TIMEOUT'] = 5
    
# After adding your Configurations in above format, save and rename this file as "mailConfig.py" in root directory