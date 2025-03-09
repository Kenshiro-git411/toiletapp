from django.db import models

class TrainLine(models.Model):
    """路線テーブル"""
    
    train_line_name = models.CharField(max_length=255)

    def __str__(self):
        return self.train_line_name

class TrainStation(models.Model):
    """駅テーブル"""

    station_name = models.CharField(max_length=255)
    train_line = models.ForeignKey(TrainLine, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.station_name}({self.train_line})"




