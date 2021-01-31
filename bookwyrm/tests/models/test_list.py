''' testing models '''
from django.test import TestCase

from bookwyrm import models, settings


class List(TestCase):
    ''' some activitypub oddness ahead '''
    def setUp(self):
        ''' look, a list '''
        self.user = models.User.objects.create_user(
            'mouse', 'mouse@mouse.mouse', 'mouseword',
            local=True, localname='mouse')
        self.list = models.List.objects.create(
            name='Test List', user=self.user)

    def test_remote_id(self):
        ''' shelves use custom remote ids '''
        expected_id = 'https://%s/user/mouse/list/%d' % \
            (settings.DOMAIN, self.list.id)
        self.assertEqual(self.list.get_remote_id(), expected_id)


    def test_to_activity(self):
        ''' jsonify it '''
        activity_json = self.list.to_activity()
        self.assertIsInstance(activity_json, dict)
        self.assertEqual(activity_json['id'], self.list.remote_id)
        self.assertEqual(activity_json['totalItems'], 0)
        self.assertEqual(activity_json['type'], 'OrderedCollection')
        self.assertEqual(activity_json['name'], 'Test List')
        self.assertEqual(activity_json['owner'], self.user.remote_id)
