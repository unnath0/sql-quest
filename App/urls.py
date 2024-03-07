from django.urls import path
from django.urls import re_path
from . import views

urlpatterns = [
  path('',views.home, name='home'),
  path('login/',views.login, name='login'),
  path('signup/',views.signup, name='signup'),
  path('logout/',views.logout, name='logout'),
  path('modules/',views.modules, name='modules'),
  path('question/',views.question, name='question'),
  re_path(r'^question/?$', views.question, name='question'),
  path('about/',views.about, name='about'),
  path('help/',views.help, name='help'),
  path('pricing/',views.pricing, name='pricing')
]
