from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

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

    topic = models.ForeignKey(Topic, related_name="%(class)s_set", on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    web_link = models.URLField(null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=100)
    finished = models.BooleanField(default=False)
    summary = models.ForeignKey("Summary", on_delete=models.CASCADE, null=True, blank=True)

    def __unicode__(self):
        return "%s(%s-%s)".format(self.name, self.start_date, self.end_date)


class Event(models.Model):
    class Meta:
        abstract = True
        ordering = ['start_time']

    # The following field should be declared in child classes.
    # event_set = models.ForeignKey(EventSet, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    finished = models.BooleanField(default=False)
    summary = models.ForeignKey("Summary", on_delete=models.CASCADE)

    @property
    def due(self):
        return datetime.now(pytz.UTC) >= self.start_time

    @property
    def encoded_id(self):
        return urlsafe_base64_encode(force_bytes(self.pk))

    @staticmethod
    def decode_id(encoded_id):
        return urlsafe_base64_decode(encoded_id)


class Prediction(models.Model):
    class Meta:
        abstract = True
        unique_together = ('foreteller', 'event')

    foreteller = models.ForeignKey(User, related_name="predictions", on_delete=models.CASCADE)
    # The following field should be declared in child classes.
    # event = models.ForeignKey(Event, related_name="predictions", on_delete=models.CASCADE)
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
