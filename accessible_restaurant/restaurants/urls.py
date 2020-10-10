from django.urls import path

from . import views

app_name = 'restaurants'
urlpatterns = [
    # ex: /register/
    path('register/', views.index, name='index'),
]