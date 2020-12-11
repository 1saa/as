from django.contrib import admin

# Register your models here.
from .models import User, Papers, Discussion, Dis_center

admin.site.register(User)
admin.site.register(Papers)
admin.site.register(Discussion)
admin.site.register(Dis_center)