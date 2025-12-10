from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home, name='home'),

path('register/', views.register_student, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

 path('', views.products_list, name='products_list'),
path('products/', views.products_list, name='products_list'),
path('sell/', views.sell_item, name='sell_item'),
   path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/confirm/', views.confirm_order, name='confirm_order'),
]

