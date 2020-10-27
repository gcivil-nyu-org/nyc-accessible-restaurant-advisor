from django.contrib import admin
from .models import User, User_Profile, Restaurant_Profile, Restaurant
from import_export.admin import ImportExportModelAdmin
# Register your models here.


admin.site.register(User)
admin.site.register(User_Profile)
admin.site.register(Restaurant_Profile)
# admin.site.register(Restaurant)

@admin.register(Restaurant)
class ViewAdmin (ImportExportModelAdmin):
    pass