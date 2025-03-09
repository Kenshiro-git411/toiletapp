from django import forms
from .models import TrainStation

class SearchStation(forms.Form):
    station_name = forms.CharField(
        label="駅名を検索",
        max_length=30,
        widget=forms.TextInput(attrs={
            "id": "station_input",
            "onkeyup": "searchStation()",
            "autocomplete": "off"
        })
    )