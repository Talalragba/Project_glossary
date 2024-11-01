#from django.contrib import admin
from django.urls import path
#from appwmlg.views import index
from appwmlg.views import search_view
from appwmlg.views import login_view
from appwmlg.views import logout_view
##########
from appwmlg.views import define_view
from appwmlg.views import addUser_view
from appwmlg.views import users_view
from appwmlg.views import user_view
from appwmlg.views import user_update_view
from appwmlg.views import user_delete_view

urlpatterns = [
    #path('',index, name='index'),
    path('',login_view, name ='login'),
    path('search/',search_view, name='search'),
    #path('admin/', admin.site.urls),
    path('logout/', logout_view, name='logout'),
    ###################################
    path('define/', define_view, name='define'),
    ###################################
    path('users/', users_view, name='users'),
    path('addUser/', addUser_view, name='addUser'),
    path('users/<str:username>/',user_view, name='user'),
    path('users/<str:username>/userUpdate',user_update_view, name='userUpdate'),
    path('users/<str:username>/userDelete',user_delete_view, name='userDelete'),
]


