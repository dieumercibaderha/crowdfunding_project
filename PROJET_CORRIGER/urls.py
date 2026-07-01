"""
URL configuration for PROJET_CORRIGER project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from CROWDFUNDING.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('contributions_app/', include("CONTRIBUTEUR.urls"), name="CONTRIBUTEUR_APP"),
    path('', index, name="index"),
    path('list_projets', list_projet, name="list_projets"),
    path('voir_projets/<str:id>', voir_projet, name="voir_projet"),
    path('add_project', add_projet, name="add_projet"),
    path('project_grid', projet_grid, name="project_grid"),
    path('mod_projet/<str:id>', mod_projet, name="mod_projet"),
    path('sup_projet/<str:id>', sup_projet, name="sup_projet"),
    
    path('list_type', list_type, name="list_type"),
    path('voir_type', voir_type, name="voir_type"),
    path('add_type', add_type, name="add_type"),
   
    path('mod_type/<str:id>', mod_type, name="mod_type"),
    
    path('sup_type/<str:id>', sup_type, name="sup_type"),
    
    path('list_utili', list_utili, name="list_utili"),
    path('voir_utili', voir_utili, name="voir_utili"),
    path('add_utili', add_utili, name="add_utili"),
    path('utili_grid', utili_grid, name="utili_grid"),
    path('mod_utili', mod_utili, name="mod_utili"),

    path('list_type_con', type_contributions, name="list_type_con"),
    path('add_type_con', add_type_contributions, name="add_type_con"),
    path('mod_type_contribution/<str:id>', mod_type_contribution, name="mod_type_con"),
    path('sup_type_contribution/<str:id>', sup_type_contribution, name="sup_type_con"),
    
    
    path('profile', profile, name="profile"),
    path('accounts/login/', logine, name="login"),
    path('registe', registe, name="registe"),
    path('oublie', oublie, name="oublie"),
    path('contributions', contributions, name="contributions"),
    path('deconnexion', deconnexion, name="deconnexion" ),
    
    path('add_c', add_contributions, name="add_contributions"),
    path('edit_contributions', edit_contributions, name="edit_contributions"),
    path('user_details/<str:id>', user_details, name="user_details"),
    path('activate/<uidb64>/<token>/', activate,name="activate"),
    path('erreur', erreur, name="erreur"),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment_cancel', payment_cancel, name="payment_cancel"),
    path('payment_success', payment_success, name="payment_success")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)
