from django.urls import path
from .views import session_list, SessionListView

urlpatterns = [
    path('', session_list, name='session_list_function'),
    path('class/', SessionListView.as_view(), name='session_list_class'),
]
