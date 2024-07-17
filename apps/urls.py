
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from apps.forms import RegisterForm
from apps.views import kim, ProductListView, smth, RegisterFormView, smth2, kimsan, CategoryListView, \
    WListView, LikeView, LikeDeleteView, CustomLoginView, OrderDetailView, MyOrdersView, MyOrderDelete, ProfileFormView

urlpatterns = [
    # path('', ProductListView.as_view()),
    path('', CategoryListView.as_view(),name='home'),
    # path('wishlist', WishListView.as_view(),name='wishlist'),
    path('register/', RegisterFormView.as_view(),name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('prod/<str:slug>', smth, name='product'),
    path('pro/<str:slug>', smth2, name='products'),
    path('order/<str:slug>', OrderDetailView.as_view(), name='orders'),
    # path('order-list', OrFormView.as_view(), name='orders-list'),
    path('complete-order/', kimsan, name='complete-order'),
    path('my-orders/', MyOrdersView.as_view(), name='my-orders'),
    path('my-orders/<int:pk>', MyOrderDelete.as_view(), name='delete-order'),
]

urlpatterns += [
    path('wishlist/',WListView.as_view(),name='wishlist'),
    path('product/like/<str:slug>',LikeView.as_view(),name='like'),
    path('delete-like/<int:pk>',LikeDeleteView.as_view(),name='delete-like'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('profile/',ProfileFormView.as_view(),name='profile'),
]