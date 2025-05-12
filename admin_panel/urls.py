
from django.urls import path
from admin_panel import views


urlpatterns = [
    path('admin_login',views.admin_login,name = 'admin_login'),
    path('admin_page', views.admin_page, name='admin_page'),
    path('add/',views.add,name='add'),
    path('edit',views.edit,name= 'edit'),
    path('update/<str:id>',views.update, name = 'update'),
    path('logoutt', views.logoutt, name='logoutt'),
    path('search',views.search,name = 'search'),
    path('delete/<str:id>',views.delete, name = 'delete')
]