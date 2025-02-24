from django.shortcuts import render, get_object_or_404
from .models import Sector, Result
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from twilio.twiml.messaging_response import MessagingResponse
import logging

logger = logging.getLogger(__name__)

def sector_data(request):
    sectors = Sector.objects.values("id", "name", "latitude", "longitude")
    return JsonResponse(list(sectors), safe=False)

def map_view(request):
    """Displays all sectors on the map."""
    sectors = Sector.objects.all()
    data = {"sectors": sectors}
    return render(request, "map.html", data)

def sector_view(request, sector_id):
    """Displays details of a specific sector and handles form submission."""
    sector = get_object_or_404(Sector, id=sector_id)

    # If form is submitted, get the month and redirect to result_view
    month = request.GET.get("month")
    if month:
        return result_view(request, sector_id, month)

    data = {"sector": sector}
    return render(request, "sector.html", data)

def result_view(request, sector_id, month=None):
    """Displays the result for a given sector and month."""
    sector = get_object_or_404(Sector, id=sector_id)

    # Get month from request if not provided
    month = request.GET.get("month", month)

    if not month:
        return render(request, "error.html", {"message": "Please provide a valid month."})

    result = sector.get_or_create_result(month)

    data = {"sector": sector, "result": result}
    return render(request, "result.html", data)

@csrf_exempt
def twilio_webhook(request):
    """Handle incoming messages from Twilio."""
    if request.method == "POST":
        from_number = request.POST.get("From")
        message_body = request.POST.get("Body")

        logger.info(f"📩 Received SMS from {from_number}: {message_body}")

        # Process the message (e.g., store in DB, trigger actions, etc.)

        # Send a response back to Twilio
        response = MessagingResponse()
        response.message(f"Hello! We received your message: {message_body}")

        return HttpResponse(str(response), content_type="text/xml")

    return HttpResponse("Invalid request", status=400)

