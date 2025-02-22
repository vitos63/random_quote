from django.test import SimpleTestCase
from django.core.exceptions import ValidationError
from quotes.validators.author_validator import author_validate
from quotes.validators.category_validator import category_validate


class AuthorValidatorTestCase(SimpleTestCase):

    def test_first_name_and_second_name(self):

        test_name = "Test Name"
        self.assertEqual(author_validate(test_name), None)

    def test_first_name_and_second_name_with_hyphen(self):

        test_name = "Test-Name Second Name"
        self.assertEqual(author_validate(test_name), None)

    def test_too_many_words(self):

        test_name = "First Second Third Fourth"
        with self.assertRaises(ValidationError):
            author_validate(test_name)

    def test_empty_string(self):

        test_name = ""
        with self.assertRaises(ValidationError):
            author_validate(test_name)

    def test_name_with_digits(self):

        test_name = "Test Name1"
        with self.assertRaises(ValidationError):
            author_validate(test_name)

    def test_name_with_some_symbols(self):

        test_name = "Test Name*-"
        with self.assertRaises(ValidationError):
            author_validate(test_name)


class CategoryValidatorTestCase(SimpleTestCase):

    def test_only_one_category(self):
        test_category = "Category"

        self.assertEqual(category_validate(test_category), None)

    def test_two_categories(self):
        test_category = "First Category, SecondCategory"

        self.assertEqual(category_validate(test_category), None)

    def test_seven_categories(self):
        test_category = "First Category, SecondCategory,ThirdCategory, fourth category, f f f, sss, seven"

        self.assertEqual(category_validate(test_category), None)

    def test_eight_categories(self):
        test_category = "First Category, SecondCategory,ThirdCategory, fourth category, f f f, sss, seven, eight, sdf"

        with self.assertRaises(ValidationError):
            category_validate(test_category)

    def test_category_with_digit(self):
        test_category = "First 1"

        with self.assertRaises(ValidationError):
            category_validate(test_category)

    def test_category_with_some_symbols(self):
        test_category = "First +*"

        with self.assertRaises(ValidationError):
            category_validate(test_category)
