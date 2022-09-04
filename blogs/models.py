from django.db import models
from django.contrib.auth import get_user_model

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


class Post(models.Model):
    title = models.CharField(max_length=300, unique=True)
    slug = models.SlugField(max_length=300, unique=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    status = models.IntegerField(choices=STATUS, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


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
