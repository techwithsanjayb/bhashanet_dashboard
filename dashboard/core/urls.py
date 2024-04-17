from django.contrib import admin
from django.urls import path
from . import views
app_name = 'core'
urlpatterns = [
    path('', views.home, name="home"),   
    path('display_table2', views.display_table2, name="display_table2"),
    path('update_json', views.update_json, name="update_json"),
    path('urladd', views.urladd, name="urladd"), 
    path('check', views.check, name="check"),

    
     
]
