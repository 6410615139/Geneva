from django.db import models
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

class Sector(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='sector/', null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def get_or_create_result(self, month):
        result, created = Result.objects.get_or_create(sector=self, month=month)
        if result.status == "Dry":
            result.broadcast()
        return result

    def __str__(self):
        return self.name


class Result(models.Model):
    DRY = "Dry"
    NORMAL = "Normal"
    HUMID = "Humid"

    STATUS_CHOICES = [
        (DRY, "Dry"),
        (NORMAL, "Normal"),
        (HUMID, "Humid"),
    ]

    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name="results")
    month = models.CharField(max_length=20)
    rain_image = models.ImageField(upload_to='rain/', null=True, blank=True)  # Fixed duplicate field
    suggestion_image = models.ImageField(upload_to='suggestion/', null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=NORMAL)

    def is_dry(self):
        return self.status == self.DRY

    def notify(self, phone):
        """Sends SMS notification when status is Dry."""
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            messaging_service_sid=os.getenv("TWILIO_MESSAGING_SERVICE_SID"),
            body=f"Warning: At {self.sector.name}, in month {self.month}, it is dry!",
            to=phone
        )
        return message.sid

    def broadcast(self):
        """Sends a notification to all members if any result is dry."""
        members = Member.objects.all()
        for member in members:
            self.notify(member.phone)

    def __str__(self):
        return f"Result for {self.sector.name} - {self.month}"


class Member(models.Model):
    phone = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.phone
