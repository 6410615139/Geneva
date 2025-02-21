from django.core.management.base import BaseCommand
from map.models import Sector

class Command(BaseCommand):
    help = "Populate database with river basins in Thailand"

    def handle(self, *args, **kwargs):
        river_basins = [
            {"name": "แม่น้ำปิง (Ping River)", "latitude": 18.8000, "longitude": 99.0000},
            {"name": "แม่น้ำเจ้าพระยา (Chao Phraya River)", "latitude": 15.2000, "longitude": 100.5000},
            {"name": "แม่น้ำโขง (Mekong River)", "latitude": 17.9500, "longitude": 102.6000},
            {"name": "แม่น้ำยม (Yom River)", "latitude": 17.2500, "longitude": 100.0000},
            {"name": "แม่น้ำน่าน (Nan River)", "latitude": 18.1000, "longitude": 100.8000},
            {"name": "แม่น้ำแม่กลอง (Mae Klong River)", "latitude": 13.9000, "longitude": 99.9500},
            {"name": "แม่น้ำมูล (Mun River)", "latitude": 15.0000, "longitude": 103.2000}
        ]

        for basin in river_basins:
            sector, created = Sector.objects.get_or_create(
                name=basin["name"],
                defaults={"latitude": basin["latitude"], "longitude": basin["longitude"]}
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Added: {sector.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Already exists: {sector.name}"))
