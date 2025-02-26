from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('signin',views.signin,name='signin'),
    path('signup',views.signup,name='signup'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('item',views.item,name='item'),
    path('new_item',views.new_item,name='new_item'),
    path('signout',views.signout,name='signout'),
    path('item/<int:item_id>/', views.item_detail, name='item'),
    path('item/<int:item_id>/edit/', views.edit_item, name='edit_item'),
    path('item_list/', views.item_list, name='item_list'),
    path('bid/<int:item_id>/', views.bid_item, name='bid_item'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('policy',views.policy,name='policy'),
    path('search/', views.search_results, name='search_results'),
]