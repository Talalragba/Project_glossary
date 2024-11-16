#from django.contrib import admin
from django.urls import path
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
##########
from appwmlg.views import drafts_view
from appwmlg.views import draft_view
from appwmlg.views import approve_draft_view
from appwmlg.views import delete_draft_view
from appwmlg.views import notifications_view
from appwmlg.views import notification_view


urlpatterns = [
    #path('admin/', admin.site.urls),
    path('',login_view, name ='login'),
    path('search/',search_view, name='search'),
    path('logout/', logout_view, name='logout'),
    #####################################
    path('define/', define_view, name='define'),
    #####################################
    path('users/', users_view, name='users'),
    path('addUser/', addUser_view, name='addUser'),
    path('users/<str:UserID>/',user_view, name='user'),
    path('users/<str:UserID>/userUpdate',user_update_view, name='userUpdate'),
    path('users/<str:UserID>/userDelete',user_delete_view, name='userDelete'),
    ######################################
    path('drafts/', drafts_view, name='drafts'),
    path('drafts/<str:DraftID>/', draft_view, name='draft'),
    path('drafts/<str:DraftID>/approveDraft', approve_draft_view, name='approveDraft'),
    path('drafts/<str:DraftID>/deleteDraft', delete_draft_view, name='deleteDraft'),
    ######################################
    path('notifications/', notifications_view, name='notifications'),
    path('notification/', notification_view, name='notification'),

]