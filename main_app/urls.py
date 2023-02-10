from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('aircraft/', views.aircraft_index, name='index'),
    path('aircraft/<int:aircraft_id>/', views.aircraft_detail, name='detail'),
    path('aircraft/create/', views.AircraftCreate.as_view(), name='aircraft_create'),
    # Must use "pk"
    path('aircraft/<int:pk>/update', views.AircraftUpdate.as_view(), name='aircraft_update'),
    path('aircraft/<int:pk>/delete/', views.AircraftDelete.as_view(), name='aircraft_delete'),
    # Flights
    path('aircraft/<int:aircraft_id>/add_flight/', views.add_flight, name='add_flight'),

    # Items
    path('aircraft/<int:aircraft_id>/assoc_item/<int:item_id>/', views.assoc_item, name='assoc_item'),
    path('maintenance/', views.ItemIndex.as_view(), name='item_index'),
    path('maintenance/create/', views.ItemCreate.as_view(), name='item_create'),
    path('maintenance/<int:pk>/update', views.ItemUpdate.as_view(), name='item_update'),
    path('maintenance/<int:pk>/delete/', views.ItemDelete.as_view(), name='item_delete'),
    path('maintenance/<int:pk>/', views.ItemDetail.as_view(), name='item_detail'),

    # Authentication
    path('accounts/signup/', views.signup, name='signup'),
]