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

from Data.models import Country, State, City
from django.conf import settings

import json

from Administrator.models import ModelImage, WallImage

# Create your views here.


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    response = {"response": "failed"}
    user = request.user
    data = request.data
    print(data)
    try:
        firstName = data["firstName"]
        if firstName != "":
            user.first_name = firstName
            print("Updated first name")
    except Exception as e:
        print(e)
        pass

    try:
        lastName = data["lastName"]
        if lastName != "":
            user.last_name = lastName
            print("Updated last name")
    except Exception as e:
        print(e)
        pass

    try:
        email = data["email"]
        if email != "":
            user.email = email
            print("Updated email")
    except Exception as e:
        print(e)
        pass

    print(dir(user))
    registeredUser = user.registereduser
    if registeredUser is not None:

        try:
            countryID = int(data["country"])
            country = Country.objects.get(id=countryID)
            registeredUser.country = country
        except Exception as e:
            print(e)

        try:
            stateID = int(data["state"])
            state = State.objects.get(id=stateID)
            registeredUser.state = state
        except Exception as e:
            print(e)

        try:
            cityID = int(data["city"])
            city = City.objects.get(id=cityID)
            registeredUser.city = city
        except Exception as e:
            print(e)

        try:
            street = data["street"]
            if street != "":
                registeredUser.street = street
                print("Updated street")
        except Exception as e:
            print(e)
            pass

        registeredUser.save()

    user.save()
    response["status"] = "ok"
    return Response(response)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    response = {"response": "failed"}
    user = request.user
    userInformation = {}

    userInformation["firstName"] = user.first_name
    userInformation["lastName"] = user.last_name
    userInformation["email"] = user.email


    # print(dir(user))
    registeredUser = user.registereduser
    if registeredUser is not None:
        userInformation["profileImage"] = settings.DOMAIN + registeredUser.profileImage.url
        userInformation["country"] = {
            "id": registeredUser.country.id,
            "name": registeredUser.country.name
        }

        userInformation["state"] = {
            "id": registeredUser.state.id,
            "name": registeredUser.state.name
        }
        userInformation["street"] = registeredUser.street

    response["profileInformation"] = userInformation
    response["status"] = "ok"
    return Response(response)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def upload_user_profile_image(request):
    response = {"response": "failed"}
    user = request.user
    files = request.FILES

    try:
        image = files["profileImage"]
        registeredUser = user.registereduser
        if registeredUser is not None:
            if len(files) > 0:
                registeredUser.profileImage = image
                registeredUser.save()
                response["status"] = "ok"
    except Exception as e:
        print(e)
        pass

    return Response(response)



@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
def add_item_to_cart(request):
    response = {"status": "failed"}
    try:
        data = request.data
        print(data)
        wall_image_id = data["wallImage"]
        model_image_id = data["modelImage"]
        variantInformation = json.loads(data["variantInformation"])
        # files = request.FILES["userSelectedImage"]

        modelImage = ModelImage.objects.get(id=model_image_id)
        modelImageURL = settings.DOMAIN + modelImage.image.url

        cart = request.session.get("cart", [])
        cart.append({
            "wallImageID": wall_image_id,
            "modelImageID": model_image_id,
            # "files": files,
            "modelImageURL": modelImageURL
        })

        request.session["cart"] = cart
        request.session.save()
        response["status"] = "ok"
    except Exception as e:
        print(e)
        pass
    return Response(response)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
def get_items_in_cart(request):
    response = {"status": "failed"}
    try:
        cart = request.session.get("cart", [])
        # print(dir(request.session))
        # print(request.session.session_key)
        print("Cart: ", cart)
        response["cart"] = cart
        response["status"] = "ok"
    except Exception as e:
        print(e)
        pass
    return Response(response)
