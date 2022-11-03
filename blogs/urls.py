from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('create-post', views.post_create, name='post_create'),
    path('<slug:slug>/', views.post_detail,  name='post_detail'),
]