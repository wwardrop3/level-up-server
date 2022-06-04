from django.urls import path
from levelupreports.views.eventbyuser import UserEventList

from levelupreports.views.gamesbyuser import UserGameList

urlpatterns = [
    path('reports/usergames', UserGameList.as_view()),
    path('reports/userevents', UserEventList.as_view())
]