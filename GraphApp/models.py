from django.db import models
from django.conf import settings


# Create your models here.

class ForecastModel(models.Model):
    Name = models.CharField(max_length=150, blank=True, null=True)
    Platform = models.CharField(max_length=150, blank=True, null=True)
    Year_of_Release = models.CharField(max_length=150, blank=True, null=True)
    YearOfReleaseDate = models.DateField(null=True)
    Genre = models.CharField(max_length=150, blank=True, null=True)
    Publisher = models.CharField(max_length=150, blank=True, null=True)
    Global_Sale = models.CharField(max_length=150, blank=True, null=True)
    Critic_Score = models.CharField(max_length=150, blank=True, null=True)
    User_Score = models.CharField(max_length=150, blank=True, null=True)
    
    def __str__(self):
        return "{}-{}".format(self.Name, self.Platform, self.Genre )
