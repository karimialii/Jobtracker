"""Unit tests for JobApplicationService."""
import unittest
from datetime import datetime, timedelta
from unittest.mock import Mock, MagicMock

from src.models import JobApplication, ApplicationStatus
from src.services import JobApplicationService


class TestJobApplicationService(unittest.TestCase):
    """Test cases for JobApplicationService."""
    
    def setUp(self):
        """Set up test dependencies before each test."""
        self.mock_repository = Mock()
        self.service = JobApplicationService(self.mock_repository)
    
    def test_create_application_success(self):
        """Test successful application creation."""
        # Setup mock
        created_app = JobApplication(
            id=1,
            company_name="Tech Corp",
            position="Developer",
            country="USA",
            city="NYC",
            date_applied=datetime.now()
        )
        self.mock_repository.create.return_value = created_app
        
        # Execute
        result = self.service.create_application(
            company_name="Tech Corp",
            position="Developer",
            country="USA",
            city="NYC"
        )
        
        # Verify
        self.assertEqual(result.company_name, "Tech Corp")
        self.mock_repository.create.assert_called_once()
    
    def test_create_application_with_empty_company_raises_error(self):
        """Test that empty company name raises ValueError."""
        with self.assertRaises(ValueError):
            self.service.create_application(
                company_name="",
                position="Developer",
                country="USA",
                city="NYC"
            )
    
    def test_get_application(self):
        """Test getting an application by ID."""
        app = JobApplication(
            id=1,
            company_name="Tech Corp",
            position="Developer",
            country="USA",
            city="NYC",
            date_applied=datetime.now()
        )
        self.mock_repository.get_by_id.return_value = app
        
        result = self.service.get_application(1)
        
        self.assertEqual(result.id, 1)
        self.mock_repository.get_by_id.assert_called_once_with(1)
    
    def test_get_all_applications(self):
        """Test getting all applications."""
        apps = [
            JobApplication(
                id=1,
                company_name="Tech Corp",
                position="Developer",
                country="USA",
                city="NYC",
                date_applied=datetime.now()
            ),
            JobApplication(
                id=2,
                company_name="StartupXYZ",
                position="Engineer",
                country="Canada",
                city="Toronto",
                date_applied=datetime.now()
            )
        ]
        self.mock_repository.get_all.return_value = apps
        
        result = self.service.get_all_applications()
        
        self.assertEqual(len(result), 2)
        self.mock_repository.get_all.assert_called_once()
    
    def test_update_application_status(self):
        """Test updating application status."""
        app = JobApplication(
            id=1,
            company_name="Tech Corp",
            position="Developer",
            country="USA",
            city="NYC",
            date_applied=datetime.now()
        )
        self.mock_repository.get_by_id.return_value = app
        self.mock_repository.update.return_value = True
        
        interview_date = datetime.now() + timedelta(days=7)
        success = self.service.update_application_status(
            app_id=1,
            new_status=ApplicationStatus.INVITED_TO_INTERVIEW,
            interview_date=interview_date
        )
        
        self.assertTrue(success)
        self.mock_repository.update.assert_called_once()
    
    def test_update_status_application_not_found(self):
        """Test updating status for non-existent application raises error."""
        self.mock_repository.get_by_id.return_value = None
        
        with self.assertRaises(ValueError) as context:
            self.service.update_application_status(
                app_id=999,
                new_status=ApplicationStatus.REJECTED
            )
        
        self.assertIn("not found", str(context.exception))
    
    def test_delete_application(self):
        """Test deleting an application."""
        self.mock_repository.delete.return_value = True
        
        success = self.service.delete_application(1)
        
        self.assertTrue(success)
        self.mock_repository.delete.assert_called_once_with(1)
    
    def test_delete_multiple_applications(self):
        """Test deleting multiple applications."""
        self.mock_repository.delete_multiple.return_value = True
        
        success = self.service.delete_multiple_applications([1, 2, 3])
        
        self.assertTrue(success)
        self.mock_repository.delete_multiple.assert_called_once_with([1, 2, 3])
    
    def test_delete_multiple_with_empty_list_raises_error(self):
        """Test that deleting with empty list raises ValueError."""
        with self.assertRaises(ValueError):
            self.service.delete_multiple_applications([])
    
    def test_get_applications_by_status(self):
        """Test getting applications by status."""
        apps = [
            JobApplication(
                id=1,
                company_name="Tech Corp",
                position="Developer",
                country="USA",
                city="NYC",
                date_applied=datetime.now(),
                status=ApplicationStatus.APPLIED
            ),
            JobApplication(
                id=2,
                company_name="StartupXYZ",
                position="Engineer",
                country="Canada",
                city="Toronto",
                date_applied=datetime.now(),
                status=ApplicationStatus.REJECTED
            )
        ]
        self.mock_repository.get_all.return_value = apps
        
        result = self.service.get_applications_by_status(ApplicationStatus.APPLIED)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].status, ApplicationStatus.APPLIED)
    
    def test_get_statistics(self):
        """Test getting statistics."""
        apps = [
            JobApplication(
                id=1,
                company_name="Tech Corp",
                position="Developer",
                country="USA",
                city="NYC",
                date_applied=datetime.now(),
                status=ApplicationStatus.APPLIED
            ),
            JobApplication(
                id=2,
                company_name="StartupXYZ",
                position="Engineer",
                country="Canada",
                city="Toronto",
                date_applied=datetime.now(),
                status=ApplicationStatus.REJECTED
            ),
            JobApplication(
                id=3,
                company_name="BigCorp",
                position="Dev",
                country="USA",
                city="LA",
                date_applied=datetime.now(),
                status=ApplicationStatus.INVITED_TO_INTERVIEW
            )
        ]
        self.mock_repository.get_all.return_value = apps
        
        stats = self.service.get_statistics()
        
        self.assertEqual(stats['total'], 3)
        self.assertEqual(stats['applied'], 1)
        self.assertEqual(stats['rejected'], 1)
        self.assertEqual(stats['invited_to_interview'], 1)


if __name__ == '__main__':
    unittest.main()
