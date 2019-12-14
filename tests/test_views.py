from django.test import TestCase
from django.urls import reverse

from medslist.models import Drug, Doctor, Client, Prescription

class DrugListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        d1 = Drug.objects.create(
            name='paracetamol1', ingredient='paracetamol', use='headache',
            sideeffects='more headaches', particularities='geen')
        d2 = Drug.objects.create(
            name='paracetamol2', ingredient='paracetamol', use='headache',
            sideeffects='more headaches', particularities='geen')
        d3 = Drug.objects.create(
            name='paracetamol3', ingredient='paracetamol', use='headache',
            sideeffects='more headaches', particularities='geen')
           
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/authors/')
        self.assertEqual(response.status_code, 200)
           
    #def test_view_url_accessible_by_name(self):
    #    response = self.client.get(reverse('authors'))
    #    self.assertEqual(response.status_code, 200)
    #    
    #def test_view_uses_correct_template(self):
    #    response = self.client.get(reverse('authors'))
    #    self.assertEqual(response.status_code, 200)
    #    self.assertTemplateUsed(response, 'catalog/author_list.html')
    #    
    #def test_pagination_is_ten(self):
    #    response = self.client.get(reverse('authors'))
    #    self.assertEqual(response.status_code, 200)
    #    self.assertTrue('is_paginated' in response.context)
    #    self.assertTrue(response.context['is_paginated'] == True)
    #    self.assertTrue(len(response.context['author_list']) == 10)
#
#    def test_lists_all_authors(self):
#        # Get second page and confirm it has (exactly) remaining 3 items
#        response = self.client.get(reverse('authors')+'?page=2')
#        self.assertEqual(response.status_code, 200)
#        self.assertTrue('is_paginated' in response.context)
#        self.assertTrue(response.context['is_paginated'] == True)
#        self.assertTrue(len(response.context['author_list']) == 3)
