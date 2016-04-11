from .base import BaseTest
from xmlunittest import XmlTestCase


class RootTest(BaseTest):

    def test_it_works(self):
        response = self.client.get('/')
        self.assertEquals(200, response.status_code)


class SurveysViewTest(BaseTest, XmlTestCase):

    def test_says_welcome_on_a_call(self):
        response = self.client.get('/voice')
        root = self.assertXmlDocument(response.data)
        welcome_text = 'Welcome to the %s survey' % self.survey.title
        self.assertXpathValues(root, './Say/text()', (welcome_text))
