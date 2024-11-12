# voter_analytics/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path(r"", VotersListView.as_view(), name="home"),
    path(r"voters", VotersListView.as_view(), name="voters"),
    path(r"voter/<int:pk>", VoterDetailView.as_view(), name="voter_detail"),
    path(r"graphs", GraphsListView.as_view(), name="graphs"),
]
