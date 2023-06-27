# djbootstrap

To run server


Download django
pip install Django


Setup project

inside the djbootstrap folder run this command
django-admin startproject (project name here)



now inside the settings.py file in the project folder add the following to the installed_apps list
    'djbootstrap.apps.DjbootstrapConfig',
    'phone_field',
    'localflavor',

also write this at the end
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'youremail@gmail.com'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

now under the timezone vareable write your timezone ex: 'America/New_York'

under urlpatterns in urls write

path("", include('djbootstrap.urls')),

be sure to delete anything that is already in that list


also to update the database the commands are
python manage.py makemigrations djbootstrap
python manage.py migrate