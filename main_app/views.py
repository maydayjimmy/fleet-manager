from django.shortcuts import render, redirect
from .models import Aircraft
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required # for functions
from django.contrib.auth.mixins import LoginRequiredMixin # for class based views

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
    return render(request, 'aircraft/index.html', { 'aircrafts': aircrafts })

@login_required
def aircraft_detail(request, aircraft_id):
  aircraft = Aircraft.objects.get(id=aircraft_id)

  return render(request, 'aircraft/detail.html', {
    'aircraft': aircraft,
  })

# By convention, the AircraftCreateCBV will look to render a template named templates/main_app/aircraft_form.html.
class AircraftCreate(LoginRequiredMixin, CreateView): # class based view
  model = Aircraft
  fields = ('type', 'n_num', 'engines', 'msn', 'mfr_date')
  success_url = '/aircraft/'

  # This inherited method is called when a
  # valid cat form is being submitted
  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user  # form.instance is the aircraft
    # Let the CreateView do its job as usual
    return super().form_valid(form)

class AircraftUpdate(LoginRequiredMixin, UpdateView): # class based view
  model = Aircraft
  fields = '__all__'

class AircraftDelete(LoginRequiredMixin, DeleteView): # class based view
  model = Aircraft
  success_url= '/aircraft/'

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