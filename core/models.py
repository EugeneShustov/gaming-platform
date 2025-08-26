from django.db import models
from django.db.models import Avg

class Game(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    release_date = models.DateField()
    cover_image = models.ImageField(upload_to='covers/')
    video_url = models.URLField(blank=True)
    developer = models.CharField(max_length=255, blank=True, null=True)
    platforms = models.CharField(max_length=255, blank=True, null=True)

    def average_rating(self):
        return self.posts.aggregate(Avg('rating'))['rating__avg']

    def __str__(self):
        return self.title

class Post(models.Model):
    game = models.ForeignKey(Game, related_name='posts', on_delete=models.CASCADE)
    author = models.CharField(max_length=100, default='Anonymous')
    content = models.TextField()
    rating = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class BackgroundImage(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='backgrounds/')
    display_time = models.IntegerField(help_text="")

class Screenshot(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='screenshots/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Screenshot {self.game}"