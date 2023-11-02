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
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView



import authentification.views
import iga.views


urlpatterns = [
    path('admin/', admin.site.urls),
   path('', LoginView.as_view(
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
    path('home/', iga.views.home, name='home'),
    path('signup/', authentification.views.signup_page, name='signup'),
    path('photo/upload/', iga.views.photo_upload, name='photo_upload'),
    path('profile-photo/upload', authentification.views.upload_profile_photo,
         name='upload_profile_photo'),
    path('iga/create', iga.views.blog_and_photo_upload, name='blog_create'),
    path('iga/<int:blog_id>', iga.views.view_blog, name='view_blog'),
    path('iga/2/edit', iga.views.edit_blog, name='edit_blog'),
    path('photo/upload-multiple/', iga.views.create_multiple_photos,
    name='create_multiple_photos'),

]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)