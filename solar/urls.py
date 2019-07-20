from django.urls import path
from . import views

app_name = 'solar'
urlpatterns = [
    path('', views.solar_level_view.as_view(), name='levels'),
    path('<int:pk>/delete', views.solar_level_delete.as_view(), name='delete'),
]