from django.db import models
from twilio.rest import Client
import os
# from dotenv import load_dotenv
from django.db.models.signals import post_save
from django.dispatch import receiver

# load_dotenv()

class Sector(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='sector/', default='sector/image1.png')
    latitude = models.FloatField()
    longitude = models.FloatField()

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
    rain_image = models.ImageField(upload_to='rain/',default='rain/rain.png') 
    suggestion_image = models.ImageField(upload_to='suggestion/', default='suggestion/predict.png')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=NORMAL)

    def is_dry(self):
        return self.status == self.DRY

    def __str__(self):
        return f"Result for {self.sector.name} - {self.month}"

class Announcement(models.Model):
    message = models.CharField(max_length=255, blank=False, null=False)

    def notify(self, phone):
        """Sends SMS notification."""
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        client = Client(account_sid, auth_token)

        sms = client.messages.create(
            messaging_service_sid=os.getenv("TWILIO_MESSAGING_SERVICE_SID"),
            body=self.message,
            to=phone
        )
        return sms.sid

    def broadcast(self):
        """Sends a notification to all members."""
        members = Member.objects.all()
        for member in members:
            self.notify(member.phone)

@receiver(post_save, sender=Announcement)
def send_announcement(sender, instance, created, **kwargs):
    if created:
        instance.broadcast()

class Member(models.Model):
    phone = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.phone
