from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth.models import User

from item_api.models import Item, Category


class ItemApiTests(APITestCase):
    def setUp(self) -> None:
        """
        Setting the test environment with user and items and fetching the auth token
        :return:
        """

        self.new_user = User.objects.create_user(username='setupuser@gmail.com', password='pass$12345')
        self.category = Category.objects.create(name='Food')
        self.item = Item.objects.create(
            sku='Stock-1', name='stock1', category=self.category,
            currentStock=69, availableStock=100, tag="New Arrival"
        )
        url = reverse('login')
        data = {
            'username': 'setupuser@gmail.com',
            'password': 'pass$12345',
        }

        response = self.client.post(url, data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue('username' in response_data)
        self.assertTrue('access_token' in response_data)
        self.token = response_data['access_token']

    def test_get_items(self):
        """
        Listing all the items
        :return:
        """
        url = reverse('list')
        headers = {
            'Authorization': 'Bearer %s' % self.token
        }
        response = self.client.get(url, headers=headers, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data['results']), 1)

    def test_get_item_by_id(self):
        """
        Listing the item by a stock_id
        :return:
        """
        url = reverse('list_stock_item', kwargs={'stock_id': self.item.id})
        headers = {
            'Authorization': 'Bearer %s' % self.token
        }
        response = self.client.get(url, headers=headers, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['name'], self.item.name)

    def test_item_list_pagination(self):
        """
        Testing Pagination of the response
        :return:
        """
        url = reverse('list')
        headers = {
            'Authorization': 'Bearer %s' % self.token
        }
        response = self.client.get(url, {'page': 1}, headers=headers)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response contains pagination metadata
        self.assertIn('count', response_data)
        self.assertIn('next', response_data)
        self.assertIn('previous', response_data)
        self.assertIn('results', response_data)

        self.assertEqual(len(response_data['results']), 1)

    def test_create_item(self):
        """
        Creating a new item
        :return:
        """
        data = {
            'sku': 'Stock-2',
            'name': 'Stock2',
            'category': 1, # Food
            'tags': 'Fresh',
            'currentStock': 789.56,
            'availableStock': 1500
        }
        url = reverse('add')
        headers = {
            'Authorization': 'Bearer %s' % self.token
        }

        response = self.client.post(url, data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 2)

        created_item = Item.objects.latest('id')
        self.assertEqual(created_item.name, data['name'])
        self.assertEqual(created_item.currentStock, data['currentStock'])

    def test_delete_item(self):
        """
        Deleting an item by stock_id
        :return:
        """
        url = reverse('delete_stock_item', kwargs={'stock_id': self.item.id})
        headers = {
            'Authorization': 'Bearer %s' % self.token
        }

        response = self.client.delete(url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 0)

