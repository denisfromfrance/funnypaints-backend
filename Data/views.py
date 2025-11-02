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

from Administrator.models import ImageCategories, WallImage

from django.conf import settings

from Administrator.models import RequestStatus

from .models import *

from Administrator.models import Suit

# Create your views here.


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def get_categories(request):
    response = {"status": "failed"}

    categories_info = []

    try:
        categories = ImageCategories.objects.all().order_by('priority')
        if categories is not None:
            for category in categories:
                categories_info.append({
                    "id": category.id,
                    "priority": category.priority,
                    "category": category.category,
                    "images": []
                })

                for image_model in category.modelimage_set.all():
                    # print(dir(image_model))
                    productVariantInformation = {}
                    for productVariantHasSize in image_model.productvarianthassize_set.all():
                        # print(image_model.product_name)
                        # print(productVariantHasSize)
                        if productVariantInformation.keys().__contains__(productVariantHasSize.variation.variation):
                            productVariantInformation[productVariantHasSize.variation.variation]["sizes"].append(
                                {
                                    "id": productVariantHasSize.size.id,
                                    "sizeObj": {
                                        "id": productVariantHasSize.size.id,
                                        "size": productVariantHasSize.size.size,
                                        "width": productVariantHasSize.size.width,
                                        "height": productVariantHasSize.size.height,
                                        "unit": productVariantHasSize.size.unit,
                                        "price": productVariantHasSize.size.price
                                    },
                                    "price": productVariantHasSize.price
                                }
                            )
                        else:
                            productVariantInformation[productVariantHasSize.variation.variation] = {
                                "variation": {
                                    "id": productVariantHasSize.variation.id,
                                    "variation": productVariantHasSize.variation.variation,
                                },
                                "sizes": [
                                    {
                                        "id": productVariantHasSize.size.id, 
                                        "sizeObj": {
                                            "id": productVariantHasSize.size.id,
                                            "size": productVariantHasSize.size.size,
                                            "width": productVariantHasSize.size.width,
                                            "height": productVariantHasSize.size.height,
                                            "unit": productVariantHasSize.size.unit,
                                            "price": productVariantHasSize.size.price
                                        },
                                        "price": productVariantHasSize.price
                                    }
                                ]
                            }
                    categories_info[-1]["images"].append(
                        {
                            "imageID": image_model.id,
                            "categoryID": category.id,
                            "productName": image_model.product_name,
                            "image": settings.DOMAIN + image_model.image.url,
                            "smallSize": image_model.small_size_price,
                            "mediumSize": image_model.medium_size_price,
                            "largeSize": image_model.large_size_price,
                            "smallPaintOnCanvasSize": image_model.small_size_oil_paint_on_canvas_price,
                            "mediumPaintOnCanvasSize": image_model.medium_size_oil_paint_on_canvas_price,
                            "largePaintOnCanvasSize": image_model.large_size_oil_paint_on_canvas_price,
                            "smallPrintMetalSize": image_model.small_size_print_on_metal,
                            "mediumPrintMetalSize": image_model.medium_size_print_on_metal,
                            "largePrintMetalSize": image_model.large_size_print_on_metal,
                            "smallPrintPaperSize": image_model.small_size_print_on_paper,
                            "mediumPrintPaperSize": image_model.medium_size_print_on_paper,
                            "largePrintPaperSize": image_model.large_size_print_on_paper,
                            "variations": productVariantInformation.values()
                        }
                    )
        response["wallImages"] = [{"wallImageID": wall_image.id, "image": settings.DOMAIN +
                                   wall_image.image.url} for wall_image in WallImage.objects.all()]
        response["status"] = "ok"
    except Exception as e:
        print(e)
        pass
    response["categories"] = categories_info
    return Response(response)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
def get_painting_status(request):
    response = {"status": "failed"}

    status_info = []

    try:
        statuses = RequestStatus.objects.all()
        if len(statuses) > 0:
            for status in statuses:
                status_info.append({
                    "id": status.id,
                    "status": status.status,
                })
        response["status"] = "ok"
    except Exception as e:
        # print(e)
        pass
    response["statuses"] = status_info
    # print(status_info)
    return Response(response)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
def get_location_data(request):
    response = {"status": "failed"}
    data = request.GET
    print(data)
    status_info = []

    countries = Country.objects.all()
    states = State.objects.all()
    cities = City.objects.all()

    try:
        countryID = int(data["country"])
        print("Country ID: ", countryID)
        states = Country.objects.get(id=countryID).state_set.all()
        statesData = []
        for state in states:
            statesData.append({
                "id": state.id,
                "name": state.name
            })
        response["states"] = statesData
    except Exception as e:
        print(e)
        pass


    try:
        stateID = int(data["state"])
        cities = State.objects.get(id=stateID).city_set.all()
        cityData = []
        for city in cities:
            cityData.append({
                "id": city.id,
                "name": city.name
            })
        print("Getting cities")
        print(cities)
        print(cityData)
        response["cities"] = cityData
    except Exception as e:
        print(e)
        pass

    data = []
    for country in countries:
        data.append({
            "id": country.id,
            "name": country.name
        })
    response["countries"] = data
    response["status"] = "ok"
    print(response)
    return Response(response)



@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([AllowAny])
def get_painting_sizes(request):
    response = {"status": "failed"}
    sizes = []
    for size in Size.objects.all():
        sizes.append({
            "id": size.id,
            "size": size.size,
            "width": size.width,
            "height": size.height,
            "unit": size.unit,
            "price": size.price
        })

    response["status"] = "ok"
    response["sizes"] = sizes
    return Response(response)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_painting_size(request):
    response = {"status": "failed"}
    try:
        data = request.data
        size = data["size"]
        width = data["width"]
        height = data["height"]
        unit = data["unit"]
        price = data["price"]

        size = Size.objects.create(
            size=size,
            width=width,
            height=height,
            unit=unit,
            price=price
        )

        if size is not None:
            response["status"] = "ok"
    except Exception as e:
        print(e)
        pass
    return Response(response)


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def get_suits(request):
    response = {"status": "failed"}
    try:
        suitData = []
        suits = Suit.objects.all()
        for suit in suits:
            suitData.append({
                "id": suit.id,
                "suitImage": settings.DOMAIN + suit.suit_image.url
            })
        response["suits"] = suitData
        response["status"] = "ok"
    except Exception as e:
        print(e)
        pass
    return Response(response)
