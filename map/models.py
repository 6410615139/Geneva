from django.db import models
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()


class Sector(models.Model):
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    latitude = models.FloatField()  # Storing latitude
    longitude = models.FloatField()  # Storing longitude

    def get_or_create_result(self, month):
        result, created = Result.objects.get_or_create(sector=self, month=month)
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
    rain = models.TextField(blank=True)
    suggestion = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=NORMAL)

    def get_rain_forecast(self):
        return self.rain

    def get_suggestion(self):
        return self.suggestion

    def is_dry(self):
        return self.status == self.DRY

    def notify(self, phone):
        """Sends SMS notification when status is Dry."""
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            messaging_service_sid=os.getenv("TWILIO_MESSAGING_SERVICE_SID"),
            body="Warning: At {self.sector.name}, in month {self.month} is dry!",
            to=phone
        )
        return message.sid

    @classmethod
    def broadcast(cls):
        """Sends a notification to all members if any result is dry."""
        members = Member.objects.all()
        for member in members:
            cls.notify(member.phone)


class Member(models.Model):
    phone = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.phone
