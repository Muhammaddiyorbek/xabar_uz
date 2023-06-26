from django.db import models
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=News.Status.Published)

class Catigor(models.Model):
    name=models.CharField(max_length=255)
    url=models.CharField(max_length=255)

    def __str__(self) :
        return self.name

class News(models.Model):
    class Status(models.TextChoices):
        Draft="DF","Draft"
        Published="PB","Published"
    title=models.CharField(max_length=255)
    slug=models.SlugField(max_length=255)
    body=models.TextField()
    image=models.ImageField(upload_to='news/images/')
    category=models.ForeignKey(Catigor,on_delete=models.CASCADE)
    publish_time=models.DateTimeField(default=timezone.now)
    created_time=models.DateTimeField(auto_now_add=True)
    updated_time=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=2,
                            choices=Status.choices,
                            default=Status.Draft
                            )
    
    objects=models.Manager()
    published=PublishedManager()

    def photo(self):
        return mark_safe(f"""<a href='{self.image.url}' ><img src='{self.image.url}' width=100 style="border-radius: 10px;" /></a>""")


    class Meta:
        ordering=["-publish_time"]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('new_detail',args=[self.slug])
    
class Contact(models.Model):
    name=models.CharField(max_length=250)
    email=models.EmailField(max_length=250)
    message=models.TextField()

    def __str__(self):
        return self.name