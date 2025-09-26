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

from .models import ImageCategories, ModelImage, WallImage, PaintRequest, RequestStatus

from django.conf import settings

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
                    "image": model_image.image.url,
                    "wall_images": [{"id": wall_image.id, "image": wall_image.image.url} for wall_image in model_image.wall_image_set.all()]
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
        newStateID = data["newStateID"]

        paintRequest = PaintRequest.objects.get(id=requestID)
        if paintRequest is not None:
            newStatus = RequestStatus.objects.get(id=newStateID)
            paintRequest.request_status = newStatus
            paintRequest.save()
            response["status"] = "ok"
    except:
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
        files = request.FILES.getlist("images")
        category = ImageCategories.objects.get(id=categoryID)
        if category is not None:
            for file in files:
                try:
                    model_image = ModelImage.objects.create(image=file, image_category=category)
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
        categoryID = data["modelImageID"]
        files = request.FILES.getlist("wallImages")

        print(categoryID)
        print(files)
        model_image = ModelImage.objects.get(id=categoryID)
        if model_image is not None:
            for file in files:
                try:
                    wall_image = WallImage.objects.create(image=file, model_image=model_image)
                except Exception as e:
                    print(e)
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

        print(request_statuses_ids)

        for request in PaintRequest.objects.all():
            # print(dir(request))
            requests_information.append({
                "id": request.id,
                "wall_image": settings.DOMAIN + request.wall_image.image.url,
                "model_image": settings.DOMAIN + request.model_image.image.url,
                "request_status": request.request_status.status,
                "user_uploaded_image": settings.DOMAIN + request.userselectedimage_set.all()[0].image.url,
                "user": {
                    "userID": request.user.id,
                    "firstName": request.user.first_name,
                    "lastName": request.user.last_name
                    }
            })

            try:
                # print(dir(request_statuses_ids))
                idIndex = int(request_statuses_ids.index(request.request_status.id))
                print("Index", idIndex)
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
            print(dir(request))
            requests_information.append({
                "id": request.id,
                "wall_image": settings.DOMAIN + request.wall_image.image.url,
                "model_image": settings.DOMAIN + request.model_image.image.url,
                "request_status": request.request_status.status,
                "user_uploaded_image": settings.DOMAIN + request.userselectedimage_set.all()[0].image.url
            })
    
    response["status"] = "ok"
    response["requests"] = requests_information
    print(response)
    return Response(response)

