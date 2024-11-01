#from django.contrib import admin
from django.urls import path
#from appwmlg.views import index
from appwmlg.views import search_view
from appwmlg.views import login_view
from appwmlg.views import logout_view
##########
from appwmlg.views import define_view
from appwmlg.views import addUser_view



urlpatterns = [
    #path('',index, name='index'),
    path('',login_view, name ='login'),
    path('search/',search_view, name='search'),
    #path('admin/', admin.site.urls),
    path('logout/', logout_view, name='logout'),
    ###################################
    path('define/', define_view, name='define'),
    path('addUser/', addUser_view, name='addUser'),
]


