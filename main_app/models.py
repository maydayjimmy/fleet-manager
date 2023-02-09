from django.db import models
from django.urls import reverse
from datetime import date
# from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User

class Aircraft(models.Model):
    type = models.CharField(max_length=100)
    n_num = models.CharField(max_length=6)
    msn = models.CharField(max_length=5)
    engines = models.IntegerField()
    mfr_date = models.DateField()

    # Age is difference between today's date and mfr_date, in years
    # age = models.IntegerField(
    #     default = relativedelta(date.today(), mfr_date).years
    # )

    # # Authorization/Authentication
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.type

    def get_absolute_url(self):
        return reverse("detail", kwargs={'aircraft_id': self.id})