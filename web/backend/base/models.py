from django.db import models
from django.contrib.auth.models import User

from datetime import datetime
import pytz

from .badges import Badge


class Topic(models.Model):
    class Meta:
        db_table = "psh_topic"

    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name


class EventSet(models.Model):
    class Meta:
        abstract = True
        ordering = ['start_date']

    topic = models.ForeignKey(Topic, related_name="event_sets", on_delete=models.SET_NULL)
    name = models.CharField(max_length=100)
    web_link = models.URLField(null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=100)
    finished = models.BooleanField(default=False)
    summary = models.ForeignKey("Summary", on_delete=models.CASCADE, null=True, blank=True)


class Event(models.Model):
    class Meta:
        abstract = True
        ordering = ['start_time']

    event_set = models.ForeignKey(EventSet, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    finished = models.BooleanField(default=False)
    summary = models.ForeignKey("Summary", on_delete=models.CASCADE)


class Prediction(models.Model):
    class Meta:
        abstract = True

    foreteller = models.ForeignKey(User, related_name="predictions", on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name="predictions", on_delete=models.CASCADE)
    normal_badge = models.PositiveIntegerField(choices=Badge.normal_types, null=True, blank=True)
    exceptional_badge = models.PositiveIntegerField(choices=Badge.exceptional_types, null=True, blank=True)
    created_on = models.DateTimeField(editable=False)
    last_modified = models.DateTimeField()
    edit_count = models.PositiveIntegerField(default=0)
    concluded = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now(pytz.UTC)
        else:
            self.edit_count += 1
        self.modified = datetime.now(pytz.UTC)
        return super(Prediction, self).save(*args, **kwargs)


class Summary(models.Model):
    class Meta:
        db_table = "psh_summary"
        verbose_name_plural = "summaries"

    royal = models.PositiveIntegerField(default=0)
    full_house = models.PositiveIntegerField(default=0)
    straight = models.PositiveIntegerField(default=0)
    eye_less = models.PositiveIntegerField(default=0)

    oracle = models.PositiveIntegerField(default=0)
    nostradamus = models.PositiveIntegerField(default=0)
    trelawney = models.PositiveIntegerField(default=0)
