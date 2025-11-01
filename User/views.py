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

from Administrator.models import *

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
        # print(data)
        wall_image_id = data["wallImage"]
        model_image_id = data["modelImage"]
        variantInformation = json.loads(data["variantInformation"])

        modelImage = ModelImage.objects.get(id=model_image_id)
        modelImageURL = settings.DOMAIN + modelImage.image.url

        cart = request.session.get("cart", [])
        id = 1

        if len(cart) > 0:
            id = cart[-1]["id"] + 1

        cart.append({
            "id": id,
            "wallImageID": wall_image_id,
            "modelImageID": model_image_id,
            # "files": files,
            "modelImageURL": modelImageURL,
            "variantInformation": variantInformation
        })

        try:
            # print(request.FILES)
            files = request.FILES
            file = files["userSelectedImage"]
            # print(file)
            tempUpload = TempUploads.objects.create(file=file)
            uploadFileURL = settings.DOMAIN + tempUpload.file.url
            # print(uploadFileURL)
            cart[-1]["userUploadedImage"] = tempUpload.id
            cart[-1]["userUploadedImagePath"] = uploadFileURL
            # print("Updated cart:", cart)
        except Exception as e:
            print(e)
            pass

        # cart = cart[:-1]

        request.session["cart"] = cart
        request.session.save()
        response["status"] = "ok"
    except Exception as e:
        print(e)
        pass
    return Response(response)


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def get_items_in_cart(request):
    response = {"status": "failed"}
    try:
        cart = request.session.get("cart", [])
        # print(dir(request.session))
        # print(request.session.session_key)
        # print("Cart: ", cart)
        cost = 0
        for itemIndex in range(len(cart)):
            cost = 0
            modelImage = ModelImage.objects.get(id=cart[itemIndex]["modelImageID"])
            productVariations = modelImage.productvarianthassize_set.all()
            # print(productVariations)
            for variantInformation in cart[itemIndex]["variantInformation"]["variantIDs"]:
                # print(type(variantInformation))
                variantID = variantInformation["variantID"]
                for productVariantHasSize in productVariations:
                    # print(productVariantHasSize.id)
                    if productVariantHasSize.variation.id == variantID:
                        # print(productVariantHasSize)
                        cost += productVariantHasSize.price
                # print(variantInformation)
                # for variantIDS in json.loads(variantInformation)["variantIDs"]:
                #     print(variantIDS)
            cart[itemIndex]["cost"] = cost
        response["cart"] = cart
        response["status"] = "ok"
    except Exception as e:
        print(e)
        pass
    return Response(response)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def remove_cart_item(request):
    try:
        id = request.data["id"]
        cart = request.session.get("cart", [])
        updatedCart = []
        for cartItem in cart:
            if cartItem["id"] != id:
                updatedCart.append(cartItem)
        request.session["cart"] = updatedCart
        return Response({"status": "failed"})
    except Exception as e:
        print(e)
        pass
    return Response({"status": "ok"})


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def clear_cart(request):
    request.session["cart"] = []
    return Response({"status": "ok"})


@api_view(["POST"])
@permission_classes([])
@authentication_classes([])
def get_invoice(request):
    response = {"status": "failed"}
    try:
        invoiceID = request.data["invoiceID"]
        invoice = Invoice.objects.get(id=invoiceID)
        if invoice is not None:
            paymentStatus = ""

            if invoice.order.payment_status == -1:
                paymentStatus = "Failed"
            elif invoice.order.payment_status == 0:
                paymentStatus = "Processing"
            elif invoice.order.payment_status == 1:
                paymentStatus = "Successful"

            invoiceData = {
                "invoiceID": invoice.invoice_number,
                "invoiceDate": invoice.invoice_date,
                "paymentDate": invoice.payment_date,
                "currency": invoice.currency,
                "paymentStatus": paymentStatus,
                "amount": invoice.amount
            }

            order = invoice.order

            orderedItems = {}
            for item in order.paintrequesthasproductvarianthassize_set.all():
                product = item.product
                if orderedItems.keys().__contains__(product.id):
                    variations = orderedItems[product.id]["variations"]
                    if variations.keys().__contains__(item.variation.variation):
                        information = variations[item.variation.variation]
                        sizes = information["sizes"]

                        if not sizes.__contains__(item.size.size):
                            sizes.append(f"{item.size.width}x{item.size.height}")
                        
                        information["sizes"] = sizes
                        variations[item.variation.variation] = information

                    orderedItems[product.id]["variations"] = variations
                else:
                    orderedItems[product.id] = {
                        "image": settings.DOMAIN + product.image.url,
                        "name": product.product_name,
                        "category": product.image_category.category,
                        "variations": {
                            f"{item.variation.variation}": {
                                "sizes": [f"{item.size.width}x{item.size.height}"]
                            }
                        }
                    }
                # order
                # user_uploaded_image
            print(invoiceData)
            response["invoiceData"] = invoiceData
            response["orderedData"] = orderedItems
            response["status"] = "ok"
    except Exception as e:
        print(e)
        pass

    print(response)
    return Response(response)
