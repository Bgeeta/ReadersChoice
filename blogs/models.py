from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
import secrets

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)
def get_token_slug():
    return secrets.token_urlsafe(15)

def get_image_filename(instance, filename):
    return f"post_images/{slugify(instance.post.title)}-{filename}"


class Post(models.Model):
    title = models.CharField(max_length=300, unique=True)
    slug = models.SlugField(max_length=300,default=get_token_slug,editable=False,blank=False, unique=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    status = models.IntegerField(choices=STATUS, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Images(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename, verbose_name='Image')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    # name = models.CharField(max_length=80)
    # email = models.EmailField()
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="commented_by")
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.created_by.username)
