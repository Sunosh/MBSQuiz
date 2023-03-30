from django.test import TestCase
from .models import Subjects

class SubjectsTestCase(TestCase):
    def setUp(self):
        # Create some subjects with different grade values
        Subjects.objects.create(title='Subject 1', grade=5)
        Subjects.objects.create(title='Subject 2', grade=3)
        Subjects.objects.create(title='Subject 3', grade=8)
        Subjects.objects.create(title='Subject 4', grade=1)
        Subjects.objects.create(title='Subject 5', grade=11)

    def test_subjects_sorted_by_grade(self):
        # Get the sorted queryset of subjects
        subjects_with_grade_1_to_11 = Subjects.objects.filter(grade__gte=1, grade__lte=11).order_by('grade')

        # Check that the queryset is sorted in order from grade 1 to grade 11
        expected_grades = [1, 3, 5, 8, 11]
        actual_grades = list(subjects_with_grade_1_to_11.values_list('grade', flat=True))
        self.assertEqual(actual_grades, expected_grades)

        # Print the test results to the console
        print('Test "test_subjects_sorted_by_grade" passed.')
        print(f'Expected grades: {expected_grades}')
        print(f'Actual grades: {actual_grades}')