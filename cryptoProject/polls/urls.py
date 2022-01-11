from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('encrypt/', views.encrypt, name='encrypt'),
    path('decrypt/', views.decrypt, name='decrypt'),
    path('logout/', views.logout, name="logout"),
]