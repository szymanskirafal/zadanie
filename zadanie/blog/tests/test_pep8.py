from django.test import TestCase

import pycodestyle


class TestCodeFormat(TestCase):

    def test_style(self):
        list_of_error_codes_to_ignore = ['E251']
        style = pycodestyle.StyleGuide(
            ignore = list_of_error_codes_to_ignore,
            quiet = True,
        )
        list_of_files = [
            'blog.admin.py',
            'blog.apps.py',
            'blog.forms.py',
            'blog.models.py',
            'blog.urls.py',
            'blog.views.py',
        ]
        result = style.check_files(list_of_files)
        number_of_errors_expected = 0
        number_of_errors_given = result.total_errors
        self.assertEqual(number_of_errors_expected, number_of_errors_given)
