from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('logoff', views.logoff, name='logoff'),
    path('planes',views.planes,name='planes'),
    path('signup',views.signup,name='signup'),
    path('profile',views.profile,name='profile'),
    path('register/<str:city_name>/',views.register,name='register'),
    path('search_page',views.search_page,name='search_page'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('services',views.services,name='services'),
    path('insert_user',views.insert_user,name='insert_user'),
    path('edit_profile',views.edit_profile,name='edit_profile'),
    path('delete_profile',views.delete_profile,name='delete_profile'),
    path('deleted_profile',views.deleted_profile,name='deleted_profile'),
    path('insert_vacancy',views.insert_vacancy,name='insert_vacancy'),
    path('custom_search',views.custom_search,name='custom_search'),
    path('list_search',views.list_search,name='list_search'),
    # begin test views #
    path('insert_random_users/<int:quantity>/',views.insert_random_users,name='insert_random_users'),
    path('delete_all_users',views.delete_all_users,name='delete_all_users'),
    # end test views #
]