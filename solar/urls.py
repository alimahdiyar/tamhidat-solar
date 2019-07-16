from django.urls import path
from . import views

app_name = 'solar'
urlpatterns = [
    path('levels/', views.solar_level_view.as_view(), name='levels'),
]