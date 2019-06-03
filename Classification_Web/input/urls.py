from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'.*.html$', views.index, name='index'),
    path('index<int:index_pk>', views.index, name='index'),    
    path('text', views.lime, name='text'),
    path('table', views.lime, name='table'),
    path('shap', views.lime, name='shap'),
    path('ajax/classify<int:classify_pk>', views.classify, name='ajax/classify'),    
]