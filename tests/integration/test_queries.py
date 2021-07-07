from adaptive_learning.schema import schema
from graphene.test import Client
from unittest import TestCase

class MeQueriesTestCase(TestCase):


   def test_me_al_student_query():
      client = Client(schema)
      result = client.execute('''{ }''')
