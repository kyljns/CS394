from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home),
    path('login/', auth_views.LoginView.as_view(), name='login'), 
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), 
    path('add-member/', views.add_family_member, name='add_member'),
    path('member/<int:pk>/', views.family_member_profile, name='member_profile'), 
    path('family-tree/', views.family_tree, name='family_tree'),
    path('profile/<int:pk>/', views.family_member_profile, name='member_profile')



]
