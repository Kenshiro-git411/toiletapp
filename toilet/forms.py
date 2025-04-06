from django import forms
from .models import TrainLine, ToiletMaster
from toilet.models import Gender

class SearchStation(forms.Form):
    station_name = forms.CharField(
        label="駅名を検索",
        max_length=30,
        widget=forms.TextInput(attrs={
            "id": "station_input",
            "class": "block w-full p-2 border border-gray-300 focus:ring-1 focus:ring-blue-500 focus:outline-none",
            # "onkeyup": "searchStation()",
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
            "class": "w-full p-1",
        }),
    )
    size = forms.IntegerField(
        label="広さ",
        min_value=1,
        max_value=5,
        required=True,
        widget=forms.NumberInput(attrs={
            "step":1,
            "class": "w-full p-1",
        }),
    )
    congestion = forms.IntegerField(
        label="混雑さ",
        min_value=1,
        max_value=5,
        required=True,
        widget=forms.NumberInput(attrs={
            "step":1,
            "class": "w-full p-1",
        }),
    )
    comment = forms.CharField(
        label="コメント",
        max_length=300,
        widget=forms.Textarea(attrs={
            "class": "w-full p-1"
        }),

    )

class SearchLine(forms.Form):
    line = forms.ModelChoiceField(
        queryset=TrainLine.objects.all(),
        widget=forms.Select(attrs={
            "id": "line_input",
            "class": "w-3/5 sm:w-2/5 p-1"
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


