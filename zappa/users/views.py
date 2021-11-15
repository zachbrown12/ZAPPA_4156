from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# render a page to login the account
def login_user(request):
    if request.user.is_authenticated:
        return redirect("profiles")

    # post the login request and redirect
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # get the authorization
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            messages.error(request, f"Username does not exist: {e}")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("profiles")
        else:
            messages.error(request, "Username or password is incorrect")

    return render(request, "users/login_register.html")


# render a page to register a new user
def register_user(request):
    page = "register"
    form = UserCreationForm()

    # post the register request and redirect to the account page
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "User account was created")

            login(request, user)
            return redirect("profiles")

        else:
            messages.error(request, "An error has occurred during registration!")

    context = {"page": page, "form": form}
    return render(request, "users/login_register.html", context)


# log out the user page
def logout_user(request):
    logout(request)
    return redirect("login")


# render profile page
def profiles(request):
    return render(request, "users/profiles.html")
