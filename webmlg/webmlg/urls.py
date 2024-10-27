#from django.contrib import admin
from django.urls import path
#from appwmlg.views import index
from appwmlg.views import search_view
from appwmlg.views import index_view



urlpatterns = [
    #path('',index, name='index'),
    path('',index_view, name ='login'),
    path('search/',search_view, name='search'),
    #path('admin/', admin.site.urls),
]


