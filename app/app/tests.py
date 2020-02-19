from django.test import TestCase

from app.calc import add, subtract


class CalcTests(TestCase):

    def test_add_numbers_equal(self):
        """Test that two numbers are added together"""
        self.assertEqual(add(3, 8), 11)
        self.assertNotEqual(add(3, 1), 5)

    def test_add_numbers_unequal(self):
        """Test that two numbers added together are not another result"""
        self.assertNotEqual(add(3, 1), 5)

    def test_subtract_numbers(self):
        """Test that values are subtracted and returned well"""
        self.assertEqual(subtract(5, 11), 6)
