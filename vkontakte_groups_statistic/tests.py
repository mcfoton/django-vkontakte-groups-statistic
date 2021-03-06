# -*- coding: utf-8 -*-
from datetime import timedelta, date

from django.test import TestCase
from models import GroupStat, GroupStatistic, GroupStatisticMembers
from vkontakte_groups.models import Group
from django.utils import timezone
from vkontakte_groups.factories import GroupFactory

from .models import GroupStat, GroupStatistic

GROUP_ID = 1


class VkontakteGroupsStatisticTest(TestCase):

    def test_fetch_statistic(self):

        group = GroupFactory(remote_id=GROUP_ID)
        self.assertEqual(GroupStat.objects.count(), 0)

        group.fetch_statistic()
        self.assertGreater(GroupStat.objects.count(), 350)

        stat = GroupStat.objects.filter(period=30)[0]
        self.assertGreater(stat.views, 0)
        self.assertGreater(stat.visitors, 0)
        self.assertIsInstance(stat.date, date)

        stat = GroupStat.objects.filter(period=1)[0]
        self.assertGreater(stat.members, 0)
        self.assertGreater(stat.views, 0)
        self.assertGreater(stat.visitors, 0)
        self.assertGreater(stat.males, 0)
        self.assertGreater(stat.females, 0)
        self.assertIsInstance(stat.date, date)

        # test date_from argument
        date_from = timezone.now() - timedelta(5)
        stat_month_count = GroupStat.objects.filter(period=30).count()
        GroupStat.objects.all().delete()

        group.fetch_statistic(date_from=date_from)
        self.assertEqual(GroupStat.objects.filter(period=1).count(), 6)
        self.assertEqual(GroupStat.objects.filter(period=30).count(), stat_month_count)
        
    def test_fetch_statistic_via_api(self):

        group = GroupFactory(remote_id=GROUP_ID)
        self.assertEqual(GroupStatistic.objects.count(), 0)

        group.fetch_statistic(source='api')
        self.assertGreater(GroupStatistic.objects.count(), 0)

        stat = GroupStatistic.objects.all()[0]
        self.assertGreater(stat.views, 0)
        self.assertGreater(stat.visitors, 0)
        self.assertGreater(stat.males, 0)
        self.assertGreater(stat.females, 0)
        self.assertIsInstance(stat.date, date)

class VkontakteGroupsStatisticMembers(TestCase):
    #TODO rewrite using model other than Group and factory (?)
    def test_new_members_count_instance(self):
        count = GroupStatisticMembers.objects.count()
        Group.remote.fetch(ids=[GROUP_ID])
        self.assertEqual(GroupStatisticMembers.objects.count(), count+1)
'''
    def test_new_members_count_instance_factory(self):

        group = GroupFactory(remote_id=GROUP_ID)
        self.assertEqual(GroupStatisticMembers.objects.count(), 0)

        group.fetch_statistic(source='api')
        self.assertNotEqual(GroupStatisticMembers.objects.count(), 0)

        stat = GroupStatisticMembers.objects.all()[0]
        self.assertTrue(stat.members_count > 0)
        self.assertNotEqual(stat.updated_at, None)
'''