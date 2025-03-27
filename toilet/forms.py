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
    # toilet_name = forms.ModelChoiceField(
    #     label="トイレ場所を選択",
    #     queryset=ToiletMaster.objects.none(),
    #     empty_label="選択してください",
    #     widget=forms.Select(attrs={
    #         "id": "toilet_select",
    #         "class": "w-full max-w-md p-1 text-md"
    #     })
    # )

    # def __init__(self, *args, **kwargs):
    #     station_id = kwargs.pop("station_id", None)
    #     super().__init__(*args, **kwargs)

    #     if station_id:
    #         self.fields["toilet_name"].queryset = ToiletMaster.objects.filter(station_id=station_id)
    #     else:
    #         self.fields["toilet_name"].queryset = ToiletMaster.objects.all()


class Review(forms.Form):
    value = forms.IntegerField(
        label="評価点",
        min_value=1,
        max_value=5,
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

