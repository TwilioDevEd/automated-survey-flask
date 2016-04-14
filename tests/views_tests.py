from .base import BaseTest


class RootTest(BaseTest):

    def test_renders_all_questions(self):
        response = self.client.get('/')
        for question in self.questions:
            self.assertIn(question.content, response.data.decode('utf8'))
