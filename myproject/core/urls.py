from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('employees/', views.employees_view, name='employees'),
    path('users/', views.users_view, name='users'),
    path('profile/', views.profile_view, name='profile'),
    path('settings/', views.settings_view, name='settings'),
    path('settings/role/', views.role_view, name='role'),
    path('settings/role/add/', views.role_add_view, name='role_add'),
    path('settings/role/edit/<int:role_id>/', views.role_edit_view, name='role_edit'),
    path('settings/role/delete/<int:role_id>/', views.role_delete_view, name='role_delete'),
    path('settings/role-permission/', views.role_permission_view, name='role_permission'),
    path('settings/role-permission/<int:role_id>/', views.role_permission_edit_view, name='role_permission_edit'),
    path('settings/page/', views.page_view, name='page'),
    path('settings/page/add/', views.page_add_view, name='page_add'),
    path('settings/page/edit/<int:page_id>/', views.page_edit_view, name='page_edit'),
    path('settings/page/delete/<int:page_id>/', views.page_delete_view, name='page_delete'),
    path('logout/', views.logout_view, name='logout'),
]
