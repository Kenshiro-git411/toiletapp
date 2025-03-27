from django.shortcuts import render, get_object_or_404
from . import forms
from django.http import JsonResponse
from .models import TrainStation, ToiletMaster, MaleToilet, FemaleToilet, MultiFunctionalToilet
from decimal import Decimal, ROUND_DOWN

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

    # MaleToiletテーブルからデータを取得
    toilet = get_object_or_404(MaleToilet, pk=male_pk)
    print(toilet)

    station_name = toilet.toilet_id.station_id.station_name
    place = toilet.toilet_id.place
    value = Decimal(toilet.value)
    value = value.quantize(Decimal("0.0"), rounding=ROUND_DOWN)
    root = toilet.toilet_id.toilet_root
    gen = toilet.gender.pk

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
    ]

    return render(request, 'toilet/search_result_toilet_info.html', {
        "toilet": toilet,
        "station_name": station_name,
        "place": place,
        "value": value,
        "toilet_info": toilet_info,
        "root": root,
        "gender": gen,
    })

def female_toilet_info(request, female_pk):
    """トイレpkに紐づく女性トイレ情報を返す"""

    # FemaleToiletテーブルからデータを取得
    toilet = get_object_or_404(FemaleToilet, pk=female_pk)

    station_name = toilet.toilet_id.station_id.station_name
    place = toilet.toilet_id.place
    value = Decimal(toilet.value)
    value = value.quantize(Decimal("0.0"), rounding=ROUND_DOWN)
    root = toilet.toilet_id.toilet_root
    gen = toilet.gender.pk

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
    ]

    return render(request, 'toilet/search_result_toilet_info.html', {
        "toilet": toilet,
        "station_name": station_name,
        "place": place,
        "value": value,
        "toilet_info": toilet_info,
        "root": root,
        "gender": gen,
    })

def multifunctional_toilet_info(request, multi_pk):
    """トイレpkに紐づく多機能トイレ情報を返す"""

    # MultiFunctionalToiletテーブルからデータを取得
    toilet = get_object_or_404(MultiFunctionalToilet, pk=multi_pk)

    station_name = toilet.toilet_id.station_id.station_name
    place = toilet.toilet_id.place
    value = Decimal(toilet.value)
    value = value.quantize(Decimal("0.0"), rounding=ROUND_DOWN)
    root = toilet.toilet_id.toilet_root
    gen = toilet.gender.pk

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
    ]

    return render(request, 'toilet/search_result_toilet_info.html', {
        "toilet": toilet,
        "station_name": station_name,
        "place": place,
        "value": value,
        "toilet_info": toilet_info,
        "root": root,
        "gender": gen,
    })

def change_toilet_data(request, toilet_pk, gender_num):

    print("toilet_pk", toilet_pk)
    print("gender_num", gender_num)

    try:
        if gender_num == 1:
            toilet = get_object_or_404(MaleToilet, toilet_id=toilet_pk)
            # 小便器数
            urial = toilet.urial
        elif gender_num == 2:
            toilet = get_object_or_404(FemaleToilet, toilet_id=toilet_pk)
            powder_room = toilet.powder_room_display()
        elif gender_num == 3:
            toilet = get_object_or_404(MultiFunctionalToilet, toilet_id=toilet_pk)
        else:
            return JsonResponse({"error": "無効なgender値です"}, status=400)
    except Exception as e:
        print("データを取得出来ませんでした")
        return JsonResponse({"error": f"データを取得できませんでした。存在しないデータの可能性があります。:{str(e)}"}, status=500)

    print("toilet", toilet)

    # 駅名
    station_name = toilet.toilet_id.station_id.station_name
    # トイレ場所
    place = toilet.toilet_id.place
    # 改札内外
    in_out_station_ticket_gate = toilet.toilet_id.station_ticket_gate_id.station_ticket_gate
    # 評価
    value = Decimal(toilet.value)
    value = value.quantize(Decimal("0.0"), rounding=ROUND_DOWN)
    # 設置階
    floor = toilet.toilet_id.floor
    # 利用時間
    time = f"{toilet.toilet_id.open_time}～{toilet.toilet_id.close_time}"
    # 個室数
    toilet_stall = toilet.toilet_stall
    # 近い改札口
    near_gate = toilet.toilet_id.near_gate
    # 近いホーム
    near_home_num = toilet.toilet_id.near_home_num
    # 近い車両番号
    near_train_door_num = toilet.toilet_id.near_train_door_num
    # 温水洗浄便座
    warm_water_washing_toilet_seat = toilet.warm_water_washing_toilet_seat_display()
    # おむつ交換設備
    child_facility = toilet.child_facility_display()
    # バリアフリートイレ
    barrier_free_toilet = toilet.barrier_free_toilet_display()
    # 車いす対応
    wheelchair = toilet.wheelchair_display()
    # 経路
    root = toilet.toilet_id.toilet_root
    # 性別id
    gen = toilet.gender.pk

    # javascriptでデータを受け取るには、Json形式でレスポンスするのが一般的で、適しているため、JsonResponseを使用する。
    if gender_num == 1:
        toilet_info = [
            {"label": "改札内外", "value": in_out_station_ticket_gate},
            {"label": "設置階", "value": floor},
            {"label": "利用時間", "value": time},
            {"label": "個室数", "value": toilet_stall},
            {"label": "小便器数", "value": urial},
            {"label": "近い改札口", "value": near_gate},
            {"label": "近いホーム", "value": near_home_num},
            {"label": "近い車両番号", "value": near_train_door_num},
            {"label": "温水洗浄便座", "value": warm_water_washing_toilet_seat},
            {"label": "おむつ交換設備", "value": child_facility},
            {"label": "バリアフリートイレ", "value": barrier_free_toilet},
            {"label": "車いす対応", "value": wheelchair},
        ]
    elif gender_num == 2:
        toilet_info = [
            {"label": "改札内外", "value": in_out_station_ticket_gate},
            {"label": "設置階", "value": floor},
            {"label": "利用時間", "value": time},
            {"label": "個室数", "value": toilet_stall},
            {"label": "近い改札口", "value": near_gate},
            {"label": "近いホーム", "value": near_home_num},
            {"label": "近い車両番号", "value": near_train_door_num},
            {"label": "パウダールーム", "value": powder_room},
            {"label": "温水洗浄便座", "value": warm_water_washing_toilet_seat},
            {"label": "おむつ交換設備", "value": child_facility},
            {"label": "バリアフリートイレ", "value": barrier_free_toilet},
            {"label": "車いす対応", "value": wheelchair},
        ]
    else:
        toilet_info = [
            {"label": "改札内外", "value": in_out_station_ticket_gate},
            {"label": "設置階", "value": floor},
            {"label": "利用時間", "value": time},
            {"label": "個室数", "value": toilet_stall},
            {"label": "近い改札口", "value": near_gate},
            {"label": "近いホーム", "value": near_home_num},
            {"label": "近い車両番号", "value": near_train_door_num},
            {"label": "温水洗浄便座", "value": warm_water_washing_toilet_seat},
            {"label": "おむつ交換設備", "value": child_facility},
            {"label": "バリアフリートイレ", "value": barrier_free_toilet},
            {"label": "車いす対応", "value": wheelchair},
        ]

    return JsonResponse({
        "toilet": {
            "id": toilet.pk,
            "station_name": station_name,
            "place": place,
            "value": value,
            "toilet_info": toilet_info,
            "root": root,
            "gender": gen,
        }
    })

def toilet_review(request):
    "レビューボタン押されたときの処理"

    if request.method == 'POST':
        pass
    else:
        review_form = forms.Review()

    return render(request, 'toilet/toilet_review.html', context={
            'review_form': review_form,
        }
    )