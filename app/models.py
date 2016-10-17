from django.db import models

# Create your models here.


class Bookmark(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey("auth.User")
    created = models.DateTimeField(auto_now_add=True)
    random_id = models.CharField(max_length=10)
    link = models.URLField()

    class Meta:
        ordering = ("-created",)

    @property
    def click_count(self):
        return sum(click_obj.count for click_obj in self.click_set.all())

    def __str__(self):
        return self.title


class Click(models.Model):
    bookmark = models.ForeignKey(Bookmark)
    visited = models.DateTimeField(auto_now_add=True)
    clicked = models.BooleanField()

    @property
    def click_count(self):
        if Click.clicked:
            return 1
        return 0
