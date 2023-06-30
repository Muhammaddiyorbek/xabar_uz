from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe

# Create your models here.
# class User():
#     photo=models.ImageField('users/images')
#     date_of_birth=models.DateTimeField()
#     address=models.TextField()

class Profile(models.Model):
    user=models.OneToOneField(User,
                              on_delete=models.CASCADE,)
    photo=models.ImageField(upload_to='users/images/',blank=True,null=True)
    date_of_birth=models.DateTimeField(blank=True,null=True)

    def image(self):
        return mark_safe(f"""<a href='{self.photo.url}' ><img src='{self.photo.url}' width=100 style="border-radius: 10px;" /></a>""")


    def __str__(self):
        return f"{self.user.username} profili"