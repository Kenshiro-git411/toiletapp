from django.shortcuts import render, get_object_or_404, redirect
from . import forms
from django.http import JsonResponse
from .models import TrainLine, TrainStation, ToiletMaster, MaleToilet, FemaleToilet, MultiFunctionalToilet, Comment
from decimal import Decimal, ROUND_DOWN
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from accounts.models import Gender, User
from django.db.models import F


def home(request):
    return render(request, 'toilet/home.html')

def search_toilet(request):
    if request.method == 'POST':
        search_form = forms.SearchStation(request.POST)
        station_id = request.POST.get("station_id")
        # print("受け取ったPOSTデータ:", request.POST)
        # print("選択された駅ID:", station_id)

        station_id = request.POST.get("station_id")
        # 検索のidをセッションに保存する
        request.session["search_station_id"] = station_id

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

        return render(request, 'toilet/search_result.html', context={
            'toilet_data': toilet_data
        })
        # else:
            # print("フォームエラー:", search_form.errors) # エラーの確認
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

def toilet_info(request, pk, gender):
    # print("pk", pk)
    # print("gender", gender)

    try:
        if gender == 1:
            toilet = get_object_or_404(MaleToilet, pk=pk)
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
        elif gender == 2:
            toilet = get_object_or_404(FemaleToilet, pk=pk)
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
        elif gender == 3:
            toilet = get_object_or_404(MultiFunctionalToilet, pk=pk)
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

        station_name = toilet.toilet_id.station_id.station_name
        place = toilet.toilet_id.place
        value = Decimal(toilet.value)
        value = value.quantize(Decimal("0.0"), rounding=ROUND_DOWN)
        size = Decimal(toilet.size)
        size = size.quantize(Decimal("0.0"), rounding=ROUND_DOWN)
        congestion = Decimal(toilet.congestion)
        congestion = congestion.quantize(Decimal("0.0"), rounding=ROUND_DOWN)
        root = toilet.toilet_id.toilet_root

        comments = Comment.objects.filter(toilet=toilet.toilet_id, gender=gender)
        # print(comments)
        if not comments.exists():
            print("コメントはありません")
            comments = ""

        return render(request, 'toilet/search_result_toilet_info.html', {
            "toilet": toilet,
            "station_name": station_name,
            "place": place,
            "value": value,
            "size": size,
            "congestion": congestion,
            "toilet_info": toilet_info,
            "root": root,
            "gender": gender,
            "comments": comments,
        })

    except Exception as e:
        print("データを取得出来ませんでした", e)
        return render(request, 'toilet/search_result_toilet_info.html', {})


def change_toilet_data(request, toilet_pk, gender_num):

    # print("toilet_pk", toilet_pk)
    # print("gender_num", gender_num)

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

    # print("toilet", toilet)

    # トイレpk(ToiletMasterテーブルのpk)
    toilet_pk = toilet.toilet_id.pk
    # トイレid(各性別のトイレテーブルのid)
    toilet_id = toilet.pk
    # 駅名
    station_name = toilet.toilet_id.station_id.station_name
    # トイレ場所
    place = toilet.toilet_id.place
    # 改札内外
    in_out_station_ticket_gate = toilet.toilet_id.station_ticket_gate_id.station_ticket_gate
    # 評価
    value = Decimal(toilet.value)
    value = value.quantize(Decimal("0.0"), rounding=ROUND_DOWN)
    # 広さ
    size = Decimal(toilet.size)
    size = size.quantize(Decimal("0.0"), rounding=ROUND_DOWN)
    # 混雑さ
    congestion = Decimal(toilet.congestion)
    congestion = congestion.quantize(Decimal("0.0"), rounding=ROUND_DOWN)
    # 設置階
    floor = toilet.toilet_id.floor
    # 利用時間
    # time = f"{toilet.toilet_id.open_time}～{toilet.toilet_id.close_time}"
    time = toilet.toilet_id.get_opening_hours()
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
    # コメント
    comments = Comment.objects.select_related("user").filter(gender=gen, toilet=toilet_pk)
    print(comments)
    if comments.exists():
        comments = list(comments.values(
            "user",
            "user__username",
            "comment",
            "data_create"
        ))
    else:
        comments = ""


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

    print("レスポンス前")
    return JsonResponse({
        "toilet": {
            "toilet_pk": toilet_pk,
            "id": toilet_id, # 各性別のトイレpk
            "station_name": station_name,
            "place": place,
            "value": value,
            "size": size,
            "congestion": congestion,
            "toilet_info": toilet_info,
            "root": root,
            "gender": gen,
            "comments": comments,
        },
    })

@login_required(login_url='/accounts/user_login')
def toilet_review(request, toilet_id, gender):
    "レビューボタン押されたときの処理"

    # print("toilet_id:", toilet_id)
    # print("gender:", gender)
    # print("user:", request.user.pk)

    try:
        if gender == 1:
            toilet = get_object_or_404(MaleToilet, toilet_id=toilet_id)
        elif gender == 2:
            toilet = get_object_or_404(FemaleToilet, toilet_id=toilet_id)
        elif gender == 3:
            toilet = get_object_or_404(MultiFunctionalToilet, toilet_id=toilet_id)
        else:
            print("gender値が不正です")
            raise ValueError(f"不正なgender値:{gender}")

        if toilet is None:
            raise ValueError(f"toilet_id={toilet_id} のデータが見つかりません")

        if request.method == 'POST':
            review_form = forms.Review(request.POST)

            if review_form.is_valid():
                gender_instance = get_object_or_404(Gender, pk=gender)
                user_instance = get_object_or_404(User, pk=request.user.pk)
                toilet_instance = get_object_or_404(ToiletMaster, pk=toilet_id)

                comment_data = Comment.objects.create(
                    user=user_instance,
                    comment=review_form.cleaned_data["comment"],
                    value=review_form.cleaned_data["value"],
                    size=review_form.cleaned_data["size"],
                    congestion=review_form.cleaned_data["congestion"],
                    gender=gender_instance,
                    toilet=toilet_instance,
                )
                data_dict = {
                    "value": review_form.cleaned_data["value"],
                    "size": review_form.cleaned_data["size"],
                    "congestion": review_form.cleaned_data["congestion"],
                    "gender": gender,
                    "toilet_id": toilet_id, # toilet_idはToiletMasterテーブルのpk
                }
                calculate_value_size_congestion(data_dict)

                return redirect('toilet:toilet_info', pk=toilet.pk, gender=gender)
        else:
            review_form = forms.Review()

        return render(request, 'toilet/toilet_review.html', context={
                'toilet': toilet,
                'review_form': review_form,
            }
        )

    except ValueError as e:
        # print(f"ジェンダー値不正error:{e}")
        return HttpResponseBadRequest(f"無効なリクエスト: {e}")
    
    except Exception as e:
        print("データを取得出来ませんでした")
        return HttpResponseBadRequest("エラーが発生しました")
    
def calculate_value_size_congestion(data_dict):
    gender = data_dict["gender"]
    value = data_dict["value"]
    size = data_dict["size"]
    congestion = data_dict["congestion"]
    toilet_id = data_dict["toilet_id"]

    if gender == 1:
        # きれいさの平均を算出
        total_value = MaleToilet.objects.filter(toilet_id=toilet_id).first().value

        # 広さの平均を算出
        total_size = MaleToilet.objects.filter(toilet_id=toilet_id).first().size

        # 空き具合の平均を算出
        total_congestion = MaleToilet.objects.filter(toilet_id=toilet_id).first().congestion

        toilet = MaleToilet.objects.filter(toilet_id=toilet_id).first()

    elif gender == 2:
        # きれいさの平均を算出
        total_value = FemaleToilet.objects.filter(toilet_id=toilet_id).first().value

        # 広さの平均を算出
        total_size = FemaleToilet.objects.filter(toilet_id=toilet_id).first().size

        # 空き具合の平均を算出
        total_congestion = FemaleToilet.objects.filter(toilet_id=toilet_id).first().congestion

        toilet = FemaleToilet.objects.filter(toilet_id=toilet_id).first()

    elif gender == 3:
        # きれいさの平均を算出
        total_value = MultiFunctionalToilet.objects.filter(toilet_id=toilet_id).first().value
        
        # 広さの平均を算出
        total_size = MultiFunctionalToilet.objects.filter(toilet_id=toilet_id).first().size
        
        # 空き具合の平均を算出
        total_congestion = MultiFunctionalToilet.objects.filter(toilet_id=toilet_id).first().congestion

        toilet = MultiFunctionalToilet.objects.filter(toilet_id=toilet_id).first()
    else:
        raise ValueError("不正gender値が設定されました")

    # コメントの数 + デフォルトで最初に登録されているデータ1件
    length = (len(Comment.objects.filter(toilet_id=toilet_id, gender=gender)) + 1)

    # きれいさの総合値
    """
    総合値の計算方法（加重平均）
    (total_value * (length - 1))の計算式は現在登録されているvalue(平均値)から
    先ほどコメントテーブルに登録した1件分を引いた数を掛けることで前回分までの合計値を算出。
    ((前回分までの合計値) + value) / lengthは、前回分までの合計値に今回分のvalueを
    足すことで今回分までの合計値を算出し、コメント全体の数で割ることで平均値を算出する。
    """
    total_value = ((total_value * (length - 1)) + value) / length
    # 広さの総合値
    total_size = ((total_size * (length - 1)) + size) / length
    # 混み具合の総合値
    total_congestion = ((total_congestion * (length - 1)) + congestion) / length

    # データ更新
    toilet.value = round(total_value, 1)
    toilet.size = round(total_size, 1)
    toilet.congestion = round(total_congestion, 1)
    toilet.save()


def toilet_rank(request):
    if request.method == "POST":
        search_line_form = forms.SearchLine(request.POST)

        line = request.POST.get("line")
        gender = request.POST.get("gender")
        toilets = get_toilet_rank_queryset(line, gender)

        line_obj = TrainLine.objects.filter(pk=line).first

        return render(request, 'toilet/toilet_rank.html', context={
            "line":line_obj,
            "toilets": toilets,
            "gender": gender,
            "search_line_form": search_line_form,
        })

    else:
        search_line_form = forms.SearchLine()
        return render(request, 'toilet/toilet_rank.html', context={
            "search_line_form": search_line_form,
        })

def get_toilet_object_rank(request, line, gender):
    gender = int(gender)

    try:
        toilets = get_toilet_rank_queryset(line, gender)
        return JsonResponse ({
            "toilets": {
                "toilet_value": list(toilets["toilet_value"].values("toilet_id", "toilet_id__station_id__station_name", "toilet_id__place", "value")),

                "toilet_size": list(toilets["toilet_size"].values("toilet_id", "toilet_id__station_id__station_name", "toilet_id__place", "size")),

                "toilet_congestion": list(toilets["toilet_congestion"].values("toilet_id", "toilet_id__station_id__station_name", "toilet_id__place", "congestion")),
            },
            "gender": gender,
        })
    except ValueError:
        return JsonResponse({"error": "無効なgender"}, status=400)
        

def get_toilet_rank_queryset(line, gender):
    gender = int(gender)

    if gender == 1:
        # 男性トイレのオブジェクトを取得
        return {
            "toilet_value": MaleToilet.objects.filter(toilet_id__station_id__train_line=line).order_by('value').reverse(),
            "toilet_size": MaleToilet.objects.filter(toilet_id__station_id__train_line=line).order_by('size').reverse(),
            "toilet_congestion": MaleToilet.objects.filter(toilet_id__station_id__train_line=line).order_by('congestion').reverse()
        }

    elif gender == 2:
        # 女性トイレのオブジェクトを取得
        return {
            "toilet_value": FemaleToilet.objects.filter(toilet_id__station_id__train_line=line).order_by('value').reverse(),
            "toilet_size": FemaleToilet.objects.filter(toilet_id__station_id__train_line=line).order_by('size').reverse(),
            "toilet_congestion": FemaleToilet.objects.filter(toilet_id__station_id__train_line=line).order_by('congestion').reverse()
        }

    elif gender == 3:
        # 多機能トイレのオブジェクトを取得
        return {
            "toilet_value": MultiFunctionalToilet.objects.filter(toilet_id__station_id__train_line=line).order_by('value').reverse(),
            "toilet_size": MultiFunctionalToilet.objects.filter(toilet_id__station_id__train_line=line).order_by('size').reverse(),
            "toilet_congestion": MultiFunctionalToilet.objects.filter(toilet_id__station_id__train_line=line).order_by('congestion').reverse()
        }

    else:
        raise ValueError("不正gender値が設定されました")

def get_latest_comment(request):
    male_comments = Comment.objects.filter(gender=1).order_by("data_create")
    female_comments = Comment.objects.filter(gender=2).order_by("data_create")
    multi_comments = Comment.objects.filter(gender=3).order_by("data_create")
    
    print(multi_comments)
    return render(request, "toilet/toilet_latest_comment.html", context={
        "male_comments": male_comments,
        "female_comments": female_comments,
        "multi_comments": multi_comments
    })