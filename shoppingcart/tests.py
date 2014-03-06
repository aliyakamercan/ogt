from django.test import TestCase, RequestFactory
# from mock import Mock

from shoppingcart.models import Store, Product
from shoppingcart.middleware import SubdomainProcessor
import views

# Create your tests here.

class SubdomainMiddlewareTest(TestCase):
    def setUp(self):
        self.mw = SubdomainProcessor()
        self.factory = RequestFactory()
        self.store = Store.objects.create(name='TestStore', sub_domain='test')

    def test_existing_store(self):
        request = self.factory.get('/', HTTP_HOST = 'test.example.com')
        self.mw.process_request(request)
        self.assertEqual(request.store, self.store)

    def test_missing_store(self):
        request = self.factory.get('/', HTTP_HOST = 'missing.example.com')
        response = self.mw.process_request(request)
        self.assertContains(response, 'The store you were looking for was not found.')
        self.assertEqual(request.store, None)

class IndexTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.mw = SubdomainProcessor()

        store1 = Store.objects.create(name='TestStore1', sub_domain='test1')
        Product.objects.create(name='test1 store p1', price=5.0, inventory=5, store=store1)

        store2 = Store.objects.create(name='TestStore2', sub_domain='test2')
        Product.objects.create(name='test2 store p1', price=5.0, inventory=5, store=store2)

    def test_store_basic(self):
        request = self.factory.get('/', HTTP_HOST = 'test1.example.com')
        self.mw.process_request(request)
        response = views.index(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test1 store p1')
        self.assertNotContains(response, 'test2 store p1')


