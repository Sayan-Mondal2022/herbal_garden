from django.shortcuts import render, Http404
from .models import plants_collection
from django.conf import settings
from django.http import JsonResponse
import json


def explore_leaves(request):
    return render(request, 'explore/leaves.html')

# Create your views here.
def explore_home(request):
    return render(request, "explore/explore_main.html")

def explore_flowers(request):
    return render(request, "explore/flowers.html")

def explore_fruits(request):
    return render(request, "explore/fruits.html")

def explore_gums(request):
    return render(request, "explore/gums.html")

def explore_roots(request):
    return render(request, "explore/roots.html")


def specific_plant(request, slug):
    json_file_path = settings.BASE_DIR / "Explore" / "Dataset" / "leaves.json"

    try:
        with open(json_file_path, "r") as file:
            plants_data = json.load(file)
    except FileNotFoundError:
        raise Http404("The data file was not found.")
    except json.JSONDecodeError:
        raise Http404("The data file is corrupted.")
    
    print(f"Slug: {slug}")
    for plant in plants_data:
        print(f"Plant Name: {plant['name'].lower().replace(' ', '-')}")
    
    plant = next((plant for plant in plants_data if plant["name"].lower().replace(" ", "-") == slug), None)
    
    if plant is None:
        raise Http404("Plant not found")
    
    return render(request, "explore/specific_plant.html", {"plant": plant})

def search_plants(request):
    query = request.GET.get("q", "").lower() 
    json_file_path = settings.BASE_DIR / "Explore" / "Dataset" / "leaves.json"

    try:
        with open(json_file_path, "r") as file:
            plants_data = json.load(file)
    except FileNotFoundError:
        return JsonResponse({"error": "Data file not found."}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Data file is corrupted."}, status=500)

    # Filter plants based on the query
    filtered_plants = [
        plant for plant in plants_data
        if query in plant["name"].lower() or query in plant.get("description", "").lower()
    ]

    return JsonResponse(filtered_plants, safe=False)

