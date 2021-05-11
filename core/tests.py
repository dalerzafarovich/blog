from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from core.models import Post


class PostViewTest(TestCase):
    def setUp(self):
        for _ in range(10):
            Post.objects.create(title='Aboba', content='Hello')

    def test_post_list(self):
        resp = self.client.get(reverse('post-list'))
        self.assertTrue('post_list' in resp.context)
        self.assertEquals(len(resp.context['post_list']), 10)
        for post in resp.context['post_list']:
            self.assertEquals(str(post), 'Aboba')


class PostDeleteTest(TestCase):
    def setUp(self):
        test1 = User.objects.create_user(username='test1', password='12345')
        test1.save()
        test2 = User.objects.create_user(username='test2', password='12345')
        test2.save()

    def test_deleting_by_author(self):
        user = User.objects.get(pk=1)
        post = Post.objects.create(title='Title', content='text', author=user)
        post.save()
        login = self.client.login(username='test1', password='12345')
        resp = self.client.post(reverse('post-delete', kwargs={'pk': post.id}))
        self.assertEquals(resp.status_code, 302)
        self.assertRedirects(resp, reverse('my-post-list'))

    def test_deleting_not_by_author(self):
        user = User.objects.get(pk=1)
        post = Post.objects.create(title='Title', content='text', author=user)
        post.save()
        login = self.client.login(username='test2', password='12345')
        resp = self.client.post(reverse('post-delete', kwargs={'pk': post.id}))
        self.assertEquals(resp.status_code, 403)
