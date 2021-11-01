"""Template for each urls."""
import logging

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed

from .models import Choice, Question, Vote


class IndexView(generic.ListView):
    """Index view."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions (not including those set to be published in the future)."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """Detail view."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """Results view."""

    model = Question
    template_name = 'polls/results.html'


@login_required(login_url='/accounts/login/')
def vote(request, question_id):
    """When user click vote in each question."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Bro you didn't select any choice \U0001F624.",
        })
    else:
        if question.vote_set.filter(user=request.user).exists():
            vote = question.vote_set.get(user=request.user)
            vote.choice = selected_choice
            vote.save()
        else:
            selected_choice.vote_set.create(user=request.user, question=question)
        return HttpResponseRedirect(reverse('polls:results', args=(question_id, )))


@login_required(login_url='/accounts/login/')
def detail(request, question_id=None):
    """Detail view but when polls aren't available redirect user to index page."""
    question = get_object_or_404(Question, pk=question_id)
    if not question.can_vote():
        messages.error(request, f"Yo man you can't vote on \"{question.question_text}\" poll anymore its to late. "
                                f"\U0001F612")
        return HttpResponseRedirect(reverse('polls:index'))
    else:
        return render(request, 'polls/detail.html', {'question': question, })


def get_client_ip(request):
    """Get the visitor’s IP address using request headers."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def on_login(user, request, **kwargs):
    """A message show about user info when the user is login."""
    logger.info(f"Sub {user.username} We know your IP's {get_client_ip(request)} Don't "
                f"mind we just want to say hi to you.")


@receiver(user_logged_out)
def on_logout(user, request, **kwargs):
    """A message show about user info when the user is logout."""
    logger.info(f"C ya {user.username} sad to say but your IP's {get_client_ip(request)} has been ejected.")


@receiver(user_login_failed)
def login_fail(credentials, request, **kwargs):
    """Log a message at the warning level when the user failed login."""
    logger.warning(f"Dude IP: {get_client_ip(request)} sh idk why but you're failed to log in to "
                   f"{credentials['username']}")
