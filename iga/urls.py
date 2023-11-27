from django.urls import path
from . import views
from .views import EditPhotoView

urlpatterns = [
    path('index/', views.index, name='index'),
    path('about-us/', views.about_us, name='about_us'),
    path('contact_us/', views.contact_us, name='contact_us'),
     path('privacy_and_policy/', views.privacy_and_policy, name='privacy_and_policy'),
     path('edit/<int:photo_id>', EditPhotoView.as_view(), name='edit_photo'),
     
]
