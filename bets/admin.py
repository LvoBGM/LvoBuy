from django.contrib import admin

from .models import Bid, Listing, Comments

# Register your models here.
admin.site.register(Bid)
admin.site.register(Listing)
admin.site.register(Comments)