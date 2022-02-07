from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify 


class SimilarSong(models.Model):
    genre = models.CharField(max_length=15)
    source = models.CharField(max_length=500)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Delete profile when user is deleted
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    

    def __str__(self):
        return "%s" % self.user

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user)
        super(Profile, self).save(*args, **kwargs)


class SavedSongs(models.Model):
    user = models.ForeignKey(User, unique=False, on_delete=models.CASCADE)
    song_name = models.CharField(max_length=30)
    genre = models.CharField(max_length=15)
    source = models.CharField(max_length=60)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "%s" % self.user

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user)
        super(SavedSongs, self).save(*args, **kwargs)
