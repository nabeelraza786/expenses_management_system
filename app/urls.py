from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import  path

from app import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('logout',views.logout_user,name="logout"),
    path('base', views.Base, name="base"),
    path('client', views.Client, name="Client"),
    path('add_new_client', views.add_new_client, name="add_new_client"),
    path('All_clients' , views.All_clients, name="all_clients"),
    path('Client_balance', views.Client_balance, name='Client_balance'),
    path('Expenses', views.Expenses, name="expenses"),
    path('Total_page', views.Total_page, name='Total_page'),
    path('All_pages', views.all_page,name="all_pages"),
    path('add_expenses',views.add_exp,name='add_expenses'),
    path('add_funds', views.add_funds,name='funds'),
    path('add_Provider',views.add_Provider,name='add_provider'),
    path('all_providers', views.all_providers,name='all_providers'),
    path('all_funds', views.all_funds,name='all_funds'),
    path('client/<int:client_id>/history',views.client_history, name='client_history'),
    path('Client/<int:client_id>', views.delet_client, name= "delet_client"),
    # path('search-client', views.search_client, name='search_client'),


    
]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
