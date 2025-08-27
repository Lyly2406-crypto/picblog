from django.conf import settings
from django.db import models
from PIL import Image


class Photo(models.Model):
    image = models.ImageField()
    IMAGE_MAX_SIZE = (800, 800)
    caption = models.CharField(max_length=128, blank=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)


    def resize_image(self):

        image = Image.open(self.image.path)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)   

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)
        self.resize_image()   

class BlogContributor(models.Model):
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE)
    contributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contributions = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('blog', 'contributor')


class Blog(models.Model):
    photo = models.ForeignKey(Photo, null=True, on_delete=models.SET_NULL, blank=True)
    title = models.CharField(max_length=128)
    content = models.CharField(max_length=5000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    contributors = models.ManyToManyField(settings.AUTH_USER_MODEL, through='BlogContributor', related_name='contributions')
    date_created = models.DateTimeField(auto_now_add=True)
    starred = models.BooleanField(default=False)
class Meta:
     permissions = [
            ('change_blog_title', 'Peut changer le titre d’un billet de blog')
        ]


