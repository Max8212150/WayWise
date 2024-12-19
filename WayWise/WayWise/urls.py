from django.contrib import admin
from django.urls import path

from maps import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.map_view, name='map_view'),
    path('search/', views.search_places, name='search_places'),
]
