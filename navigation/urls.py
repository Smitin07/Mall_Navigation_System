from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('store/<int:id>/', views.store_detail, name='store_detail'),
    path('mall-map/', views.mall_map, name='mall_map'),
    path('navigation/', views.navigation, name='navigation'),
]