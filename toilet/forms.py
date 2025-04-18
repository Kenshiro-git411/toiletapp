from django import forms
from .models import TrainLine, ToiletMaster
from toilet.models import Gender

class SearchStation(forms.Form):
    station_name = forms.CharField(
        label="駅名を検索",
        max_length=30,
        widget=forms.TextInput(attrs={
            "id": "station_input",
            "class": "block w-full p-2 ring-1 ring-gray-500 focus:ring-1 focus:ring-blue-500 focus:outline-none",
            "autocomplete": "off", # ブラウザの自動補完機能をオフにして、過去の入力値が候補として表示されないようにする。
            "placeholder": "入力候補から選択してください"
        })
    )

class Review(forms.Form):
    value = forms.IntegerField(
        label="きれいさ",
        min_value=1,
        max_value=5,
        required=True,
        widget=forms.NumberInput(attrs={
            "step":1,
            "class": "w-full p-1 ring-1 ring-gray-500 focus:ring-1 focus:ring-blue-500 focus:outline-none",
        }),
    )
    size = forms.IntegerField(
        label="広さ",
        min_value=1,
        max_value=5,
        required=True,
        widget=forms.NumberInput(attrs={
            "step":1,
            "class": "w-full p-1 ring-1 ring-gray-500 focus:ring-1 focus:ring-blue-500 focus:outline-none",
        }),
    )
    congestion = forms.IntegerField(
        label="混雑さ",
        min_value=1,
        max_value=5,
        required=True,
        widget=forms.NumberInput(attrs={
            "step":1,
            "class": "w-full p-1 ring-1 ring-gray-500 focus:ring-1 focus:ring-blue-500 focus:outline-none",
        }),
    )
    comment = forms.CharField(
        label="コメント",
        max_length=300,
        widget=forms.Textarea(attrs={
            "class": "w-full p-1 ring-1 ring-gray-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
        }),

    )

class SearchLine(forms.Form):
    line = forms.ModelChoiceField(
        queryset=TrainLine.objects.all(),
        widget=forms.Select(attrs={
            "id": "line_input",
            "class": "w-full sm:w-2/5 p-1 ring-1 ring-gray-400 focus:ring-1 focus:ring-blue-500 focus:outline-none rounded-none"
        }),
        label="路線",
        empty_label="路線を選択してください",
        required=True,
        error_messages={"required": "路線を選択してください"}
    )
    gender = forms.ChoiceField(
        choices=[(g.pk, g.type) for g in Gender.objects.all()],
        widget=forms.RadioSelect
    )


