from django.shortcuts import render, get_object_or_404
from .models import Sector, Result
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from twilio.twiml.messaging_response import MessagingResponse
import logging

logger = logging.getLogger(__name__)

def map_view(request):
    """Displays all sectors on the map."""
    sectors = Sector.objects.all()
    data = {"sectors": sectors}
    return render(request, "map.html", data)

def sector_map(request, sector_name):
    """Displays details of a specific sector and handles form submission."""
    sector = Sector.objects.filter(name='Ping', month='January').first()
    
    month = request.GET.get("month")
    if month:
        return result_view(request, sector_name, month)

    data = {"sector": sector}
    return render(request, "sector_map.html", data)

def sector_view(request, sector_name):
    """Displays details of a specific sector and handles form submission."""
    sector = Sector.objects.filter(name='Ping', month='January').first()
    
    month = request.GET.get("month")
    if month:
        return redirect("result_view", sector_name=sector_name, month=month)

    return render(request, "sector.html", {"sector": sector})

def result_view(request, sector_name, month=None):
    """Displays the result for a given sector and month."""
    sector = get_object_or_404(Sector, name=sector_name)

    # Get month from request if not provided
    month = request.GET.get("month", month)
    if not month:
        return render(request, "error.html", {"message": "Please provide a valid month."})

    result, created = Result.objects.get_or_create(sector=sector, month=month)

    return render(request, "result.html", {"sector": sector, "result": result})

def rain_view(request, sector_name):
    """Displays rainfall data for a specific sector."""
    month = request.GET.get("month", "January")
    
    sector = Sector.objects.filter(name=sector_name, month=month).first()
    
    return render(request, "rain.html", {"sector": sector, "month": month})


def spi_view(request, sector_name):
    """Displays SPI data for a specific sector."""
    month = request.GET.get("month", "January")
    
    sector = Sector.objects.filter(name=sector_name, month=month).first()

    return render(request, "spi.html", {"sector": sector, "month": month})


def warning_view(request, sector_name):
    """Displays drought warning data for a specific sector."""
    month = request.GET.get("month", "January")
    
    sector = Sector.objects.filter(name=sector_name, month=month).first()

    return render(request, "warning.html", {"sector": sector, "month": month})


def crop_view(request, sector_name):
    """Displays crop-related data for a specific sector."""
    month = request.GET.get("month", "January")
    
    sector = Sector.objects.filter(name=sector_name, month=month).first()

    return render(request, "cropping.html", {"sector": sector, "month": month})

def income_view(request, sector_name):
    """Displays crop-related data for a specific sector."""
    month = request.GET.get("month", "January")
    
    sector = Sector.objects.filter(name=sector_name, month=month).first()

    return render(request, "income.html", {"sector": sector, "month": month})

@csrf_exempt  # We need to exempt CSRF since Twilio doesn't use CSRF tokens
def twilio_webhook(request):
    """Securely handle incoming messages from Twilio."""
    if request.method != "POST":
        logger.warning("⚠️ Invalid request method")
        return HttpResponse("Invalid request", status=400)

    # Validate the request signature from Twilio
    validator = RequestValidator(TWILIO_AUTH_TOKEN)
    twilio_signature = request.headers.get("X-Twilio-Signature", "")

    request_valid = validator.validate(
        request.build_absolute_uri(), request.POST, twilio_signature
    )

    if not request_valid:
        logger.error("🚨 Unauthorized Twilio request detected!")
        return HttpResponse("Unauthorized", status=403)

    # Process incoming message
    from_number = request.POST.get("From")
    message_body = request.POST.get("Body")

    logger.info(f"📩 Securely received SMS from {from_number}: {message_body}")

    # Respond to Twilio with a message
    response = MessagingResponse()
    response.message(f"Hello! We received your message securely: {message_body}")

    return HttpResponse(str(response), content_type="application/xml")

