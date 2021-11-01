"""Models for polls."""
import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    """Question model."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('end date', null=True, default=timezone.now)

    def __str__(self):
        """Return name of question."""
        return self.question_text

    def was_published_recently(self):
        """Return True if poll is publish recently."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def is_published(self):
        """Return True if current date is on or after question’s publication date."""
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        """Return True if voting is currently allowed for this question."""
        now = timezone.now()
        return self.end_date >= now >= self.pub_date


class Choice(models.Model):
    """Choice model."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        """Return choice."""
        return self.choice_text

    @property
    def votes(self):
        """Return vote result of the choice."""
        return Vote.objects.filter(choice=self).count()


class Vote(models.Model):
    """Vote model."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE, default=0)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=0)

    def __str__(self):
        """Return the representation of vote."""
        return f"{self.choice} got deez {self.question} question."
