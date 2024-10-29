#from django.contrib import admin
from django.urls import path
#from appwmlg.views import index
from appwmlg.views import search_view
from appwmlg.views import index_view
from appwmlg.views import logout_view
##########
from appwmlg.views import add_definition
from appwmlg.views import add_user



urlpatterns = [
    #path('',index, name='index'),
    path('',index_view, name ='login'),
    path('search/',search_view, name='search'),
    #path('admin/', admin.site.urls),
    path('logout/', logout_view, name='logout'),
    ###################################
    path('definition/', add_definition, name='addDefinition'),
    path('addUser/', add_user, name='addUser'),
]


