from django.contrib import admin
from .models import (
    User,
    User_Profile,
    User_Preferences,
    Restaurant_Profile,
    Restaurant,
    Review,
    Comment,
    ApprovalPendingUsers,
    ApprovalPendingRestaurants,
    FAQ,
    Favorites,
    # Images,
)
from import_export.admin import ImportExportModelAdmin

# Register your models here.
admin.site.register(User)
admin.site.register(User_Profile)
admin.site.register(User_Preferences)
admin.site.register(Restaurant_Profile)
admin.site.register(Review)
# admin.site.register(Restaurant)
admin.site.register(ApprovalPendingUsers)
admin.site.register(ApprovalPendingRestaurants)
admin.site.register(Favorites)
# admin.site.register(Images)


@admin.register(Restaurant)
class ViewAdmin(ImportExportModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "review", "time", "text")
    search_fields = ("user", "review", "text")


@admin.register(FAQ)
class ViewAdmin(ImportExportModelAdmin):
    pass
