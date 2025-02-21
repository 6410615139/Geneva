from django.shortcuts import render, get_object_or_404
from .models import Sector, Result
from django.http import JsonResponse

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
