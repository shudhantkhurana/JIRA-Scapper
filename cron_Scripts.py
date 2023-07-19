def create_cron_file(cron_file_path, cron_entries):
    with open(cron_file_path, 'a') as cron_file:
        for entry in cron_entries:
            cron_file.write(f"{entry}\n")
    print(f"Cron file '{cron_file_path}' created.")


cron_file_path = ''
cron_entries = [
    "55 8 * * 1-5 ./python send_mail.py",
    "58 8 * * 1-5 ./python fetch_api.py",
    "0 17 * * 5 ./backup_appLog"
]
create_cron_file(cron_file_path, cron_entries)
