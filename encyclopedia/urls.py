from django.urls import path

from . import views

app_name="encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.page, name="page"),
    path("newpage/", views.newpage, name="newpage"),
    path("editpage/<str:title>",views.editpage,name="editpage"),
    path("random/",views.randompage,name="random"),
    path("search/",views.search, name="search"),
    path("search/wiki/<str:title>",views.page,name="page1"),
    
    
]
