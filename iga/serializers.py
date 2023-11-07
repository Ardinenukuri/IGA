from rest_framework import serializers
from iga.models import Photo, Blog, BlogContributor

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'

class BlogContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogContributor
        fields = '__all__'
