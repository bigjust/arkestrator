from django.test import TestCase
from models import Thread, Post

from django.contrib.auth.models import User
from django.contrib.sites.models import Site

import datetime

class ThreadTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('foo','foo@bar.net','badpassword')
        self.site = Site.objects.get_current()

    def test_create_thread(self): 
        thread = Thread.objects.create(
            subject="Hello, World",
            creator=self.user,
            site=self.site)

    def test_str(self):
        thread = Thread.objects.create(
            subject="Hello, World",
            creator=self.user,
            site=self.site)

        self.assertEquals(str(thread),"Hello, World")

class PostTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('foo','foo@bar.net','badpass')
        self.user2 = User.objects.create_user('bar','bar@foo.net','badpass')
        self.site = Site.objects.get_current()
        self.thread = Thread.objects.create(
            subject="Hello, World",
            creator=self.user1,
            site=self.site)
    
    def test_create_post(self):
        post = Post.objects.create(
            thread=self.thread,
            creator=self.user1,
            body="Take and eat; this is my body."
        )

    def test_post_str(self):
        post = Post.objects.create(
            thread=self.thread,
            creator=self.user1,
            body="Take and eat; this is my body."
        )

        self.assertEquals(str(post),"%s: %s"%(str(post.thread),post.body[:20]))

    def test_update_thread_signal(self):
        # timestamp 2 days in the future
        ts = datetime.datetime.now() + datetime.timedelta(2)

        post = Post.objects.create(
            thread=self.thread,
            creator=self.user2,
            body="Take and eat; this is my body.",
            created_at=ts
        )

        self.assertEqual(self.thread.last_post.creator, self.user2)
        self.assertEqual(self.thread.last_post.created_at, ts)

