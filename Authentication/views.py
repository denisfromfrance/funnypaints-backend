from django.shortcuts import render
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
)

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password, make_password


from Administrator.models import RegisteredUser
from Data.models import Country, State, City

# Create your views here.
@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def register_user(request):
    response = {"status": "failed", "message": ""}
    data = request.data


    try:
        first_name = data["firstName"]
        last_name = data["lastName"]
        email = data["email"]
        password = data["password"]
        password_confirmation = data["confirmationPassword"]
        phone = data["phone"]
        # country = Country.objects.get(id=data["country"])
        # state = State.objects.get(data["state"])
        # city = City.objects.get(data["city"])

        if password == password_confirmation:
            user = User.objects.create(first_name=first_name, last_name=last_name, username=first_name + " " + last_name, email=email, password=make_password(password))
            if user is not None:
                registered_user = RegisteredUser.objects.create(
                    phone=phone,
                    # country=country,
                    # state=state,
                    # city=city,
                    user=user
                )
                if registered_user is not None:
                    refresh = RefreshToken.for_user(user)
                    access = refresh.access_token
                    response["access"] = str(access)
                    response["refresh"] = str(refresh)
                    response["status"] = "ok"
        else:
            response["message"] = "Passwords do not match!"

    except Exception as e:
        print(e)
        response["message"] = "Please fill all the fields!"
    return Response(response)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def login_user(request):
    response = {"status": "failed", "message": "", "refresh": "", "access": ""}
    data = request.data
    email = data["email"]
    password = data["password"]
    # remember = data["rememberMe"]

    try:
        user = User.objects.get(email=email)
        if user is not None:
            # login(request, user)
            try:
                print(user)
                if user.check_password(password):
                    refresh = RefreshToken.for_user(user)
                    access = refresh.access_token
                    response["access"] = str(access)
                    response["refresh"] = str(refresh)
                    response["status"] = "ok"
                else:
                    # print(exception)
                    response["message"] = "password is incorrect!"
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
        response["message"] = "User with the provided credentials couldn't find!"
    return Response(response)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def sign_in_admin(request):
    response = {"status": "failed", "message": "", "refresh": "", "access": ""}
    data = request.data
    username = data["username"]
    password = data["password"]

    try:
        user = User.objects.get(username=username)
        if user is not None:
            if user.check_password(password):
                if user.is_superuser:
                    refresh = RefreshToken.for_user(user)
                    access = refresh.access_token
                    response["access"] = str(access)
                    response["refresh"] = str(refresh)
                    response["status"] = "ok"
                else:
                    response["message"] = "You are not an admin user!"
            else:
                response["message"] = "password is incorrect!"
    except User.DoesNotExist:
        response["message"] = "User with the provided credentials couldn't find!"
    return Response(response)