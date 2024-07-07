from django.db import models
from django.contrib import admin
from django.utils.html import escape
from django.utils.safestring import mark_safe


class Family(models.Model):
    index = models.IntegerField(null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Zone(models.Model):
    index = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Detection(models.Model):
    base_dir = 'static/captures'
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)

    center_x = models.FloatField(null=True)
    center_y = models.FloatField(null=True)
    width = models.FloatField(null=True)
    height = models.FloatField(null=True)

    score = models.IntegerField(null=True)

    date = models.DateTimeField()

    photo_file = models.CharField(null=True, max_length=200)

    def photo_path(self):
        return f"{self.base_dir}/{self.photo_file}"

    def image_tag(self):
        return mark_safe('<a href="/%s" target="_blank">'
                         '<img src="/%s" width="150" height="150" />'
                         '</a>' % (self.photo_path(), self.photo_path()))
    image_tag.short_description = 'Image'

    def __str__(self):
        return f"{self.family} in {self.zone} at {self.date}"
