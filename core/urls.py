from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('python/', views.python_page, name='python'),
    path('odoo/', views.odoo_page, name='odoo'),
    path('about/', views.about, name='about'),
    path('privacy-policy/', views.privacy_policy, name='privacy'),
    path('terms/', views.terms, name='terms'),
]