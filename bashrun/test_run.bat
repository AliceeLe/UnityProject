@echo off
cd /d "T:\VTV\Apps\Unity Project\UnityProject"
call .venv\Scripts\activate
python "T:\VTV\Apps\Unity Project\UnityProject\src\sendgrid_mail.py"
