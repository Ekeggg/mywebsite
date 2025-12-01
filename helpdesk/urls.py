from django.urls import path
from . import views
urlpatterns = [
    path('', views.request_list, name='request_list'),
    path('request/<int:request_id>/', views.request_detail, name='request_detail'),
    path('request/new/', views.create_request, name='create_request'),
    path('request/<int:request_id>/reply/', views.reply_request, name='reply_request'),
    path('signup/', views.signup, name='signup'),
    path('accounts/editprofile/', views.editprofile, name='editprofile'),
    path("notifications/", views.notifications, name="notifications"),
]