from django.test import TestCase, client

class ProcutListTestcase(TestCase):
    def test_prodcut_list(self):

        request = client.Client()

        response = request.get('/products')
        self.assertEqual(response.status_code, 401)