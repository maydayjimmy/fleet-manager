from django.db import models
from django.urls import reverse
from datetime import date
# from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User

#  Many aircraft to Many items
class Item(models.Model):
    name = models.CharField(max_length=100) # name of maintenance item
    completed = models.DateField() # date completed
    interval = models.IntegerField() # maximum time between completions

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse("detail", kwargs={'pk': self.id})

#     def create_page(self):
#         "Adds a page to the book"
#         #Do what you need to do
#         page = Page(name="TitlePage", Book=self)
#         page.save()

# class Complete(models.Model):
#     date = models.DateField()

#     Item= models.ForeignKey("Item", on_delete=models.CASCADE)

class Aircraft(models.Model):
    type = models.CharField(max_length=100)
    n_num = models.CharField(max_length=6)
    msn = models.CharField(max_length=5)
    engines = models.IntegerField()
    mfr_date = models.DateField()
    # Many to many relationship:
    items = models.ManyToManyField(Item)

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

# One aircraft to Many flights
class Flight(models.Model):
    date = models.DateField()
    dep = models.CharField(max_length=4)
    dest = models.CharField(max_length=4)
    distance = models.IntegerField()
    fuel_used = models.IntegerField()
    fuel_rem = models.IntegerField()
    
    # Many flights to one aircraft
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.dep} to {self.dest}"

    # Sorts display from most recent to least recent
    class Meta:
        ordering = ('-date',)