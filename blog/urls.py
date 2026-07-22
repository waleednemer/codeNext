from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('articles/', views.article_list, name='article_list'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('category/<slug:slug>/', views.category_detail, name='category'),
]