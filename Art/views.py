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

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File

import os
import json
import stripe

from django.utils import timezone

from Administrator.models import *

import datetime
import time

stripe.api_key = settings.STRIPE_SECRET_KEY
WEBHOOK_SECRET = settings.STRIPE_WEBHOOK_SECRET

def generate_invoice_number():
    now = datetime.datetime.now()
    timestamp = int(time.time() * 1000)
    invoice_number = f"INV-{now.year}-{now.month:02d}-{now.day:02d}-{timestamp}"
    return invoice_number

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


@api_view(["POST"])
@permission_classes([])
@authentication_classes([])
def make_payment(request):
    # print("Stripe API Key: ", settings.STRIPE_SECRET_KEY)
    if request.method == "POST":
        try:
            data = request.data
            print("Payment data: ", data)
            # amount = int(float(data["amount"]) * 100)

            orderCreated = False
            orderID = 0
            invoiceID = 0
            amount = 0
            try:
                billingDetails = data["billingDetails"]
                orderData = Order.objects.create(
                    first_name=billingDetails["firstName"],
                    last_name=billingDetails["lastName"],
                    company=billingDetails["company"],
                    country=billingDetails["country"],
                    billing_street_address=billingDetails["billingStreetAddress"],
                    shipping_street_address=billingDetails["shippingStreetAddress"],
                    shipping_destination_type=billingDetails["shippingDestinationType"],
                    post_code=billingDetails["postCode"],
                    city=billingDetails["city"],
                    province=billingDetails["province"],
                    phone=billingDetails["phone"],
                    email_address=billingDetails["emailAddress"],
                    notes=billingDetails["notes"],
                    payment_status=0
                )

                invoiceNumber = generate_invoice_number()

                invoice = Invoice.objects.create(
                    invoice_number=invoiceNumber,
                    order=orderData
                )

                invoiceID = invoice.id

                orderID = orderData.id

                for product in data["products"]:
                    wallImageID = product["wallImageID"]
                    modelImageID = product["modelImageID"]

                    userUploadedImage = None

                    try:
                        print(f"Trying to get user selected image of product {product['id']}")
                        userSelectedImage = product["userUploadedImage"]
                        tempUpload = TempUploads.objects.get(id=userSelectedImage)
                        fileName = os.path.basename(tempUpload.file.path)

                        with open(tempUpload.file.path, 'rb') as f:
                            userUploadedImage = UserSelectedImage.objects.create()
                            userUploadedImage.image.save(fileName, File(f), save=True)
                    except Exception as exception:
                        print(f"Error occurred when trying to get user selected image of product {product['id']}")
                        print(exception)
                        pass

                    wallImage = WallImage.objects.get(id=wallImageID)
                    modelImage = ModelImage.objects.get(id=modelImageID)

                    for variant in product["variantInformation"]["variantIDs"]:
                        variantID = variant["variantID"]
                        variation = ProductVariation.objects.get(id=variantID)

                        for sizeID in variant["sizes"]:
                            size = Size.objects.get(id=sizeID)

                            try:
                                productVariantHasSize = ProductVariantHasSize.objects.get(variation=variation, size=size, product=modelImage)
                                print(productVariantHasSize)
                                print(productVariantHasSize.price)
                                amount += productVariantHasSize.price
                            except Exception as e:
                                print(e)

                            orderedProduct = PaintRequestHasProductVariantHasSize.objects.create(
                                product=modelImage,
                                wallImage=wallImage,
                                variation=variation,
                                size=size,
                                order=orderData
                            )

                            if userUploadedImage is not None:
                                orderedProduct.user_uploaded_image = userUploadedImage
                                orderedProduct.save()

                if orderData is not None:
                    orderCreated = True
            except Exception as e:
                # print(e)
                pass

            amount = 50
            currency = data.get("currency", "usd")
            print(f"Charging amount: {amount}")
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                metadata={
                    "integration_check": "accept_a_payment",
                    "orderID": f"ORDER-{orderID}",
                    "invoiceID": f"INV-{invoice.id}"
                }
            )

            # print({
            #     "clientSecret": intent.client_secret
            # })
            return Response({
                "clientSecret": intent.client_secret,
                "invoiceID": invoiceID
            })
        except Exception as e:
            print(e)
            return Response({"": ""})


{
    "api_version": "2023-08-16",
    "created": 1761897281,
    "data": {
        "object": {
            "amount": 50,
            "amount_capturable": 0,
            "amount_details": {
                "tip": {}
            },
            "amount_received": 0,
            "application": None,
            "application_fee_amount": None,
            "automatic_payment_methods": {
                "allow_redirects": "always",
                "enabled": True
            },
            "canceled_at": None,
            "cancellation_reason": None,
            "capture_method": "automatic",
            "client_secret": "pi_3SODATHAel19XjBl0HFgMYUm_secret_jY4wIBY0VLH6o3kyxwIPwQ17d",
            "confirmation_method": "automatic",
            "created": 1761897281,
            "currency": "usd",
            "customer": None,
            "description": None,
            "excluded_payment_method_types": None,
            "id": "pi_3SODATHAel19XjBl0HFgMYUm",
            "invoice": None,
            "last_payment_error": None,
            "latest_charge": None,
            "livemode": False,
            "metadata": {
                "integration_check": "accept_a_payment",
                "orderID": "ORDER-24"
            },
            "next_action": None,
            "object": "payment_intent",
            "on_behalf_of": None,
            "payment_method": None,
            "payment_method_configuration_details": {
                "id": "pmc_1SMZqoHAel19XjBlxZyupwed",
                "parent": None
            },
            "payment_method_options": {
                "card": {
                    "installments": None,
                    "mandate_options": None,
                    "network": None,
                    "request_three_d_secure": "automatic"
                },
                "cashapp": {}
            },
            "payment_method_types": [
                "card",
                "cashapp"
            ],
            "processing": None,
            "receipt_email": None,
            "review": None,
            "setup_future_usage": None,
            "shipping": None,
            "source": None,
            "statement_descriptor": None,
            "statement_descriptor_suffix": None,
            "status": "requires_payment_method",
            "transfer_data": None,
            "transfer_group": None
        }
    },
    "id": "evt_3SODATHAel19XjBl0zSBwmsu",
    "livemode": False,
    "object": "event",
    "pending_webhooks": 2,
    "request": {
        "id": "req_P85RauF4YbpRpf",
        "idempotency_key": "ff37ce9e-b0fd-4005-bfec-208bec560329"
    },
    "type": "payment_intent.created"
}


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, WEBHOOK_SECRET
        )
    except ValueError as e:
        print(e)
        return JsonResponse({"error": "Invalid payload"}, status=400)
    except stripe.error.SignatureVerificationError as e:
        print(e)
        return JsonResponse({"error": "Invalid Signature"}, status=400)

    invoice = None
    print(event)
    if event["type"] == "payment_intent.succeeded":
        paymentIntent = event["data"]["object"]
        orderID = paymentIntent["metadata"].get("orderID")
        orderID = orderID.split("-")

        invoiceID = paymentIntent["metadata"].get("invoiceID")
        invoiceID = invoiceID.split("-")
        if len(invoiceID) > 1:
            invoiceID = invoiceID[1]
            if invoiceID:
                currency = paymentIntent["currency"]
                total = paymentIntent["amount"]

                invoice = Invoice.objects.get(id=invoiceID)
                invoice.invoice_date = timezone.now().date()
                invoice.payment_date = timezone.now().date()
                invoice.currency=currency
                invoice.save()

        if len(orderID) > 1:
            orderID = int(orderID[1])
            if orderID:
                order = Order.objects.get(id=orderID)
                order.payment_status=0
                order.save()
                print(order)
                # request.session["cart"] = []
        print("Payment succeeded for: ", paymentIntent["id"])
    elif event["type"] == "payment_intent.payment_failed":
        error_message = event["data"]["object"]["last_payment_error"]["message"]
        print("Payment failed: ", error_message)
    elif event["type"] == "charge.succeeded":
        invoiceID = event["data"]["object"]["metadata"].get("invoiceID")
        invoiceID = invoiceID.split("-")
        if len(invoiceID) > 1:
            invoiceID = invoiceID[1]
            if invoiceID:
                currency = event["data"]["object"]["currency"]
                total = event["data"]["object"]["amount"]

                invoice = Invoice.objects.get(id=invoiceID)
                invoice.currency = currency
                invoice.order.payment_status = 1
                invoice.order.save()
                invoice.amount = total
                invoice.save()

    response = {"status": "success"}

    return JsonResponse(response)
