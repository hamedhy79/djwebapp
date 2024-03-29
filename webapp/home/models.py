from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateField(auto_now_add=True)
    update = models.DateField(auto_now=True)

    class Meta:
        ordering = ('body',)

    def __str__(self):
        return f'{self.slug}-{self.created}'

    def get_absolute_url(self):
        return reverse('home:post_detail', args=(self.id, self.slug))

    def likes_count(self):
        return self.post_votes.count()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='reply_comments', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=100)
    created = models.DateField(auto_now_add=True)

    def __self__(self):
        return f'{self.user} - {self.body[:20]}'


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_votes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_votes')

    def __str__(self):
        return f'{self.user} Liked {self.post.slug}'


class PersonSer(models.Model):
    name = models.CharField(max_length=30)
    age = models.PositiveSmallIntegerField()
    email = models.EmailField()

    def __str__(self):
        return self.name


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}-{self.title[:20]}'


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uanswer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='qanswer')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}-{self.question.title[:30]}'


class Car(models.Model):
    name = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name
