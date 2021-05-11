from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    post_datetime = models.DateTimeField(auto_now_add=True, editable=False)
    update_datetime = models.DateTimeField(auto_now=True, editable=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    categories = models.ManyToManyField('Category', related_name='posts', blank=True)

    class Meta:
        ordering = ['-post_datetime']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.id})

    @property
    def get_content_beginning(self):
        list_of_words = self.content.split(' ')[:10]
        return ' '.join(list_of_words) + ' ...'


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Comment(models.Model):
    content = models.TextField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'For {self.post} by {self.author}'
