import os
import shutil
import datetime

def backup_log_file(file_path, backup_folder):
    # Extract file name and extension
    file_name = os.path.basename(file_path)
    file_name, file_extension = os.path.splitext(file_name)

    # Generate backup file name with date and time
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d--%H-%M")
    backup_file_name = f"{file_name}--{timestamp}{file_extension}"

    # Build destination path
    destination_path = os.path.join(backup_folder, backup_file_name)

    # Perform the backup by copying the file
    shutil.copy(file_path, destination_path)
    
def clear_file(log_file_path):
    with open(log_file_path,'w') as file:
        file.truncate(0)

# Usage example
log_file_path = './app.log'
backup_folder_path = './backup'
backup_log_file(log_file_path, backup_folder_path)
clear_file(log_file_path)