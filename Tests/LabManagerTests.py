from django.test import TestCase
from scheduler.models import Lab
from ManagerClasses.LabManager import LabManager

class TestLabManager(TestCase):
    def setUp(self):
        self.mgr = LabManager()
        Lab.objects.create(lab_id=11111, section_number='801')

    def test_createSuccess(self):
        newsect = {'lab_id': 22222, 'section_number': '802'}
        res = self.mgr.create(newsect)
        self.assertTrue(res)
        self.assertTrue(Lab.objects.filter(section_number='802').exists())

    def test_createduplicate(self):
        newsect = {'lab_id': 11111, 'section_number': '801'}
        res = self.mgr.create(newsect)
        self.assertFalse(res)

    def test_createBadEntry(self):
        newsect = {'lab_id': 'Invalid', 'section_number': '803'}
        res = self.mgr.create(newsect)
        self.assertFalse(res)

    def test_createBadEntry2(self):
        newsect = {'lab_id': 44445, 'section_number': [1, 2, 3]}
        res = self.mgr.create(newsect)
        self.assertFalse(res)

    def test_view_success(self):
        res = self.mgr.view(11111)
        self.assertEqual(res, {'lab_id': 11111, 'section_number': '801'})

    def test_view_nonexistant_lab(self):
        res = self.mgr.view(12345)
        self.assertIsNone(res)

    def test_view_badinput(self):
        with self.assertRaises(TypeError):
            self.mgr.view('hello')

    def test_update_success(self):
        res = self.mgr.update(11111, {'section_number': '802'})
        self.assertTrue(res)
        updated = Lab.objects.get(lab_id=11111)
        self.assertEqual(updated.section_number, '802')

    def test_update_nonexistant_lab(self):
        res = self.mgr.update(12345, {'section_number': '802'})
        self.assertFalse(res)

    def test_update_badinput(self):
        with self.assertRaises(TypeError):
            self.mgr.update('InvalidID', {'section_number': '802'})

    def test_delete_success(self):
        res = self.mgr.delete(11111)
        self.assertTrue(res)
        with self.assertRaises(Lab.DoesNotExist):
            Lab.objects.get(lab_id=11111)

    def test_delete_nonexistant_lab(self):
        res = self.mgr.delete(12345)
        self.assertFalse(res)

    def test_delete_badinput(self):
        with self.assertRaises(TypeError):
            self.mgr.delete('InvalidID')
