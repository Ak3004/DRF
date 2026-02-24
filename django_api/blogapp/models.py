from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.text import slugify

# Create  your models here.
class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    facebook_profile = models.URLField(max_length=255, blank=True, null=True)
    youtube_profile = models.URLField(max_length=255, blank=True, null=True)
    instagram_profile = models.URLField(max_length=255, blank=True, null=True)
    twitter_profile = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username
    
class Blog(models.Model):

    CATEGORY = (
        ('Technology', 'Technology'),
        ('Lifestyle', 'Lifestyle'),
        ('Business', 'Business'),
        ('Economy', 'Economy'),
        ('Sports', 'Sports')
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True,blank=True)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,related_name='blogs', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(null=True, blank=True)
    is_draft = models.BooleanField(default=True)
    category = models.CharField(max_length=255, choices=CATEGORY, null=True, blank=True)
    featured_image = models.ImageField(upload_to='blog_img', blank=True, null=True)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        base_slug=slugify(self.title)
        slug=base_slug
        num=1
        while Blog.objects.filter(slug=slug).exists():
            slug=f'{base_slug}-{num}'
            num+=1
        self.slug=slug

        if not self.is_draft and self.published_date is None:
            self.published_date = timezone.now()
        
        super().save(*args, **kwargs)