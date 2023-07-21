import requests
import logging.config
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
flask_logger = logging.getLogger('flask')



with open('port.txt','r') as f:
    port = f.read()
    
while True:
    
    response1 = requests.get(
        f'http://localhost:{port}/all',
        headers={'Content-Type': 'application/json'},
    )
    
    if response1.status_code == 200:
        flask_logger.info(f"GET HTTP request -- status-code : {response1.status_code}")
        
        response2 = requests.get(
            f'http://localhost:{port}/managers',
            headers={'Content-Type': 'application/json'},
        )
        
        if response2.status_code == 200:
            flask_logger.info(f"GET HTTP request -manager- status-code : {response2.status_code}")
        
            try:
                requests.get(
                    f'http://localhost:{port}/shutdown',
                    headers={'Content-Type': 'application/json'}
                )
            except:
                flask_logger.info("Server Shutdown Successful")
        
            break
        else:
            break
    else:
        break