from flask_testing import TestCase
from main import app
from flask import current_app, url_for


class MainTest(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def test_app_exists(self):
        self.assertIsNotNone(current_app)

    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_index_redirects(self):
        response = self.client.get(url_for('index'))
        self.assertRedirects(response, url_for('hello_world'))

    def test_hello_get(self):
        response = self.client.get(url_for('hello_world'))
        self.assert200(response)

    def test_hello_post(self):
        fake_user = {
            'username': 'jumar98',
            'password': '123456'
        }
        response = self.client.post(url_for('hello_world'), data=fake_user)
        self.assertRedirects(response, url_for('index'))
