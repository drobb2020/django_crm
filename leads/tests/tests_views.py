from django.test import TestCase
from django.shortcuts import reverse


class LandingPageTest(TestCase):
  
  def test_get(self):
    # TODO a basic get request test
    response = self.client.get(reverse('landing-page'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'landing.html')
