from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from stashboard.models import *
from stashboard.forms import *

class RegionDetailView(DetailView):

    context_object_name = "region"
    model = Region

    def get_context_data(self, **kwargs):
        context = super(RegionDetailView, self).get_context_data(**kwargs)
        context['services'] = Service.objects.filter(region=self.object)
        context['statuses'] = Status.objects.all()
        return context

class DefaultRegionView(RegionDetailView):

    template_name = "stashboard/index.html"

    def get_object(self):
        return Region.objects.all()[0]

    def get_context_data(self, **kwargs):
        context = super(DefaultRegionView, self).get_context_data(**kwargs)
        context['regions'] = Region.objects.all()
        return context

class IssueDetailView(DetailView):

    context_object_name = "issue"
    model = Issue

    def get_object(self):
        region = get_object_or_404(Region, slug=self.kwargs["region"])
        service = get_object_or_404(Service, region=region,
                                    slug=self.kwargs["service"])
        return get_object_or_404(Issue, service=service,
                                 pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(IssueDetailView, self).get_context_data(**kwargs)
        # Get the object we're querying
        context['updates'] = Update.objects.filter(issue=self.object)
        return context

class ServiceIssuesView(ListView):

    model = Issue
    context_object_name = "issues"

    def get_queryset(self):
        self.region = get_object_or_404(Region, slug=self.kwargs["region"])
        self.service = get_object_or_404(Service, region=self.region,
                                    slug=self.kwargs["service"])
        return Issue.objects.filter(service=self.service).order_by("-opened")

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ServiceIssuesView, self).get_context_data(**kwargs)
        context['service'] = self.service
        return context

class AnnouncementDetailView(DetailView):

    model = Announcement

    def get_object(self):
        region = get_object_or_404(Region, slug=self.kwargs["region"])
        self.service = get_object_or_404(Service, region=region,
                                    slug=self.kwargs["service"])
        return get_object_or_404(Announcement, service=self.service,
                                 pk=self.kwargs["pk"])


class ServiceAnnouncementsView(ListView):

    model = Announcement

    def get_queryset(self):
        self.region = get_object_or_404(Region, slug=self.kwargs["region"])
        self.service = get_object_or_404(Service, region=self.region,
                                    slug=self.kwargs["service"])
        return Announcement.objects.filter(service=self.service).order_by("-created")

    def get_context_data(self, **kwargs):
        context = super(ServiceAnnouncementsView, self).get_context_data(**kwargs)
        context['service'] = self.service
        return context


class ServiceDetailView(DetailView):

    context_object_name = "service"
    model = Service

    def get_object(self):
        region = get_object_or_404(Region, slug=self.kwargs["region"])
        return get_object_or_404(Service, region=region,
                                 slug=self.kwargs["slug"])

    def get_context_data(self, **kwargs):
        context = super(ServiceDetailView, self).get_context_data(**kwargs)
        context['announcements'] = self.object.get_recent_announcements()
        issues = self.object.get_open_issues()
        if issues:
            context['issues'] = issues
            context['issue_type'] = "Open Issues"
        else:
            context['issues'] = self.object.get_recent_issues()
            context['issue_type'] = "Recently Resolved Issues"
        return context


class StatusListView(ListView):

    model = Status
    context_object_name = "status_list"


class RegionListView(ListView):

    model = Region
    context_object_name = "region_list"


class AnnouncementFeed(ListView):
    context_object_name = "announcement_list"
    template_name = "stashboard/announcement_feed.html"
    queryset = Announcement.objects.order_by("-created")


class ServiceAnnouncementFeed(AnnouncementFeed):

    def get_queryset(self):
        service =  get_object_or_404(Service, slug=self.kwargs["slug"])
        return Announcement.objects.filter(service=service).order_by("-created")


class ActivityFeed(ListView):
    context_object_name = "log_list"
    template_name = "stashboard/activity_feed.html"
    queryset = LogEntry.objects.order_by("-opened")


class ServiceActivityFeed(ListView):

    def get_queryset(self):
        service =  get_object_or_404(Service, slug=self.kwargs["slug"])
        return LogEntry.objects.filter(service=service).order_by("-created")

class IssueFeed(ListView):
    context_object_name = "issue_list"
    template_name = "stashboard/issue_feed.html"
    queryset = Issue.objects.order_by("-opened")

class ServiceIssueFeed(IssueFeed):

    def get_queryset(self):
        service =  get_object_or_404(Service, slug=self.kwargs["slug"])
        return Issue.objects.filter(service=service).order_by("-opened")
