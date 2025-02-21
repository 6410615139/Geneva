from django.shortcuts import render
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

def map_view(request):
    return render(request, "map.html")
    
def location_detail(request, location_id):
    return render(request, "location_detail.html", {"location_id": location_id})

def prediction_view(request, location_id, month):
    return render(request, "prediction.html", {"location_id": location_id})

def prediction(request, location_id, month):
    return render(request, "prediction.html", {"location_id": location_id})

def notification():
    account_sid = os.getenv("account_sid")
    auth_token = os.getenv("auth_token")
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        messaging_service_sid=os.getenv("messaging_service_sid"),
        body='Dry',
        to='+18777804236'
        )

