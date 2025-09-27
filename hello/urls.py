from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user/', views.user_page, name='user_page'),
    path('handyman/', views.handyman_page, name='handyman_page'),
    path('client/signup/', views.client_signup_view, name='client_signup'),
    path('handyman/signup/', views.handyman_signup_view, name='handyman_signup'),
    path('signup/', views.role_selection_view, name='signup_role'),
    path('book/<int:service_id>/', views.book_service_view, name='book_service_with_id'),
    path('book/', views.book_service_view, name='book_service'),
]

