from django.contrib import admin
from .models import TrainLine, TrainStation

# @admin.register(TrainLine)
class TrainLineAdmin(admin.ModelAdmin):
    list_display = ("id", "train_line_name")
    search_fields = ("train_line_name",)

# @admin.register(TrainStation)
class TrainStationAdmin(admin.ModelAdmin):
    list_display = ("id", "station_name", "train_line") # 外部キーも表示する
    search_fields = ("station_name",)
    list_filter = ("train_line",) # 路線でフィルタリングする

admin.site.register(TrainLine, TrainLineAdmin)
admin.site.register(TrainStation, TrainStationAdmin)