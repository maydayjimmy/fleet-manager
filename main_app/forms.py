from django.forms import ModelForm
from .models import Flight

class FlightForm(ModelForm):
  class Meta:
    model = Flight
    fields = ['date','dep', 'dest','distance','fuel_used','fuel_rem']
    labels = {
      "fuel_used": "Fuel Used",
      "fuel_rem": "Fuel Remaining",
    }

