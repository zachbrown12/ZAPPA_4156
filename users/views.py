from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from rest_framework.decorators import api_view
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@api_view(["POST"])
def login_user(request):
    """
    Render a page to login the account
    """
    print("in here!")

    if request.user.is_authenticated:
        return redirect("profiles")

    # post the login request and redirect
    if request.method == "POST":
        username = request.data.get("username")
        password = request.data.get("password")

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

    return render(request, "login_register.html")


@csrf_exempt
def register_user(request):
    """
    Render a page to register a new user
    """
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
    return render(request, "login_register.html", context)


def logout_user(request):
    """
    Render a page to log out
    """
    logout(request)
    return redirect("login")


def profiles(request):
    """
    Render profile page
    """
    return render(request, "profiles.html")
