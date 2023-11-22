from django.conf import settings
from django.db import models
from PIL import Image
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class Post(models.Model):
    title= models.CharField(max_length=200)
    content= models.CharField()
    pub_date = models.DateTimeField('date published')

class Photo(models.Model):
    IMAGE_MAX_SIZE = (800, 800)

    image = models.ImageField()
    caption = models.CharField(max_length=128, blank=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    

    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        # save the resized image to the file system
        # this is not the model save method!
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()

class Blog(models.Model):
    photo = models.ForeignKey(Photo, null=True, on_delete=models.SET_NULL, blank=True)
    title = models.CharField(max_length=128)
    content = models.CharField(max_length=5000)
    date_created = models.DateTimeField(auto_now_add=True)
    starred = models.BooleanField(default=False)
    title = models.CharField(max_length=255)
    content = models.TextField()
    word_count = models.IntegerField(null=True)
    contributors = models.ManyToManyField(settings.AUTH_USER_MODEL, through='BlogContributor', related_name='contributed_blogs')
    language = models.CharField(
         max_length=50,
         choices=[
              ('en', _('English')),
              ('fr', _('French')),
              ('ki', _('kirundi')),
         ],
        default='English')
    created_at = models.DateTimeField(default=timezone.now)
    

    def _get_word_count(self):
        return len(self.content.split(' '))

    def save(self, *args, **kwargs):
        self.word_count = self._get_word_count()
        super().save(*args, **kwargs)
        exit

    class Meta:
        permissions = [
            ('change_blog_title', 'Can change the title of a blog')
        ]
class BlogContributor(models.Model):
            contributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
            blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
            contribution = models.CharField(max_length=255, blank=True)
            
            class Meta:
                 unique_together = ('contributor', 'blog')