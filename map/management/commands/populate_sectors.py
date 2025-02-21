from django.core.management.base import BaseCommand
from map.models import Sector

class Command(BaseCommand):
    help = "Populate database with river basins in Thailand"

    def handle(self, *args, **kwargs):
        river_basins = [
            {"name": "แม่น้ำปิง (Ping River)", "latitude": 18.8000, "longitude": 99.0000, "image":"sector/image1.png"},
            
        ]

        for basin in river_basins:
            sector, created = Sector.objects.get_or_create(
                name=basin["name"],
                defaults={"latitude": basin["latitude"], "longitude": basin["longitude"], "image": basin["image"]}
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Added: {sector.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Already exists: {sector.name}"))
