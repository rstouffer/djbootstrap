from django.core.mail import send_mail
from django.shortcuts import render

def authenicate_email(request, guid):
    print(guid)
    #send_mail("activate email", "test test test", "ryry2nd@gmail.com", ["ryry2nd@gmail.com"], fail_silently=False)
    return render(request, "verifyEmail.html")