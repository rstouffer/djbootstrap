# djbootstrap

To run server


Download django
pip install Django


Setup project

inside the djbootstrap folder run this command
django-admin startproject (project name here)



now inside the settings.py file in the project folder add the following to the installed_apps list
    'django.contrib.staticfiles',
    'polls.apps.PollsConfig',
    'phone_field',
    'localflavor',

now under the timezone vareable write your timezone ex: 'America/New_York'

under urlpatterns in urls write

path("", include('polls.urls')),