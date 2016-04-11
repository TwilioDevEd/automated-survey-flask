from .base import BaseTest


class RootTest(BaseTest):

    def test_it_works(self):
        response = self.client.get('/')
        self.assertEquals(200, response.status_code)
