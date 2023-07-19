import sqlite3

def getManagers(ProjectKey):
    
    # Connect to the database
    conn = sqlite3.connect('./databases/managers.db')
    cursor = conn.cursor()

    # Fetch the data
    cursor.execute('SELECT displayName, Email FROM projects WHERE projectName=?', (ProjectKey,))
    results = cursor.fetchall()

    # Close the connection
    conn.close()
    
    # Check if the result is found
    if results:
        return results
    else:
        return -1
