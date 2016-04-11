from .base import BaseTest
from xmlunittest import XmlTestCase


class RootTest(BaseTest):

    def test_it_works(self):
        response = self.client.get('/')
        self.assertEquals(200, response.status_code)


class SurveysViewTest(BaseTest, XmlTestCase):

    def test_says_welcome_on_a_call(self):
        response = self.client.get('/voice')
        self.assertXmlDocument(response.data)
