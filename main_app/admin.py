from django.contrib import admin
from .models import Aircraft, Item, Flight


# Register your models here.
admin.site.register(Aircraft)
admin.site.register(Item)
admin.site.register(Flight)