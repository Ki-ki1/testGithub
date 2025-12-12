from django.urls import path
from .views import *
urlpatterns = [
    path('home/',home, name='conference_home'),
    path('about/',about, name='conference_about'),
    path('welcome/<str:name>',welcome, name='conference_welcome'),
    path('list/', listconferences, name='conference_list'),
    path('listLV/', ConferenceListView.as_view(), name='conference_listLV'),
    path('detailLV/<int:pk>/', conferenceDetailView.as_view(), name='conference_detailLV'),
    path('create/', conferenceCreateView.as_view(), name='conference_create'),
    path('update/<int:pk>/', conferenceUpdateView.as_view(), name='conference_update'),
    path('delete/<int:pk>/', conferenceDeleteView.as_view(), name='conference_delete'),

]
