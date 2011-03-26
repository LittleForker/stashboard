"""
urls.py for Stashboard.

stashboard assumes that the it lives under /

Usage in your base urls.py:
(r'^/', include('stashboard.urls')),

"""

from django.conf.urls.defaults import *
from stashboard.views import *
from stashboard.models import *

servicepatterns = patterns('',
    url(r'^$', ServiceDetail.as_view()),
    url(r'/issues$', ServiceIssues.as_view(), name="service-issues"),
    url(r'/issues/(?P<pk>\d+)$', IssueDetail.as_view()),
    url(r'/announcements$', ServiceAnnouncements.as_view(), name="service-announcements"),
    url(r'/announcements/(?P<pk>\d+)$', AnnouncementDetail.as_view()),
)

regionpatterns = patterns('',
    url(r'^$', RegionDetail.as_view()),
    url(r'/services/(?P<service>[-\w]+)', include(servicepatterns)),
)

servicefeeds = patterns('',
    url(r'^$', ServiceActivityFeed.as_view(), name="service-feed"),
    url(r'^/issues$', ServiceIssueFeed.as_view(), name="issues-feed"),
    url(r'^/announcements$', ServiceAnnouncementFeed.as_view(),
        name="announcements-feed"),
)

feedpatterns = patterns('',
    # url(r'^/all$', None),
    # url(r'^/issues$', None),
    # url(r'^/announcements$', None),
    url(r'^/regions/(?P<region>[-\w]+)/services/(?P<service>[-\w]+)', include(servicefeeds)),
)

urlpatterns = patterns('',
    url(r'^$', DefaultRegion.as_view()),
    url(r'^regions/(?P<region>[-\w]+)', include(regionpatterns)),
    url(r'^feeds', include(feedpatterns)),
)


