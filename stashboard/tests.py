"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
import django
from datetime import datetime, timedelta
from stashboard.models import *

class RegionTest(django.test.TestCase):

    def test_creation(self):
        region = Region.objects.create(slug="us-east", name="U.S. East",
                        location="United States of America")
        self.assertEqual(region.name, "U.S. East")
        self.assertEqual(region.location, "United States of America")
        self.assertEqual(region.slug, "us-east")

class StatusTest(django.test.TestCase):

    def test_creation(self):
        status = Status.objects.create(slug="downd", name="Down", image="down.png",
                        description="The service is currently down", color="green")
        self.assertEqual(status.slug, "downd")
        self.assertEqual(status.name, "Down")
        self.assertEqual(status.image, "down.png")
        self.assertEqual(status.description, "The service is currently down")
        self.assertEqual(status.highlight_hex(), "#daf1b8")
        self.assertEqual(status.color_hex(), "#86c440")
        self.assertEqual(status.color, "green")

class ServiceTest(django.test.TestCase):

    def setUp(self):
        status = Status.objects.create(slug="downd", name="Down", image="down.png",
                                       description="The service is currently down")
        self.region = Region.objects.create(slug="us-east", name="U.S. East",
                                       location="United States of America")
        self.service = Service.objects.create(slug="fake-service",
                                              name="Fake Service",
                                              description="This is fake, yo",
                                              region=self.region, status=status)

    def test_creation(self):
        self.assertEqual(self.service.slug, "fake-service")
        self.assertEqual(self.service.name, "Fake Service")
        self.assertEqual(self.service.region, self.region)
        self.assertEqual(self.service.description, "This is fake, yo")

    def test_feed_urls(self):
        (aa, an, iss) = self.service.feeds()
        self.assertEquals(aa["title"], "All Activity")
        self.assertEquals(aa["url"], "/feeds/services/fake-service/all-activity")

class LogEntryTest(django.test.TestCase):

    def setUp(self):
        status = Status.objects.create(slug="downd", name="Down", image="down.png",
                                       description="The service is currently down")
        self.region = Region.objects.create(slug="us-east", name="U.S. East",
                        location="United States of America")
        self.service = Service.objects.create(slug="fake-service",
                                              name="Fake Service",
                                              description="This is fake, yo",
                                              region=self.region,
                                              status=status)

    def test_creation(self):
        entry = LogEntry.objects.create(url="/test/url", service=self.service,
                        description="The service has been changed from down to up")
        self.assertEqual(entry.url, "/test/url")
        self.assertEqual(entry.service, self.service)
        self.assertEqual(entry.description,
                         "The service has been changed from down to up")


class RecentEventsTest(django.test.TestCase):

    def setUp(self):
        status = Status.objects.create(slug="downd", name="Down", image="down.png",
                                       description="The service is currently down")
        self.region = Region.objects.create(slug="us-east", name="U.S. East",
                                            location="United States of America")
        self.service = Service.objects.create(slug="fake-service",
                                              name="Fake Service",
                                              description="This is fake, yo",
                                              region=self.region, status=status)

    def test_no_open_issues(self):
        result = self.service.get_open_issues()
        self.assertEquals(0, len(result))

    def test_no_recent_issues(self):
        result = self.service.get_recent_issues()
        self.assertEquals(0, len(result))

    def test_no_recent_announcements(self):
        result = self.service.get_recent_announcements()
        self.assertEquals(0, len(result))

    def test_one_recent_announcements(self):
        i = Announcement.objects.create(service=self.service, message="HEY YEAH",
                                        title="One of many")
        a = Announcement.objects.create(service=self.service, message="HEY YEAH",
                                        title="One of many")
        a.created = datetime.now() - timedelta(days=7)
        a.save()

        result = self.service.get_recent_announcements()
        self.assertEquals(1, len(result))

    def test_one_open_issue(self):
        i = Issue.objects.create(service=self.service, description="HEY")
        self.assertEquals(1, len(self.service.get_open_issues()))
        self.assertEquals(1, len(self.service.get_recent_issues()))

