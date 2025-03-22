from django.shortcuts import render, get_object_or_404
from . import forms
from django.http import JsonResponse
from .models import TrainStation, ToiletMaster, MaleToilet, FemaleToilet, MultiFunctionalToilet

# Create your views here.

def home(request):
    return render(request, 'toilet/home.html')

def search_toilet(request):
    if request.method == 'POST':
        search_form = forms.SearchStation(request.POST)
        print(search_form)
        station_id = request.POST.get("station_id")
        print("受け取ったPOSTデータ:", request.POST)
        print("選択された駅ID:", station_id)
        if search_form.is_valid():

            station_id = request.POST.get("station_id")

            # DBから該当するトイレを取得する
            toilets = ToiletMaster.objects.filter(station_id=station_id)
            male_toilets = MaleToilet.objects.filter(toilet_id__station_id=station_id)
            female_toilets = FemaleToilet.objects.filter(toilet_id__station_id=station_id)
            multifunctional_toilets = MultiFunctionalToilet.objects.filter(toilet_id__station_id=station_id)
            
            # 一致したトイレ情報を格納するリスト
            toilet_data = []

            # 各トイレの場所と照合して、データを収集
            for toilet in toilets:
                toilet_place = toilet.place
                matched_male = male_toilets.filter(toilet_id__place=toilet_place).first()
                matched_female = female_toilets.filter(toilet_id__place=toilet_place).first()
                matched_multifunctional = multifunctional_toilets.filter(toilet_id__place=toilet_place).first()

                # 一致したデータをリストに格納
                toilet_data.append({
                    "place": toilet_place,
                    "male": matched_male,
                    "female": matched_female,
                    "multifunctional": matched_multifunctional
                })

                # 一致したデータをリストに格納
                print("toilet_data", toilet_data)

            return render(request, 'toilet/search_result.html', context={
                'toilet_data': toilet_data
            })
        else:
            print("フォームエラー:", search_form.errors) # エラーの確認
    else:
        search_form = forms.SearchStation()

    return render(request, 'toilet/search_toilet.html', context={
            'search_form': search_form,
        }
    )

def suggest_station(request):
    """駅名検索時の駅候補機能（DBから参照する）"""

    query = request.GET.get("query", "")
    print(query) # 入力された文字列を受け取る
    if query:
        # icontainsを使って部分一致検索
        stations = TrainStation.objects.filter(station_name__icontains=query).values(
            "id", "station_name", "train_line__train_line_name"
        )

        print(list(stations))

        return JsonResponse({"suggestions": list(stations)})

    return JsonResponse({"suggestions": []})

def male_toilet_info(request, male_pk):
    """トイレpkに紐づく男性トイレ情報を返す"""

    toilet = get_object_or_404(MaleToilet, pk=male_pk)
    print(toilet)

    station_name = toilet.toilet_id.station_id.station_name
    place = toilet.toilet_id.place

    toilet_info = [
        ("改札内外", toilet.toilet_id.station_ticket_gate_id),
        ("設置階", toilet.toilet_id.floor),
        ("利用時間", toilet.toilet_id.get_opening_hours),
        ("個室数", toilet.toilet_stall),
        ("小便器数", toilet.urial),
        ("近い改札口", toilet.toilet_id.near_gate),
        ("近いホーム", toilet.toilet_id.near_home_num),
        ("近い車両番号", toilet.toilet_id.near_train_door_num),
        ("温水洗浄便座", toilet.warm_water_washing_toilet_seat_display),
        ("おむつ交換設備", toilet.child_facility_display),
        ("バリアフリートイレ", toilet.barrier_free_toilet_display),
        ("車いす対応", toilet.wheelchair_display),
        ("経路", toilet.toilet_id.toilet_root),
    ]

    return render(request, 'toilet/search_result_toilet_info.html', {
        "station_name": station_name,
        "place": place,
        "toilet_info": toilet_info
    })

def female_toilet_info(request, female_pk):
    """トイレpkに紐づく女性トイレ情報を返す"""

    toilet = get_object_or_404(FemaleToilet, pk=female_pk)

    toilet_info = [
        ("改札内外", toilet.toilet_id.station_ticket_gate_id),
        ("設置階", toilet.toilet_id.floor),
        ("利用時間", toilet.toilet_id.get_opening_hours),
        ("個室数", toilet.toilet_stall),
        ("近い改札口", toilet.toilet_id.near_gate),
        ("近いホーム", toilet.toilet_id.near_home_num),
        ("近い車両番号", toilet.toilet_id.near_train_door_num),
        ("パウダールーム", toilet.powder_room_display),
        ("温水洗浄便座", toilet.warm_water_washing_toilet_seat_display),
        ("おむつ交換設備", toilet.child_facility_display),
        ("バリアフリートイレ", toilet.barrier_free_toilet_display),
        ("車いす対応", toilet.wheelchair_display),
        ("経路", toilet.toilet_id.toilet_root),
    ]

    return render(request, 'toilet/search_result_toilet_info.html', {
        "toilet_info": toilet_info
    })

def multifunctional_toilet_info(request, multi_pk):
    """トイレpkに紐づく多機能トイレ情報を返す"""

    toilet = get_object_or_404(MultiFunctionalToilet, pk=multi_pk)

    toilet_info = [
        ("改札内外", toilet.toilet_id.station_ticket_gate_id),
        ("設置階", toilet.toilet_id.floor),
        ("利用時間", toilet.toilet_id.get_opening_hours),
        ("個室数", toilet.toilet_stall),
        ("近い改札口", toilet.toilet_id.near_gate),
        ("近いホーム", toilet.toilet_id.near_home_num),
        ("近い車両番号", toilet.toilet_id.near_train_door_num),
        ("温水洗浄便座", toilet.warm_water_washing_toilet_seat_display),
        ("おむつ交換設備", toilet.child_facility_display),
        ("バリアフリートイレ", toilet.barrier_free_toilet_display),
        ("車いす対応", toilet.wheelchair_display),
        ("経路", toilet.toilet_id.toilet_root),
    ]

    return render(request, 'toilet/search_result_toilet_info.html', {
        "toilet_info": toilet_info
    })