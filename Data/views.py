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

# Create your views here.


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def get_categories(request):
    response = {"status": "failed"}

    categories_info = []

    try:
        categories = ImageCategories.objects.all()
        if categories is not None:
            for category in categories:
                categories_info.append({
                    "id": category.id,
                    "category": category.category,
                    "images": [{"imageID": image_model.id, "image": settings.DOMAIN + image_model.image.url} for image_model in category.modelimage_set.all()]
                })
        response["wallImages"] = [{"wallImageID": wall_image.id, "image": settings.DOMAIN + wall_image.image.url} for wall_image in WallImage.objects.all()]
        response["status"] = "ok"
    except Exception as e:
        print(e)
        pass
    response["categories"] = categories_info
    return Response(response)
