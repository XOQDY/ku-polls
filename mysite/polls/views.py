from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    response = "Yep this is result of question %s \U0001F973."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("If you don't know now you're voting on question %s. \U0001F631" % question_id)
