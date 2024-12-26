from django.urls import path
from . import views

urlpatterns = [

    path('', views.map_view, name='home'),
    path('create_route/', views.create_route, name='create_route'),
    path('generate-route/', views.generate_route, name='generate_route'),
    path('about/', views.about, name='about'),
]