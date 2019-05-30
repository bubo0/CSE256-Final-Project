from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('query', views.query, name='query'),
    path('text', views.lime, name='text'),
    path('table', views.lime, name='table'),
    path('ajax/classify', views.classify, name='ajax/classify'),
]