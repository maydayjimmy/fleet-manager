from django.shortcuts import render, redirect
from .models import Aircraft, Flight, Item
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required # for functions
from django.contrib.auth.mixins import LoginRequiredMixin # for class based views
from .forms import FlightForm

# Default Pages--------------------------------------------
# 'home' is from urls.py
def home(request):
    return render(request, 'landing.html')

def about(request):
    return render(request, 'about.html')

# AIRCRAFT MODEL--------------------------------------------
# Remember singular/plural aircraft vs aircrafts
@login_required
def aircraft_index(request):
    aircrafts = Aircraft.objects.filter(user=request.user)

    return render(request, 'aircraft/index.html', { 
      'aircrafts': aircrafts
    })

@login_required
def aircraft_detail(request, aircraft_id):
  aircraft = Aircraft.objects.get(id=aircraft_id)

  required_items = Item.objects.exclude(id__in = aircraft.items.all().values_list('id'))

  # instantiate FlightForm to be rendered in the template
  flight_form = FlightForm()

  return render(request, 'aircraft/detail.html', {
    'aircraft': aircraft,
    'flight_form': flight_form,
    'required_items': required_items # required_items is passed into aircraft_detail page

  })

# By convention, the AircraftCreateCBV will look to render a template named templates/main_app/aircraft_form.html.
class AircraftCreate(LoginRequiredMixin, CreateView): # class based view
  model = Aircraft
  fields = ('type', 'n_num', 'engines', 'msn', 'mfr_date')
  success_url = '/aircraft/'

  # This inherited method is called when a
  # valid aircraft form is being submitted
  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user  # form.instance is the aircraft
    # Let the CreateView do its job as usual
    return super().form_valid(form)

class AircraftUpdate(LoginRequiredMixin, UpdateView): # class based view
  model = Aircraft
  fields = ('type', 'n_num', 'engines', 'msn', 'mfr_date')

class AircraftDelete(LoginRequiredMixin, DeleteView): # class based view
  model = Aircraft
  success_url= '/aircraft/'

# Add Flight to Aircraft----------------------------------------------------------------------------------------
@login_required
def add_flight(request, aircraft_id):

  # create the ModelForm using the data in request.POST
  form = FlightForm(request.POST)

  # validate the form
  if form.is_valid():

    # don't save the form to the db until it
    # has the aircraft_id assigned
    new_flight = form.save(commit=False)
    new_flight.aircraft_id = aircraft_id
    new_flight.save()

  return redirect('detail', aircraft_id=aircraft_id)

# Add Maintenance Item to Aircraft----------------------------------------------------------------------------------------
@login_required
def assoc_item(request, aircraft_id, item_id):
  # Note that you can pass a item's id instead of the whole object
  Aircraft.objects.get(id=aircraft_id).items.add(item_id)
  return redirect('detail', aircraft_id=aircraft_id)

# Items Model ---------- (Class-Based Views)

class ItemIndex(LoginRequiredMixin, ListView):
  model = Item

class ItemCreate(LoginRequiredMixin, CreateView):
  model = Item
  fields = '__all__'
  success_url = '/maintenance/'

class ItemDelete(LoginRequiredMixin, DeleteView):
  model = Item
  success_url = '/maintenance/'

class ItemUpdate(LoginRequiredMixin, UpdateView):
  model = Item
  fields= '__all__'
  success_url = '/maintenance/'

class ItemDetail(LoginRequiredMixin, DetailView):
  model = Item

# SIGN UP----------------------------------------------------------------------------------------
def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)