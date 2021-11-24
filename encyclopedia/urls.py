from django.urls import path

from . import views

app_name ='encyclopedia'

urlpatterns = [
    path("", views.index, name="index"),
    path('<str:TITLE>', views.article, name='article'),
    path('search/', views.search, name='search'),
    path('random_page/', views.random_page, name='random_page'),
    path('new_page/', views.new_page, name='new_page'),
    path('edit_page/<str:pagetitle>/', views.edit_page, name='edit_page'),
    path('save_new/', views.save_new, name='save_new'),
    path('save_edit/', views.save_edit, name='save_edit')
]
