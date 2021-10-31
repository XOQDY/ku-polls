"""Test for question model"""
import datetime

from django.test import TestCase
from django.utils import timezone

from ..models import Question


class QuestionModelTests(TestCase):
    """Test question model."""

    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for question whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns False for questions whose pub_dates older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() returns True for questions whose pub_dates within the last day."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_past_question(self):
        """is_published() returns True for whose pub_date is older than current time."""
        time = timezone.now() - datetime.timedelta(days=3)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.is_published(), True)

    def test_is_published_with_future_question(self):
        """is_published() returns False for whose pub_date is newer than current time."""
        time = timezone.now() + datetime.timedelta(days=2)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.is_published(), False)

    def test_can_vote_with_in_range_time_of_question(self):
        """can_vote() returns True when in voting range of time."""
        pub_date = timezone.now() - datetime.timedelta(hours=5)
        end_date = timezone.now() + datetime.timedelta(days=7)
        published_question = Question(pub_date=pub_date, end_date=end_date)
        self.assertIs(published_question.can_vote(), True)

    def test_can_vote_with_future_question(self):
        """can_vote() returns False when the question is not published yet."""
        pub_date = timezone.now() + datetime.timedelta(days=2)
        end_date = timezone.now() + datetime.timedelta(days=20)
        future_question = Question(pub_date=pub_date, end_date=end_date)
        self.assertIs(future_question.can_vote(), False)

    def test_can_vote_with_expired_question(self):
        """can_vote() returns False when the question is expired."""
        pub_date = timezone.now() - datetime.timedelta(days=10)
        end_date = timezone.now() - datetime.timedelta(minutes=1)
        expired_question = Question(pub_date=pub_date, end_date=end_date)
        self.assertIs(expired_question.can_vote(), False)