from django.test import TestCase
from core.models import Task

class TaskTestCase(TestCase):

    def test_task_creation(self):
        task = Task.objects.create(name="Test Task", task_ingestor="Test Ingestor")
        self.assertTrue(isinstance(task, Task))
        self.assertEqual(task.name, "Test Task")
        self.assertEqual(task.task_ingestor, "Test Ingestor")
        self.assertEqual(task.status, Task.TASK_STATUS_PENDING)

    def test_task_processing(self):
        # Create a task with status 'pending'
        task = Task.objects.create(name="Test Task", task_ingestor="Test Ingestor")
        
    def test_task_failed_processing(self):
        task = Task.objects.create(name="Test Task", task_ingestor="Test Ingestor")
        self.assertEqual(task.status, Task.TASK_STATUS_PENDING)
        task.start_processing()
        self.assertEqual(task.status, Task.TASK_STATUS_PROCESSING)
        task.fail_processing()
        self.assertEqual(task.status, Task.TASK_STATUS_FAILED)

    def test_task_deletion(self):
        # Create a task with status 'processed'
        task = Task.objects.create(name="Test Task", task_ingestor="Test Ingestor", status=Task.TASK_STATUS_PROCESSED)
        task.delete()
        # Check that the task has been deleted from the database
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())

        # Create a task with status 'processing' and fail the processing
        task = Task.objects.create(name="Test Task", task_ingestor="Test Ingestor")
        task.start_processing()
        task.fail_processing()
        task.delete()
        # Check that the task has not been deleted from the database
        self.assertTrue(Task.objects.filter(pk=task.pk).exists())
        # Check that the status of the task is 'failed'
        self.assertEqual(Task.objects.get(pk=task.pk).status, Task.TASK_STATUS_FAILED)
