from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Author(models.Model):
    userAuthor = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.IntegerField(default=0)

    def update_rating(self):
        postRate = self.post_set.all().aggregate(postRating=Sum('rating'))
        pRate = 0
        pRate += postRate.get('postRating')

        commentRate = self.userAuthor.comment_set.all().aggregate(commentRating=Sum('rating'))
        cRate = 0
        cRate += commentRate.get('commentRating')

        self.ratingAuthor = pRate*3 + cRate
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    article = 'AR'
    news = 'NE'

    TYPE = [
        (article, 'Статья'),
        (news, 'Новость'),
    ]
    type = models.CharField(max_length=2, choices=TYPE, default=article)
    time_in = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentAuthor = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
