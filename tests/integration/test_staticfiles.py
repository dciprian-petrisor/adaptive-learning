from django.test import TestCase
import sys
import manage
import http.client


class StaticFilesTestCase(TestCase):
    """
    Verifies if retrieving static files works correctly in production environments through nginx
    """
    original_argv = sys.argv

    @classmethod
    def setUpClass(cls):
        # we need to run collectstatic before this, so nginx has something to serve
        # bypass the command line by replacing the args.
        sys.argv = ["manage.py", "collectstatic", "--noinput"]
        # invoke main to simulate command line call
        manage.main()

    @classmethod
    def tearDownClass(cls):
        # restore original arguments
        sys.argv = cls.original_argv

    def test_get_static_resources(self):
        conn = http.client.HTTPConnection(host="nginx", port=80)
        conn.connect()
        conn.request(method='GET', url="/static/graphene_django/graphiql.js")
        response = conn.getresponse()
        self.assertEqual(200, response.status)
        self.assertNotEqual(len(response.readlines()), 0)