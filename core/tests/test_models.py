from django.test import TestCase
from core.models import Task


class TaskModelTests(TestCase):
    def test_start_processing(self):
        task = Task.objects.create(
            name="Test Task", task_ingestor="Test Ingestor")
        self.assertEqual(task.status, Task.TASK_STATUS_PENDING)

        self.test_start_processing_5(task)
        self.test_start_processing_5(task)

    def test_start_processing_5(self, task):
        self.test_delete_2(task)

    def test_complete_processing(self):
        task = self.test_save_2()
        task.complete_processing()
        self.assertTrue(Task.objects.filter(id=task.id).exists())

        task = Task.objects.create(
            name="Test Task", task_ingestor="Test Ingestor")
        task.complete_processing()
        self.assertTrue(Task.objects.filter(id=task.id).exists())

    def test_fail_processing(self):
        task = Task.objects.create(
            name="Test Task", task_ingestor="Test Ingestor")
        self.assertEqual(task.status, Task.TASK_STATUS_PENDING)

        task.fail_processing()
        task.refresh_from_db()
        self.assertEqual(task.status, Task.TASK_STATUS_PENDING)

        task.start_processing()
        task.fail_processing()
        task.refresh_from_db()
        self.assertEqual(task.status, Task.TASK_STATUS_FAILED)

        task.fail_processing()
        task.refresh_from_db()
        self.assertEqual(task.status, Task.TASK_STATUS_FAILED)

    def test_save(self):
        task = self.test_save_2()
        self.test_save_3(task)
        task = Task.objects.create(
            name="Test Task", task_ingestor="Test Ingestor")
        self.test_save_3(task)

    def test_save_3(self, task):
        task.status = Task.TASK_STATUS_PROCESSED
        task.save()
        self.assertTrue(Task.objects.filter(id=task.id).exists())

    def test_save_2(self):
        result = Task.objects.create(
            name="Test Task", task_ingestor="Test Ingestor")
        self.assertEqual(result.status, Task.TASK_STATUS_PENDING)
        self.test_delete_2(result)
        return result

    def test_delete_2(self, task):
        task.start_processing()
        task.refresh_from_db()
        self.assertEqual(task.status, Task.TASK_STATUS_PROCESSING)
