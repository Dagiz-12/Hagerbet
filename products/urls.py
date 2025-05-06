from django.urls import path
from . import views
from django.views.generic import TemplateView


app_name = 'products'
urlpatterns = [
    path('', views.MainView.as_view(), name='all'),
    path('products/<int:pk>/detail/', views.ProductsDetailView.as_view(),
         name='products_detail'),
    path('main/create/', views.AutoCreate.as_view(), name='products_create'),
    path('main/<int:pk>/update/', views.AutoUpdate.as_view(), name='products_update'),
    path('main/<int:pk>/delete/', views.AutoDelete.as_view(), name='products_delete'),
    path('lookup/', views.MakeView.as_view(), name='catagories_list'),
    path('lookup/create/', views.MakeCreate.as_view(), name='catagories_create'),
    path('lookup/<int:pk>/update/',
         views.MakeUpdate.as_view(), name='catagories_update'),
    path('lookup/<int:pk>/delete/',
         views.MakeDelete.as_view(), name='catagories_delete'),

]
