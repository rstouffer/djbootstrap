# djbootstrap

Setup project:

this is just the app, so you will have to create the project yourself as well as create a virtual environment

be sure to put this in the installed apps in settings.py
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