Generate base site : `django-admin startproject mysite`  
Generate sub site : `python manage.py startapp detections`  
Start site : `python manage.py runserver`  

Update models : `python manage.py makemigrations detections`  
Prepare migration : `python manage.py sqlmigrate detections 0001`  
Run migration : `python manage.py migrate`