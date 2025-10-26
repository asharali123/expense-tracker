from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('delete/<int:id>/', views.delete, name="delete"),
    path('update/<int:id>/', views.update, name="updata"),
    path('filter/<int:choice>/', views.filter, name="filter"),
]
