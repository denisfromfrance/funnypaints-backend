from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny,
    IsAuthenticatedOrReadOnly,
)


from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from .models import ImageCategories, ModelImage, WallImage, PaintRequest, RequestStatus, Suit

from django.conf import settings

import os

# Create your views here.
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_painting_requests(request):
    response = {"status": "failed"}
    return Response(response)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
def get_user_list(request):
    response = {"status": "failed"}
    
    user_information = []
    for user in User.objects.all():
        user_information.append({
            "id": user.id,
            "firstName": user.first_name,
            "lastName": user.last_name,
            "email": user.email
        })

        if user.register_user is not None:
            user_information[-1]["phone"] = user.phone
            user_information[-1]["country"] = user.country
            user_information[-1]["state"] = user.state
            user_information[-1]["city"] = user.city
            user_information[-1]["user"] = user.user
    return Response(response)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
def get_images_of_categories(request):
    response = {"status": "failed"}
    
    images = []
    for image_category in ImageCategories.objects.all():
        images.append({
            "category": image_category.category,
            "images": [
                {
                    "id": model_image.id,
                    "image": model_image.image.url,
                    "productName": model_image.product_name
                    # "wall_images": [{"id": wall_image.id, "image": wall_image.image.url} for wall_image in model_image.wall_image_set.all()]
                } for model_image in image_category.modelimage_set.all()
            ]
        })
    
    response["status"] = "ok"
    return Response(response)



@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
def change_painting_request_status(request):
    response = {"status": "failed"}
    data = request.data

    try:
        requestID = data["requestID"]
        newStateID = data["newStatusID"]

        paintRequest = PaintRequest.objects.get(id=requestID)
        if paintRequest is not None:
            newStatus = RequestStatus.objects.get(id=newStateID)
            paintRequest.request_status = newStatus
            paintRequest.save()
            response["status"] = "ok"
    except Exception as e:
        print(e)
        pass
    return Response(response)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
def add_new_category(request):
    print(request.user)
    print(request.auth)
    response = {"status": "failed"}
    data = request.data
    try:
        categoryText = data["category"]
        category = ImageCategories.objects.create(category=categoryText)
        if category is not None:
            response["status"] = "ok"
    except:
        pass
    return Response(response)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
def add_model_images(request):
    response = {"status": "failed"}
    data = request.data

    print(data)

    try:
        categoryID = data["categoryID"]
        name = data["productName"]
        files = request.FILES.getlist("images")
        category = ImageCategories.objects.get(id=categoryID)
        if category is not None:
            for file in files:
                try:
                    model_image = ModelImage.objects.create(image=file, product_name=name, image_category=category)
                except Exception as e:
                    print(e)
        response["status"] = "ok"
    except Exception as exception:
        print(exception)
        pass
    return Response(response)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
def add_wall_images(request):
    response = {"status": "failed"}
    data = request.data

    print(data)

    try:
        # categoryID = data["modelImageID"]
        files = request.FILES.getlist("wallImages")

        # print(categoryID)
        print(files)
        # model_image = ModelImage.objects.get(id=categoryID)
        # if model_image is not None:

        for file in files:
            try:
                wall_image = WallImage.objects.create(image=file)
            except Exception as e:
                print(e)
                return Response(response)
            
        response["status"] = "ok"
    except Exception as exception:
        print(exception)
        pass
    return Response(response)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
def get_wall_images(request):
    response = {"status": "failed"}
    data = request.data

    print(data)

    try:
        # categoryID = data["modelImageID"]
        # print(categoryID)
        # model_image = ModelImage.objects.get(id=categoryID)
        # if model_image is not None:

        wallImages = WallImage.objects.all()
        wallImagesData = []
        for file in wallImages:
            try:
                wallImagesData.append({
                    "wallImageID": file.id,
                    "image": settings.DOMAIN + file.image.url})
            except Exception as e:
                print(e)
                return Response(response)
        response["wallImages"] = wallImagesData  
        response["status"] = "ok"
    except Exception as exception:
        print(exception)
        pass
    return Response(response)




@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_all_painting_requests(request):
    response = {"status": "failed"}
    requests_information = []
    if request.user.is_superuser:
        request_statuses = RequestStatus.objects.all()

        request_statuses_ids = [status.id for status in request_statuses]
        request_statuses_ids = sorted(request_statuses_ids)

        # print(request_statuses_ids)

        for request in PaintRequest.objects.all():
            try:
            # print(dir(request))
                userUploadedImages = request.userselectedimage_set.all()
                requests_information.append({
                    "id": request.id,
                    "wall_image": settings.DOMAIN + request.wall_image.image.url,
                    "model_image": settings.DOMAIN + request.model_image.image.url,
                    "request_status": request.request_status.status,
                    "datetime": request.datetime,
                    "user_uploaded_image": settings.DOMAIN + userUploadedImages[0].image.url if len(userUploadedImages) > 0 else "",
                    "user": {
                        "userID": request.user.id,
                        "firstName": request.user.first_name,
                        "lastName": request.user.last_name
                        }
                })

            
                # print(dir(request_statuses_ids))
                idIndex = int(request_statuses_ids.index(request.request_status.id))
                # print("Index", idIndex)
                if len(request_statuses_ids) > idIndex:
                    id = request_statuses_ids[idIndex + 1]
                    next_status = RequestStatus.objects.get(id=id)
                    requests_information[-1]["nextStatus"] = {
                        "id": next_status.id,
                        "status": next_status.status
                    }
            except Exception as e:
                print(e)
                pass
    else:
        for request in PaintRequest.objects.filter(user=request.user):
            userUploadedImages = request.userselectedimage_set.all()

            # print(dir(request))
            requests_information.append({
                "id": request.id,
                "wall_image": settings.DOMAIN + request.wall_image.image.url,
                "model_image": settings.DOMAIN + request.model_image.image.url,
                "request_status": request.request_status.status,
                "user_uploaded_image": settings.DOMAIN + userUploadedImages[0].image.url if len(userUploadedImages) > 0 else ""
            })
    
    response["status"] = "ok"
    response["requests"] = requests_information
    # print(response)
    return Response(response)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_category(request):
    response = {"status": "failed"}
    try:
        categoryID = request.data["categoryID"]
        imageCategories = ImageCategories.objects.get(id=categoryID)
        for image in imageCategories.modelimage_set.all():
            imagePath = image.image.path
            image.delete()
            os.remove(imagePath)
        imageCategories.delete()
        response["status"] = "ok"
    except Exception as e:
        print(e)
    return Response(response)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def rename_category(request):
    response = {"status": "failed"}
    try:
        categoryID = request.data["categoryID"]
        name = request.data["name"]
        imageCategories = ImageCategories.objects.get(id=categoryID)
        imageCategories.category = name
        imageCategories.save()
        response["status"] = "ok"
    except Exception as e:
        print(e)
    return Response(response)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_model(request):
    response = {"status": "failed"}
    try:
        modelImageID = request.data["modelID"]
        imageModel = ModelImage.objects.get(id=modelImageID)
        imagePath = imageModel.image.path
        imageModel.delete()
        os.remove(imagePath)
        response["status"] = "ok"
    except Exception as e:
        print(e)
    return Response(response)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def change_model(request):
    response = {"status": "failed"}
    print(request.data)
    model_image = None
    try:
        modelImageID = request.data["modelImageID"]
        model_image = ModelImage.objects.get(id=modelImageID)
    except:
        categoryID = request.data["categoryID"]
        category = ImageCategories.objects.get(id=categoryID)

        if category is not None:
            model_image = ModelImage.objects.create(
                image_category=category
            )

    if model_image is not None:
        try:
            file = request.FILES["modelImage"]
            try:
                model_image.image=file
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)

        try:
            modelImageName = request.data["name"]
            model_image.product_name = modelImageName
        except Exception as e:
            print(e)

        try:
            model_image.small_size_price = request.data["smallSizePrice"]
        except Exception as e:
            print(e)

        try:
            model_image.medium_size_price = request.data["mediumSizePrice"]
        except Exception as e:
            print(e)

        try:
            model_image.large_size_price = request.data["largeSizePrice"]
        except Exception as e:
            print(e)

        try:
            model_image.small_size_oil_paint_on_canvas_price = request.data["smallPaintSize"]
        except Exception as e:
            print(e)

        try:
            model_image.medium_size_oil_paint_on_canvas_price = request.data["mediumPaintSize"]
        except Exception as e:
            print(e)

        try:
            model_image.large_size_oil_paint_on_canvas_price = request.data["largePaintSize"]
        except Exception as e:
            print(e)

        try:
            model_image.small_size_print_on_metal = request.data["smallPrintMetalSize"]
        except Exception as e:
            print(e)

        try:
            model_image.medium_size_print_on_metal = request.data["mediumPrintMetalSize"]
        except Exception as e:
            print(e)

        try:
            model_image.large_size_print_on_metal = request.data["largePrintMetalSize"]
        except Exception as e:
            print(e)
        model_image.save()
        response["status"] = "ok"
    return Response(response)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_suits(request):
    response = {"status": "failed"}
    print(request)
    files = request.FILES
    print(files)
    for key, value in files.items():
        suit = Suit.objects.create(suit_image=value)

    response["status"] = "ok"
    
    return Response(response)



# @api_view(["POST"])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# def add_preview_image(request):
#     response = {"status": "failed"}
#     files = request.FILES

#     for key, value in files.items():
#         wallImage = WallImage.objects.create(image=value)

#     response["status"] = "ok"
#     return Response(response)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_preview_image(request):
    response = {"status": "failed"}
    previewImages = []

    for image in WallImage.objects.all():
        previewImages.append({
            "wallImageID": image.id,
            "image": settings.DOMAIN + image.image.url
        })

    response["previewImages"] = previewImages
    response["status"] = "ok"
    return Response(response)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_preview_image(request):
    response = {"status": "failed"}
    try:
        data = request.data
        imageID = data["imageID"]
        wallImage = WallImage.objects.get(id=imageID)
        if wallImage is not None:
            path = wallImage.image.path
            wallImage.delete()
            os.remove(path)
            response["status"] = "ok"
    except Exception as e:
        print(e)
        pass
    return Response(response)

