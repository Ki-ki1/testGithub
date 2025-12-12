from django.shortcuts import render
from django.views.generic import ListView
from .models import Session


class SessionListView(ListView):
    model = Session
    template_name = 'session_list.html'
    context_object_name = 'sessions'
    ordering = ['start_time']


def session_list(request):
    sessions = Session.objects.all().order_by('start_time')
    return render(request, 'session_list.html', {'sessions': sessions})
