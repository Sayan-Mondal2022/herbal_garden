from django.shortcuts import render
from .models import *

def search_plants(request):
    query = request.GET.get('q', '')
    results = []
    
    if query:
        # Search in MongoDB using text index
        results = plants_collection.find({
            '$or': [
                {'name': {'$regex': query, '$options': 'i'}},  # Case-insensitive name search
                {'category': {'$regex': query, '$options': 'i'}},  # Category search
                {'description': {'$regex': query, '$options': 'i'}},  # Description search
                {'benefits': {'$regex': query, '$options': 'i'}},  # Benefits search
                {'uses': {'$regex': query, '$options': 'i'}}  # Uses search
            ]
        })
        
        # Convert cursor to list
        results = list(results)

    return render(request, 'search/search_results.html', {
        'query': query,
        'results': results
    })