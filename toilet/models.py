from django.db import models
from accounts.models import User, Gender

class TrainLine(models.Model):
    """路線マスターテーブル"""

    train_line_name = models.CharField(max_length=255)

    def __str__(self):
        return self.train_line_name

class TrainStation(models.Model):
    """駅マスターテーブル"""

    station_name = models.CharField(max_length=255)
    train_line = models.ForeignKey(TrainLine, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.station_name}({self.train_line})"

class StationTicketGate(models.Model):
    """改札内外マスターテーブル"""

    station_ticket_gate = models.CharField(max_length=5)

    def __str__(self):
        return self.station_ticket_gate

class ToiletMaster(models.Model):
    """トイレマスターテーブル"""

    station_id = models.ForeignKey(TrainStation, on_delete=models.CASCADE)
    place = models.CharField(max_length=30)
    station_ticket_gate_id = models.ForeignKey(StationTicketGate, on_delete=models.SET_NULL, null=True)
    open_time = models.TimeField(auto_now=False)
    close_time = models.TimeField(auto_now=False)
    floor = models.CharField(max_length=5, help_text="設置されている階を数字で入力してください")
    near_gate = models.CharField(max_length=100)
    near_home_num = models.CharField(max_length=3)
    near_train_door_num = models.CharField(max_length=3)
    toilet_root = models.TextField(null=True)

    def __str__(self):
        return f"{self.station_id.station_name}({self.place})"
    
    def get_opening_hours(self):
        """営業時間を 'HH:MM～HH:MM' の形式で取得"""
        return f"{self.open_time.strftime('%H:%M')}～{self.close_time.strftime('%H:%M')}"


class MaleToilet(models.Model):
    """男性用トイレテーブル"""

    toilet_id = models.ForeignKey(ToiletMaster, on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    value = models.FloatField(null=True)
    # 個室
    toilet_stall = models.IntegerField(help_text="個室数を入力してください")
    # 小便器
    urial = models.IntegerField(help_text="小便器数を入力してください")
    # 温水洗浄便座
    warm_water_washing_toilet_seat = models.BooleanField(null=True)
    # おむつ交換設備
    child_facility = models.BooleanField(null=True)
    # バリアフリートイレ
    barrier_free_toilet = models.BooleanField(null=True)
    # 車いす対応
    wheelchair = models.BooleanField(null=True)

    def __str__(self):
        return f"{self.toilet_id.place}({self.toilet_id.station_id.station_name})"
    
    def warm_water_washing_toilet_seat_display(self):
        """温水洗浄便座の〇☓表示"""
        return "〇" if self.warm_water_washing_toilet_seat else "☓"
    
    def child_facility_display(self):
        """おむつ交換設備の〇☓表示"""
        return "〇" if self.child_facility else "☓"
    
    def barrier_free_toilet_display(self):
        """バリアフリートイレの〇☓表示"""
        return "〇" if self.barrier_free_toilet else "☓"
    
    def wheelchair_display(self):
        """車いす対応の〇☓表示"""
        return "〇" if self.wheelchair else "☓"

class FemaleToilet(models.Model):
    """女性用トイレテーブル"""
    
    toilet_id = models.ForeignKey(ToiletMaster, on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    value = models.FloatField(null=True)
    # 個室
    toilet_stall = models.IntegerField(help_text="個室数を入力してください")
    # 温水洗浄便座
    warm_water_washing_toilet_seat = models.BooleanField(null=True)
    # おむつ交換設備
    child_facility = models.BooleanField(null=True)
    # バリアフリートイレ
    barrier_free_toilet = models.BooleanField(null=True)
    # 車いす対応
    wheelchair = models.BooleanField(null=True)
    # パウダールーム
    powder_room = models.BooleanField(null=True)

    def warm_water_washing_toilet_seat_display(self):
        """温水洗浄便座の〇☓表示"""
        return "〇" if self.warm_water_washing_toilet_seat else "☓"
    
    def child_facility_display(self):
        """おむつ交換設備の〇☓表示"""
        return "〇" if self.child_facility else "☓"
    
    def barrier_free_toilet_display(self):
        """バリアフリートイレの〇☓表示"""
        return "〇" if self.barrier_free_toilet else "☓"
    
    def wheelchair_display(self):
        """車いす対応の〇☓表示"""
        return "〇" if self.wheelchair else "☓"
    
    def powder_room_display(self):
        """パウダールームの〇☓表示"""
        return "〇" if self.wheelchair else "☓"
    

class MultiFunctionalToilet(models.Model):
    """多機能トイレテーブル"""
    
    toilet_id = models.ForeignKey(ToiletMaster, on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    value = models.FloatField(null=True)
    # 個室
    toilet_stall = models.IntegerField(help_text="個室数を入力してください")
    # 温水洗浄便座
    warm_water_washing_toilet_seat = models.BooleanField(null=True)
    # おむつ交換設備
    child_facility = models.BooleanField(null=True)
    # バリアフリートイレ
    barrier_free_toilet = models.BooleanField(null=True)
    # 車いす対応
    wheelchair = models.BooleanField(null=True)

    def warm_water_washing_toilet_seat_display(self):
        """温水洗浄便座の〇☓表示"""
        return "〇" if self.warm_water_washing_toilet_seat else "☓"
    
    def child_facility_display(self):
        """おむつ交換設備の〇☓表示"""
        return "〇" if self.child_facility else "☓"
    
    def barrier_free_toilet_display(self):
        """バリアフリートイレの〇☓表示"""
        return "〇" if self.barrier_free_toilet else "☓"
    
    def wheelchair_display(self):
        """車いす対応の〇☓表示"""
        return "〇" if self.wheelchair else "☓"

class Comment(models.Model):
    """コメントテーブル"""

    # accountsアプリのUserモデルを外部キーに設定
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=300)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    value = models.IntegerField(help_text="5段階で数値を入力してください")
    toilet = models.ForeignKey(ToiletMaster, on_delete=models.CASCADE)



