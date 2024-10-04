from django.contrib import admin
from django.urls import path
from appwmlg.views import index
from appwmlg.views import search
from appwmlg.views import login_view



urlpatterns = [
    # path('',index, name='index'),
    path('',login_view, name ='login'),
    path('search/',search, name='search'),
    path('admin/', admin.site.urls),
]


