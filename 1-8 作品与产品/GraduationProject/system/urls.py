from django.urls import path
from . import views
urlpatterns = [
    path('index/', views.index, name='index'),
    path('show/', views.show, name='show'),
    path('get_echart_data/', views.get_echart_data, name='get_echart_data')
]
