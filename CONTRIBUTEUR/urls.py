from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name="indexs"),
    path('details/<str:id>', details, name="details"),
    path('changement/<str:id>', changement, name="changement"),
    path('envoyer', envoyer, name="envoyer"),
    path('contribuer', contribuer, name="contribuer")
  
    
]