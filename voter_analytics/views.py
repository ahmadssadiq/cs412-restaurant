# voter_analytics/views.py
from django.shortcuts import render
from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from .models import Voter
import plotly
import plotly.graph_objs as go


class VotersListView(ListView):
    """view to show a list of voters"""

    template_name = "voter_analytics/voters.html"
    model = Voter
    context_object_name = "voters"
    paginate_by = 100

    def get_queryset(self) -> QuerySet[Any]:
        """limit the voters to a small number of records"""
        qs = Voter.objects.all()

        # handle search party parameters:
        if "party_affiliation" in self.request.GET:
            party = self.request.GET["party_affiliation"]
            qs = qs.filter(party_affiliation__icontains=party)

        # handle search min. dob year parameters:
        if "min_dob_year" in self.request.GET:
            min_year = self.request.GET["min_dob_year"] + "-01-01"
            qs = qs.filter(date_of_birth__gte=min_year)

        # handle search max. dob year parameters:
        if "max_dob_year" in self.request.GET:
            max_year = self.request.GET["max_dob_year"] + "-01-01"
            qs = qs.filter(date_of_birth__lte=max_year)

        # handle search voter score parameters:
        if "voter_score" in self.request.GET:
            score = self.request.GET["voter_score"]
            qs = qs.filter(voter_score=score)

        # handle participation options:
        for field in ["v20state", "v21town", "v21primary", "v22general", "v23town"]:
            if field in self.request.GET:
                qs = qs.filter(**{field: "TRUE"})

        return qs


class VoterDetailView(DetailView):
    """view to show detail page for one voter"""

    template_name = "voter_analytics/voter_detail.html"
    model = Voter
    context_object_name = "v"


class GraphsListView(ListView):
    """view to show a list of graphs displaying voter information"""

    template_name = "voter_analytics/graphs.html"
    model = Voter
    context_object_name = "v"

    def get_context_data(self, **kwargs):
        """provide context variables for use in this template"""
        context = super().get_context_data(**kwargs)
        all_voters = Voter.objects.all()

        # Voter distribution by birth year
        birth_years = [
            voter.date_of_birth.year for voter in all_voters if voter.date_of_birth
        ]
        years = list(set(birth_years))
        dist_year = [birth_years.count(year) for year in years]

        fig = go.Figure(data=[go.Bar(x=years, y=dist_year)])
        fig.update_layout(
            title=f"Voter distribution by birth year (total={sum(dist_year)})"
        )
        context["graph_birth_year"] = plotly.offline.plot(
            fig, auto_open=False, output_type="div"
        )

        # Party affiliation distribution
        parties = list(set(v.party_affiliation for v in all_voters))
        dist_party = [
            all_voters.filter(party_affiliation=party).count() for party in parties
        ]

        fig = go.Pie(labels=parties, values=dist_party)
        context["graph_party"] = plotly.offline.plot(
            {
                "data": [fig],
                "layout_title_text": "Voter distribution by party affiliation",
            },
            auto_open=False,
            output_type="div",
        )

        # Vote counts by election
        vote_fields = ["v20state", "v21town", "v21primary", "v22general", "v23town"]
        dist_vote = [
            all_voters.filter(**{field: "TRUE"}).count() for field in vote_fields
        ]

        fig = go.Figure(data=[go.Bar(x=vote_fields, y=dist_vote)])
        fig.update_layout(title=f"Vote counts by election (total={sum(dist_vote)})")
        context["graph_votes"] = plotly.offline.plot(
            fig, auto_open=False, output_type="div"
        )

        return context
