from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index<int:index_pk>', views.index, name='index'),
    path('query', views.query, name='query'),
    path('text', views.text, name='text'),
    path('table', views.table, name='table'),
    path('ajax/classify<int:classify_pk>', views.classify, name='ajax/classify'),    
]