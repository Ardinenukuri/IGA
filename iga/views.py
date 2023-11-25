from itertools import chain


from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.forms import formset_factory
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .models import Blog




from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from iga.models import Photo, Blog, BlogContributor
from iga.serializers import PhotoSerializer, BlogSerializer, BlogContributorSerializer
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from iga.forms import PhotoForm, BlogForm, DeleteBlogForm, FollowUsersForm, DeletePhotoForm




from . import forms, models


class PhotoAPIView(APIView):
    def get(self, *args, **kwargs):
        photos = Photo.objects.all()
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data)


class BlogAPIView(APIView):
    def get(self, *args, **kwargs):
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)


class BlogContributorAPIView(APIView):
    def get(self, *args, **kwargs):
        contributors = BlogContributor.objects.all()
        serializer = BlogContributorSerializer(contributors, many=True)
        return Response(serializer.data)
   


class PhotoViewSet(ReadOnlyModelViewSet):
   
    serializer_class = PhotoSerializer


    def get_queryset(self):
        return models.Photo.objects.filter(active=True)


class BlogViewSet(ReadOnlyModelViewSet):
   
    serializer_class = BlogSerializer


    def get_queryset(self):
        queryset = Blog.objects.filter(active=True)
        photo_id = self.request.GET.get('photo_id')
        if photo_id is not None:
            queryset = queryset. filter(photo_id=photo_id)
            return queryset


class BlogContributorViewSet(ReadOnlyModelViewSet):
   
    serializer_class = BlogContributorSerializer


    def get_queryset(self):
        return BlogContributor.objects.filter(active=True)








class PhotoUploadView(LoginRequiredMixin, View):
    template_name = 'iga/photo_upload.html'


    def get(self, request, *args, **kwargs):
        form = PhotoForm()
        return render(request, self.template_name, context={'form': form})


    def post(self, request, *args, **kwargs):
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            return redirect('home')
        return render(request, self.template_name, context={'form': form})
   
class HomeView(LoginRequiredMixin, View):
    template_name = 'iga/home.html'
    paginate_by = 6
    context_object_name = 'blog_posts'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'iga/index.html')  # Redirect or handle unauthenticated users as needed


        blogs = Blog.objects.filter(
           Q(contributors__in=[request.user]) | Q(contributors__in=request.user.follows.all()) | Q(starred=True))
        photos = Photo.objects.filter(
            uploader__in=[request.user]).exclude(
            blog__in=blogs,
            )

        

        

        blogs_and_photos = sorted(
            chain(blogs, photos),
            key=lambda instance: instance.date_created,
            reverse=True
        )
        paginator = Paginator(blogs_and_photos, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj, 'blogs': blogs}
        print("Blogs and Photos:", blogs_and_photos)


        return render(request, self.template_name, context=context)




   
class BlogAndPhotoUploadView(LoginRequiredMixin, View):
    template_name = 'iga/create_blog_post.html'


    def get(self, request, *args, **kwargs):
        blog_form = BlogForm()
        photo_form = PhotoForm()
        context = {
            'blog_form': blog_form,
            'photo_form': photo_form,
        }
        return render(request, self.template_name, context=context)


    def post(self, request, *args, **kwargs):
        blog_form = BlogForm(request.POST)
        photo_form = PhotoForm(request.POST, request.FILES)
        if all([blog_form.is_valid(), photo_form.is_valid()]):
            photo = photo_form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            blog = blog_form.save(commit=False)
            blog.photo = photo
            blog.save()
            blog.contributors.add(request.user, through_defaults={'contribution': 'Primary Author'})
            return redirect('home')
        else:
            context = {
                'blog_form': blog_form,
                'photo_form': photo_form,
            }
            return render(request, self.template_name, context=context)







class ViewBlogView(LoginRequiredMixin, View):
    template_name = 'iga/view_blog.html'


    def get(self, request, blog_id, *args, **kwargs):
        blog = get_object_or_404(Blog, id=blog_id)
        return render(request, self.template_name, {'blog': blog})




class EditBlogView(LoginRequiredMixin, View):
    template_name = 'iga/edit_blog.html'


    def get(self, request, blog_id, *args, **kwargs):
        blog = get_object_or_404(Blog, id=blog_id)
        edit_form = BlogForm(instance=blog)
        delete_form = DeleteBlogForm()
        context = {
            'edit_form': edit_form,
            'delete_form': delete_form,
        }
        return render(request, self.template_name, context=context)


    def post(self, request, blog_id, *args, **kwargs):
        blog = get_object_or_404(Blog, id=blog_id)
        edit_form = BlogForm(request.POST, instance=blog)
        delete_form = DeleteBlogForm(request.POST)
        if 'edit_blog' in request.POST:
            if edit_form.is_valid():
                edit_form.save()
                return redirect('home')
        elif 'delete_blog' in request.POST:
            if delete_form.is_valid():
                blog.delete()
                return redirect('home')


        context = {
            'edit_form': edit_form,
            'delete_form': delete_form,
        }
        return render(request, self.template_name, context=context)

class EditPhotoView(LoginRequiredMixin, View):
    template_name = 'iga/edit_photo.html'

    def get(self, request, photo_id, *args, **kwargs):
        photo = get_object_or_404(Photo, id=photo_id)
        edit_form = PhotoForm(instance=photo)
        delete_form = DeletePhotoForm()

        context = {
            'photo': photo,
            'edit_form': edit_form,
            'delete_form': delete_form,
        }

        return render(request, self.template_name, context=context)

    def post(self, request, photo_id, *args, **kwargs):
        photo = get_object_or_404(Photo, id=photo_id)
        edit_form = PhotoForm(request.POST, instance=photo)
        delete_form = DeletePhotoForm(request.POST)

        if 'edit_photo' in request.POST:
            if edit_form.is_valid():
                edit_form.save()
                return redirect('home')
        elif 'delete_photo' in request.POST:
            if delete_form.is_valid():
                photo.delete()
                return redirect('home')

        context = {
            'photo': photo,
            'edit_form': edit_form,
            'delete_form': delete_form,
        }

        return render(request, self.template_name, context=context)
    

class CreateMultiplePhotosView(LoginRequiredMixin, View):
    template_name = 'iga/create_multiple_photos.html'
    formset_class = formset_factory(PhotoForm, extra=5)


    def get(self, request, *args, **kwargs):
        formset = self.formset_class()
        context = {'formset': formset}
        return render(request, self.template_name, context=context)


    def post(self, request, *args, **kwargs):
        formset = self.formset_class(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    photo = form.save(commit=False)
                    photo.uploader = request.user
                    photo.save()
            return redirect('home')
        context = {'formset': formset}
        return render(request, self.template_name, context=context)
   
class FollowUsersView(LoginRequiredMixin, View):
    template_name = 'iga/follow_users_form.html'


    def get(self, request, *args, **kwargs):
        form = FollowUsersForm(instance=request.user)
        context = {'form': form}
        return render(request, self.template_name, context=context)


    def post(self, request, *args, **kwargs):
        form = FollowUsersForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
        context = {'form': form}
        return render(request, self.template_name, context=context)
   
def photo_feed(request):
    photos = models.Photo.objects.filter(
        uploader__in=request.user.follows.all()).order_by('-date_created')
    paginator = Paginator(photos, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'iga/photo_feed.html', context=context)


def index(request):
    blogs= Blog.objects.all()
    context= {
        'blogs':blogs
    }
    return render(request, 'iga/index.html', context)


def about_us(request):
    return render(request, 'iga/about-us.html')


def contact_us(request):
    return render(request, 'iga/contact_us.html')


def privacy_and_policy(request):
    return render(request, 'iga/privacy_and_policy.html')
    




   



