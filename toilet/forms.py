from django import forms
from .models import ToiletMaster

class SearchStation(forms.Form):
    station_name = forms.CharField(
        label="駅名を検索",
        max_length=30,
        widget=forms.TextInput(attrs={
            "id": "station_input",
            "class": "w-full max-w-md p-1 text-md",
            "onkeyup": "searchStation()",
            "autocomplete": "off" # ブラウザの自動補完機能をオフにして、過去の入力値が候補として表示されないようにする。
        })
    )
    toilet_name = forms.ModelChoiceField(
        label="トイレ場所を選択",
        queryset=ToiletMaster.objects.none(),
        empty_label="選択してください",
        widget=forms.Select(attrs={
            "id": "toilet_select",
            "class": "w-full max-w-md p-1 text-md"
        })
    )

