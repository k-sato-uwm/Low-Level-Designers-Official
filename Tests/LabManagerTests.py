from django.test import TestCase
from scheduler.models import Lab
from ManagerClasses.LabManager import LabManager

class TestLabManager(TestCase):
    def setUp(self):
        self.mgr = LabManager()

        section1 = Lab(lab_id=11111, section_number='801')
        section1.save()

    def test_createSuccess(self):
        newsect = {'lab_id':22222, 'section_number':'802'}
        res = self.mgr.create(newsect, msg='Create() did not return true!')

        self.assertTrue(res)
        self.assertTrue(Lab.objects.filter(section_number='802'), msg='New lab not in DB!')

    def test_createduplicate(self):
        newsect = {'lab_id':11111, 'section_number':'801'}
        res = self.mgr.create(newsect)

        self.assertFalse(res, msg='Returned true when creating a duplicate!')
        try:
            Lab.objects.get(section_number='802')
            truey = True
        except Lab.MultipleObjectsReturned:
            truey = False
        self.assertTrue(truey, msg='Duplicate object exists in DB!')

    def test_createBadEntry(self):
        newsect = Lab(id=12345, section_num='803')
        res = self.mgr.create(newsect)

        self.assertFalse(res, msg='Returned true with bad entry!')
        with self.assertRaises(Lab.DoesNotExist, msg='Bad entry object exists in DB!'):
            Lab.objects.get(id=12345)

    def test_createBadEntry2(self):
        newsect = {'lab_id': 'Bad data!', 'section_number': '801'}
        res = self.mgr.create(newsect)

        self.assertFalse(res, msg='Returned true with bad entry 2!')
        with self.assertRaises(Lab.DoesNotExist, msg='Bad entry 2 object exists in DB!'):
            Lab.objects.get(id=12345)

    def test_createBadEntry2(self):
        newsect = {'lab_id': 44445, 'section_number': [1,2,3]}
        res = self.mgr.create(newsect)

        self.assertFalse(res, msg='Returned true with bad entry 3!')
        with self.assertRaises(Lab.DoesNotExist, msg='Bad entry 3 object exists in DB!'):
            Lab.objects.get(id=12345)

    def test_view_success(self):
        res = self.mgr.view(11111)
        self.assertEqual(res, {'lab_id':11111, 'section_number':'801'}, msg='Returned wrong lab section info!')

    def test_view_nonexistant_lab(self):
        res = self.mgr.view(12345)
        self.assertIsNone(res, msg='Returned something when it should have returned None')

    def test_view_badinput(self):
        with self.assertRaises(TypeError, msg='Took in bad format input!'):
            self.mgr.view('hello')

    def test_update_success(self):
        res = self.mgr.update(11111, {'section_number':'802'})
        updated = Lab.objects.get(lab_id=11111)

        self.assertTrue(res)
        self.assertEqual(updated, '802', msg='DB does not reflect update!')

    def test_update_nonexistant_lab(self):
        res = self.mgr.update(12345, {'section_number': '802'})

        self.assertFalse(res)
        with self.assertRaises(Lab.DoesNotExist, msg='Somehow updated a nonexisting lab!'):
            Lab.objects.get(lab_id=12345)

    def test_update_badinput(self):
        with self.assertRaises(TypeError, msg='Update took in bad format input!'):
            self.mgr.update('Section 802', {'section_number': '802'})

    def test_delete_success(self):
        res = self.mgr.delete(11111)

        self.assertTrue(res)
        with self.assertRaises(Lab.DoesNotExist, msg='Delete failed!'):
            Lab.objects.get(lab_id=11111)

    def test_delete_nonexistant_lab(self):
        res = self.mgr.delete(12345)

        self.assertFalse(res)

    def test_delete_badinput(self):
        with self.assertRaises(TypeError, msg='Delete took in bad format input!'):
            self.mgr.delete('Section 801')