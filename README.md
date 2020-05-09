# ExtractBusinessCardData
Extract the data and detect mobile number and email from mailing labels or business card
This application is written in python using Django framework.
For frontend we have https://github.com/farrukhrazzaqbutt/ExtractBusinessCardDataFrontEnd in angular 8.

Steps to run this Project:
1)Download this Project and unzip it.
2)Activate the Virtual Environment and Upgrade pip
        •Activate the virtual environment:Scripts\activate.bat
        •Then install all the dependent modules and packages related to the project using command and make sure you are running it in same path where requirement.txt file is present by- pip install -r requirement.txt.
3)We are using MYSql, so we have to change our setting.py file in project
        'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'database_name',
        'USER': 'user_name',
        'PASSWORD': password,
        'HOST': 'localhost',  # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
4)Do all migrations using these commands
        Python3 manage.py make makemigartions
        Python3 manage.py make migarte
5)now we can run our project
        python3 manage.py runserver
