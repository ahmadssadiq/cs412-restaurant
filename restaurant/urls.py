from django.urls import path
from . import views

urlpatterns = [
    path('main/', views.main, name='main'),  # Main page route
    path('order/', views.order, name='order'),  # Order page route
    path('confirmation/', views.confirmation, name='confirmation'),  # Confirmation route
    path('', views.main, name='home'),  # Root URL pointing to the main view
]
