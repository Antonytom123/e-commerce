from django.urls import path,include
from .import views
urlpatterns = [
    path('',views.home,name='home'),
    path('signup',views.signup,name='signup'),
    path('signin',views.signin,name='signin'),
    path('signinurl',views.signinurl,name='signinurl'),
    path('signupurl',views.signupurl,name='signupurl'),
    path('show_user',views.show_user,name='show_user'),
    path('admin_home',views.admin_home,name='admin_home'),
    path('category',views.category,name='category'),
    path('product',views.product,name='product'),
    path('categoryurl',views.categoryurl,name='categoryurl'),
    path('producturl',views.producturl,name='producturl'),
    path('show_product',views.show_product,name='show_product'),
    path('deleteproduct<int:pk>',views.deleteproduct,name='deleteproduct'),
    path('deleteuser<int:pk>',views.deleteuser,name='deleteuser'),
    path('user_home',views.user_home,name='user_home'),
    path('categorized_products/<int:pk>/', views.categorized_products, name='categorized_products'),
    path('cart',views.cart,name='cart'),
    path('cart_details/<int:pk>',views.cart_details,name='cart_details'),
    path('removecart/<int:pk>',views.removecart,name='removecart'),


    path('logout',views.logout,name='logout'),

]