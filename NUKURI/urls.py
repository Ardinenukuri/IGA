"""
URL configuration for NUKURI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import (
    LoginView, LogoutView,PasswordChangeView, PasswordChangeDoneView
)

import authentification.views
from iga.views import (
    PhotoAPIView, BlogAPIView, BlogContributorAPIView,
    FollowUsersView, ViewBlogView, EditBlogView,
    PhotoUploadView, CreateMultiplePhotosView, HomeView, BlogAndPhotoUploadView
)

from rest_framework.routers import DefaultRouter
from iga.views import PhotoViewSet, BlogViewSet, BlogContributorViewSet


router = DefaultRouter()
router.register('photos', PhotoViewSet, basename='photo')
router.register('blogs', BlogViewSet, basename='blog')
router.register('blog-contributors', BlogContributorViewSet, basename='blogcontributor')


urlpatterns = [
    path('admin/', admin.site.urls),
   path('home', LoginView.as_view(
           template_name='authentication/login.html',
           redirect_authenticated_user=True),
        name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', PasswordChangeView.as_view(
        template_name='authentication/password_change_form.html'),
         name='password_change'
         ),
    path('change-password-done/', PasswordChangeDoneView.as_view(
        template_name='authentication/password_change_done.html'),
         name='password_change_done'
         ),
    path('home/', HomeView.as_view(), name='home'),
    path('signup/', authentification.views.signup_page, name='signup'),
    path('photo/upload/', PhotoUploadView.as_view(), name='photo_upload'),
    path('profile-photo/upload/', authentification.views.upload_profile_photo,
         name='upload_profile_photo'),
    path('iga/create', BlogAndPhotoUploadView.as_view(), name='blog_create'),
    path('iga/<int:blog_id>', ViewBlogView.as_view, name='view_blog'),
    path('iga/<int:blog_id>/edit', EditBlogView.as_view(), name='edit_blog'),
    path('photo/upload-multiple/', CreateMultiplePhotosView.as_view(), name='create_multiple_photos'),
    path('follow-users/', FollowUsersView.as_view(), name='follow_users'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('api/photo/', PhotoAPIView.as_view(), name='photo_api'),
    path('api/blog/', BlogAPIView.as_view(), name='blog_api'),
    path('api/blogcontributor/', BlogContributorAPIView.as_view(), name='blog_contributor_api'),
    path('iga/', include('iga.urls')),
    path('leave/', include('leave.urls')),
    path('', authentification.views.index, name='index'),
  
    

   


]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)