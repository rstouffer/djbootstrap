from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from djbootstrap.forms import SignupForm, LoginForm, ChangeInfo, SetUsername, SetPassword
from djbootstrap.models import GUID, ForgotMyPassword, ExtraInfo
import uuid

def index(request):
    if request.user.is_authenticated:
        HttpResponseRedirect("/welcome")

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/welcome")
    else:
        form = LoginForm()

    return render(request, "index.html", {"form": form})

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data["username"], form.cleaned_data["email"], form.cleaned_data["password"])
            user.save()

            extraData = ExtraInfo(
                user = user,
                first_name = form.cleaned_data["first_name"],
                last_name = form.cleaned_data["last_name"],

                company_name = form.cleaned_data["company_name"],

                address_l1 = form.cleaned_data["address_l1"],
                address_l2 = form.cleaned_data["address_l2"],

                city = form.cleaned_data["city"],
                state = form.cleaned_data["state"],
                zip_code = form.cleaned_data["zip_code"],

                phone = form.cleaned_data["phone"]
            )
            extraData.save()

            guid = GUID(user=user, guid=uuid.uuid4().hex)
            guid.save()

            print(guid.guid)
            return render(request, "verifyEmail.html")
    else:
        form = SignupForm()

    return render(request, "signup.html", {"form": form})

def welcome(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/")
    
    user = request.user

    try:
        GUID.objects.get(user=user)
        warning = True
    except GUID.DoesNotExist:
        warning = False

    return render(request, "welcome.html", {"username": user.username, "email": user.email, "warning": warning})

def changeInfo(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/")
    
    try:
        GUID.objects.get(user=request.user)
        return HttpResponseRedirect("/welcome")
    except GUID.DoesNotExist:
        pass

    user = request.user
    
    if request.method == "POST":
        form = ChangeInfo(request.POST)

        if form.is_valid() and authenticate(username=user.username, password=form.cleaned_data["prevPassword"]) == user:
            if form.cleaned_data["username"] != "":
                user.username = form.cleaned_data["username"]
            if form.cleaned_data["email"] != "":
                user.email = form.cleaned_data["email"]
            if form.cleaned_data["newPassword"] != "":
                user.set_password(form.cleaned_data["newPassword"])

            if form.cleaned_data["first_name"] != "":
                user.first_name = form.cleaned_data["first_name"]
            if form.cleaned_data["last_name"] != "":
                user.last_name = form.cleaned_data["last_name"]
            if form.cleaned_data["company_name"] != "":
                user.company_name = form.cleaned_data["company_name"]
            if form.cleaned_data["address_l1"] != "":
                user.address_l1 = form.cleaned_data["address_l1"]
            if form.cleaned_data["address_l2"] != "":
                user.address_l2 = form.cleaned_data["address_l2"]
            if form.cleaned_data["city"] != "":
                user.city = form.cleaned_data["city"]
            if form.cleaned_data["state"] != "":
                user.state = form.cleaned_data["state"]
            if form.cleaned_data["zip_code"] != "":
                user.zip_code = form.cleaned_data["zip_code"]
            if form.cleaned_data["phone"] != "":
                user.phone = form.cleaned_data["phone"]
            user.save()

            guid = GUID(user=user, guid=uuid.uuid4().hex)
            guid.save()

            print(guid.guid)
            return render(request, "verifyEmail.html")
    else:
        form = ChangeInfo()

    return render(request, "changeInfo.html", {"form": form})

def logout_page(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/")
    
    logout(request)
    return HttpResponseRedirect("/")

def verify_page(request, id):
    guid = GUID.objects.get(guid=id)
    login(request, guid.user, backend='django.contrib.auth.backends.ModelBackend')
    guid.delete()
    return HttpResponseRedirect("/welcome")

def forgot_my_password_start(request):
    if (request.method == "POST"):
        form = SetUsername(request.POST)

        if form.is_valid():
            user = User.objects.get(username=form.cleaned_data["username"])

            forgot = ForgotMyPassword(guid=uuid.uuid4().hex, user=user)
            forgot.save()
            print(forgot.guid)

            return render(request, "verifyEmail.html")
    else:
        form = SetUsername()
        
    return render(request, "getEmail.html", {"form": form})
    
def forgot_my_password_end(request, id):
    if (request.method == "POST"):
        form = SetPassword(request.POST)
        if form.is_valid():
            forgot = ForgotMyPassword.objects.get(guid=id)
            login(request, forgot.user, backend='django.contrib.auth.backends.ModelBackend')
            forgot.user.set_password(form.cleaned_data["password"])
            forgot.user.save()
            forgot.delete()
            
            return HttpResponseRedirect("/welcome")
    else:
        form = SetPassword()
        
    return render(request, "getPassword.html", {"id": id, "form": form})

def delete_account(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/")
    
    if request.method == "POST":
        request.user.delete()
        return HttpResponseRedirect("/")
    
    return render(request, "deleteAccount.html")