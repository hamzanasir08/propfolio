"""
URL configuration for signup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.property_list, name='dashboard_view'),
    path('home',views.homeview, name='homeview'),
    path('aboutview',views.aboutview, name='aboutview'),
    path('contactview',views.contactview, name='contactview'),
    path('search',views.search, name='search'),
    path('dashboard/', views.dashboard_view, name='dashboard_view'),
    path('addprop', views.submit_property, name='submit_property'),
    path('get-towns/', views.get_towns, name='get_towns'),
    path('property_list/', views.property_list, name='property_list'),
    path('list_all_properties/', views.list_all_properties, name='list_all_properties'),
    path('property/<int:property_id>/', views.property_detail, name='property_detail'),
    path('user_properties/', views.user_properties, name='user_properties'),
    path('<int:prop_id>/delete/', views.prop_delete, name= 'prop_delete'),
    path('property/edit/<int:prop_id>/', views.edit_property, name='edit_property'),
    path('book-appointment/<int:property_id>/', views.book_appointment, name='book_appointment'),
    path('view_appointments/', views.view_appointments, name='view_appointments'),
    path('appointment-success/', views.appointment_success, name='appointment_success'),
    # path('cancel_appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('logout/', views.logout_view, name='logout'),
]