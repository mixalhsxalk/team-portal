from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Item, ItemRequest


class BorrowFlowTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user('owner', password='x')
        self.other = User.objects.create_user('other', password='x')
        self.item = Item.objects.create(owner=self.owner, name='ESP32', quantity=2)
        self.req = ItemRequest.objects.create(item=self.item, requester=self.other)
        self.client.force_login(self.owner)

    def act(self, action):
        return self.client.post(reverse('respond-request', args=[self.req.pk, action]))

    def qty(self):
        self.item.refresh_from_db()
        return self.item.quantity

    def test_approve_and_return_change_stock_once(self):
        self.act('approve')
        self.act('approve')
        self.assertEqual(self.qty(), 1)
        self.act('return')
        self.act('return')
        self.assertEqual(self.qty(), 2)

    def test_cannot_return_unapproved_request(self):
        self.act('return')
        self.assertEqual(self.qty(), 2)

    def test_get_does_not_change_state(self):
        self.client.get(reverse('respond-request', args=[self.req.pk, 'approve']))
        self.req.refresh_from_db()
        self.assertEqual(self.req.status, 'pending')

    def test_cannot_request_own_item(self):
        self.client.post(reverse('request-item', args=[self.item.pk]))
        self.assertFalse(ItemRequest.objects.filter(requester=self.owner).exists())
