# config.py
import datetime
import os

base_folder_path = "./logs/"

today_date = datetime.date.today().strftime("%Y-%m-%d")

log_file_name = f"Stream_check_{today_date}.txt"

file_path = os.path.join(base_folder_path, log_file_name)

os.makedirs(base_folder_path, exist_ok=True)


email = "example@email.com"
username = "your_username"
password = "your_password"

outlookfolder = "Oa_oes"
outlooksubfolder = "2FA"
new_line = " "

auth_url = ""
full_url = ""
pipe = ""
stream = ""
orch = ""
tenant = ""
sub_tenant = ""
