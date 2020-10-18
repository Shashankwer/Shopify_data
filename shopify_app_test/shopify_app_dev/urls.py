from . import views
from django.urls import path

urlpatterns = [
    path('app_launched/',views.app_launched,name='app_launched'),
    path('app_installed/',views.app_installed),
    path('app_installed/gather_data/',views.gather_data),
   

]