from django.contrib import admin
from .models import ForecastModel
# Register your models here.
@admin.register(ForecastModel)
class UserAdmin(admin.ModelAdmin):
    search_fields = ('Name', 'Platform', 'Year_of_Release', 'Genre')
    list_display = ('Name','Platform','Year_of_Release','YearOfReleaseDate','Genre','Publisher','Global_Sale','Critic_Score','User_Score')