from rest_framework import serializers
from iga.models import Photo, Blog, BlogContributor

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['title', 'image', 'description', 'date_created', 'date_updated']


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'author', 'date_created', 'date_updated']

class BlogContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogContributor
        fields = ['name', 'bio', 'email', 'website']
