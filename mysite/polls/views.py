from django.http import HttpResponse


def index(request):
    return HttpResponse("Yo this is polls website if you don't know it btw. \U0001F618")
