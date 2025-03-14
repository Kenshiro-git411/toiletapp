from django.shortcuts import render
from . import forms
from django.http import JsonResponse
from .models import TrainStation

# Create your views here.

def home(request):
    return render(request, 'toilet/home.html')

def search_toilet(request):
    if request.method == 'POST':
        search_form = forms.SearchStation(request.POST)
        if search_form.is_valid():
            station_name = search_form.cleaned_data['station_name']
            return render(request, 'toilet/search_result.html', {
                'station_name': station_name
            })
    else:
        search_form = forms.SearchStation()

    return render(request, 'toilet/search_toilet.html', context={
            'search_form': search_form,
        }
    )

def suggest_station(request):
    """駅名検索時の駅候補機能（DBから参照する）"""

    query = request.GET.get("query", "")
    if query:
        # icontainsを使って部分一致検索
        stations = TrainStation.objects.filter(station_name__icontains=query).values(
            "station_name", "train_line__train_line_name"
        )

        print(list(stations))

        return JsonResponse({"suggestions": list(stations)})
    
    return JsonResponse({"suggestions": []})