from django.shortcuts import render
from django.http import HttpResponse
from .models import Conference
from django.views.generic import ListView ,DetailView , CreateView , UpdateView , DeleteView
from django.urls import reverse_lazy
from .forms import ConferenceForm
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from rest_framework  import viewsets
from .serializers import ConferenceSerializer   
# Create your views here.



class conferenceViewSet(viewsets.ModelViewSet):
    """
    a viewset for viewing and editing conference instances.
    -list() -> Get /conferences/
    -retrieve() -> Get /conferences/{id}/
    -create() -> Post /conferences/
    -update() -> Put /conferences/{id}/
    -partial_update() -> Patch /conferences/{id}/
    -destroy() -> Delete /conferences/{id}/


   
    """
    queryset = Conference.objects.all()
    serializer_class = ConferenceSerializer 



def home (request):
    return HttpResponse("Welcome to the Home Page!</h1>")

def about (request):
    return render (request, 'conferenceApp/about.html')

def welcome (request , name ):
    return render (request, 'conferenceApp/welcome.html' ,
     {'n': name}) #context dictionary 

def listconferences(request):
    conferences = Conference.objects.all().order_by('name')
    return render(request, 'conferenceApp/conference_list.html', {'conferences': conferences})

class ConferenceListView(ListView):
    model = Conference
    context_object_name ='conferences'
    template_name = 'conferenceApp/conference_list.html'


class conferenceDetailView(DetailView):
    model = Conference

class conferenceCreateView(LoginRequiredMixin ,UserPassesTestMixin ,CreateView):
    model = Conference
    #fields = '__all__'#
    form_class = ConferenceForm
    success_url = reverse_lazy ('conference_listLV')
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.role == 'organizer'
  
class conferenceUpdateView(UpdateView):
    model = Conference
    fields = '__all__'
    success_url = reverse_lazy ('conference_listLV')   

class conferenceDeleteView(LoginRequiredMixin ,UserPassesTestMixin ,DeleteView):
    model = Conference
    template_name = 'conferenceApp/conference_confirm_delete.html'
    success_url = reverse_lazy ('conference_listLV')

 
