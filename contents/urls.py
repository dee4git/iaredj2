from django.urls import path

from . import views

urlpatterns = [
    path('control-center/<str:key>', views.control_center, name='control-center'),
    path('create/<str:key>', views.create, name='create'),
    path('update/<str:key>/<int:pk>', views.update, name='update'),
    path('hide/<str:key>/<int:pk>', views.hide, name='hide'),
    path('destroy/<str:key>/<int:pk>', views.destroy, name='destroy'),
    path('set-profile', views.set_profile, name='set-profile'),
    path('view-profile/<int:s_id>', views.view_profile, name='view-profile'),
    path('update-profile/<int:pk>', views.update_profile, name='update-profile'),

]
