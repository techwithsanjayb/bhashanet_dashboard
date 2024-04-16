from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('chart', views.chart, name="chart"),
    path('stackedchart', views.stackedchart, name="stackedchart"),
    path('piechart', views.piechart, name="piechart"),
    path('display_table', views.display_table, name="display_table"),
    path('display_table2', views.display_table2, name="display_table2"),
    path('converturl', views.converturl, name="converturl"),
   
]
