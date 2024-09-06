from django.urls import path , include
from .views import vista1 , menu , logout_view , vistaBk , mcdonals 




urlpatterns = [
    path('', vista1,name="vista1"),
    path('menu', menu,name="menu"),
    path('logout/', logout_view, name='logout'),
    path('vistaBk/', vistaBk,name="vistaBk"),
    path('mcdonals/', mcdonals,name="mcdonals")
 ]