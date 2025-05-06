from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'home'


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('api/productss/<slug:slug>/', views.product_api, name='product_api'),
    path('productss/<slug:slug>/',
         views.ProductsDetailView.as_view(), name='product_detail'),
]
