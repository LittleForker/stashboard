"""
urls.py for Stashboard.

stashboard assumes that the it lives under /

Usage in your base urls.py:
(r'^/', include('stashboard.urls')),

"""

from django.conf.urls.defaults import *
from stashboard.views import *
from stashboard.models import *

urlpatterns = patterns(
    '',
    (r'^$', DefaultRegionView.as_view()),
    (r'^regions/(?P<region>[-\w]+)/services/(?P<service>[-\w]+)'
     '/announcements/(?P<pk>\d+)$', AnnouncementDetailView.as_view()),
    (r'^regions/(?P<region>[-\w]+)/services/(?P<service>[-\w]+)'
     '/announcements$', ServiceAnnouncementsView.as_view()),
    (r'^regions/(?P<region>[-\w]+)/services/(?P<service>[-\w]+)'
     '/issues/(?P<pk>\d+)$', IssueDetailView.as_view()),
    (r'^regions/(?P<region>[-\w]+)/services/(?P<service>[-\w]+)/issues$',
     ServiceIssuesView.as_view()),
    (r'^regions/(?P<region>[-\w]+)/services/(?P<slug>[-\w]+)$',
     ServiceDetailView.as_view()),
    (r'^regions/(?P<slug>[-\w]+)/services$', RegionDetailView.as_view()),
    (r'^regions/(?P<slug>[-\w]+)$', RegionDetailView.as_view()),
    (r'^feeds/all$', ActivityFeed.as_view()),
    (r'^feeds/issues$', IssueFeed.as_view()),
    (r'^feeds/announcements$', AnnouncementFeed.as_view()),

    # Admin
    (r'^accounts/login/$', 'django.contrib.auth.views.login',
     {'template_name': 'stashboard/login.html'}),
    (r'^admin/services/create$', ServiceFormView.as_view()),
    (r'^admin/services/(?P<pk>\d+)/edit$', ServiceEditView.as_view()),
    (r'^admin/services/(?P<pk>\d+)/delete$', ServiceDeleteView.as_view()),
    (r'^admin/services$', ServiceManageView.as_view()),
    # (r'^feeds/regions//services/(?P<slug>[-\w]+)/announcements$', ServiceAnnouncementFeed.as_view()),
    # (r'^feeds/regions///(?P<slug>[-\w]+)/issues$', ServiceIssueFeed.as_view()),
    # (r'^feeds/regions///(?P<slug>[-\w]+)/all-activity$', ServiceActivityFeed.as_view()),
)


