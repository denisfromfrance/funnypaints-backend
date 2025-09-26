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

from Administrator.models import RequestStatus, PaintRequest, WallImage, ModelImage, UserSelectedImage

# Create your views here.
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def request_art(request):
    response = {"status": "failed"}
    try:
        data = request.data
        wall_image_id = data["wallImage"]
        model_image_id = data["modelImage"]

        files = request.FILES.getlist("userSelectedImage")

        request_status = RequestStatus.objects.get(id=1)
        wall_image = WallImage.objects.get(id=wall_image_id)
        model_image = ModelImage.objects.get(id=model_image_id)

        paint_request = PaintRequest.objects.create(
            wall_image=wall_image,
            model_image=model_image,
            request_status=request_status,
            user=request.user
        )

        if paint_request is not None:
            user_selected_image = UserSelectedImage.objects.create(
                image=files[0],
                paintRequest=paint_request
            )
        print(data)
        print(wall_image_id)
        print(model_image_id)
        print(files[0])
    except Exception as e:
        print(e)
        
    return Response(response)
