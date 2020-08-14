from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length = 32)
    description = models.TextField(max_length = 360)

    def no_of_ratings(self):
        ratings = Ratings.objects.filter(movie = self)
        return len(ratings)

    def avg_ratings(self):
        sum_of_ratings = sum(Ratings.objects.filter(movies=self),key = lambda x:x.stars)

        if self.no_of_ratings > 0:
            return sum_of_ratings/self.no_of_ratings
        return 0


class Ratings(models.Model):
    movie = models.ForeignKey(Movie, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    stars = models.IntegerField(validators = [MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = (('user','movie'),)
        index_together = (('user','movie'),)

