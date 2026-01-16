"""Integration tests for the complete application flow."""
import unittest
from datetime import datetime

from src.models import JobApplication, ApplicationStatus
from src.repositories import JobApplicationRepository
from src.services import JobApplicationService
from src.controllers import JobTrackerController
from src.config import ThemeConfig


class TestIntegration(unittest.TestCase):
    """Integration tests for complete application flow."""
    
    def setUp(self):
        """Set up test environment."""
        # Use in-memory database for testing
        self.repository = JobApplicationRepository(":memory:")
        self.service = JobApplicationService(self.repository)
        self.theme_config = ThemeConfig()
        self.controller = JobTrackerController(self.service, self.theme_config)
    
    def test_complete_application_lifecycle(self):
        """Test complete lifecycle: create, read, update, delete."""
        # Create
        success, error = self.controller.create_application(
            company_name="Tech Corp",
            position="Software Engineer",
            country="USA",
            city="San Francisco",
            notes="Great company",
            job_description="Python developer role"
        )
        
        self.assertTrue(success)
        self.assertIsNone(error)
        
        # Read
        apps = self.controller.get_all_applications()
        self.assertEqual(len(apps), 1)
        self.assertEqual(apps[0].company_name, "Tech Corp")
        
        # Update status
        app_id = apps[0].id
        success, error = self.controller.update_status(
            app_id=app_id,
            new_status="invited to interview",
            interview_date="2026-01-20"
        )
        
        self.assertTrue(success)
        self.assertIsNone(error)
        
        # Verify update
        updated_app = self.controller.get_application(app_id)
        self.assertEqual(updated_app.status, ApplicationStatus.INVITED_TO_INTERVIEW)
        self.assertIsNotNone(updated_app.interview_date)
        
        # Delete
        success, error = self.controller.delete_application(app_id)
        self.assertTrue(success)
        
        # Verify deletion
        apps = self.controller.get_all_applications()
        self.assertEqual(len(apps), 0)
    
    def test_multiple_applications_workflow(self):
        """Test workflow with multiple applications."""
        # Create multiple applications
        companies = ["Tech Corp", "StartupXYZ", "BigCorp"]
        
        for company in companies:
            success, _ = self.controller.create_application(
                company_name=company,
                position="Developer",
                country="USA",
                city="NYC"
            )
            self.assertTrue(success)
        
        # Verify all created
        apps = self.controller.get_all_applications()
        self.assertEqual(len(apps), 3)
        
        # Update statuses
        self.controller.update_status(apps[0].id, "rejected")
        self.controller.update_status(apps[1].id, "invited to interview", "2026-01-25")
        
        # Get statistics
        stats = self.controller.get_statistics()
        self.assertEqual(stats['total'], 3)
        self.assertEqual(stats['rejected'], 1)
        self.assertEqual(stats['invited_to_interview'], 1)
        self.assertEqual(stats['applied'], 1)
        
        # Delete multiple
        ids_to_delete = [apps[0].id, apps[1].id]
        success, error = self.controller.delete_multiple_applications(ids_to_delete)
        self.assertTrue(success)
        
        # Verify
        remaining_apps = self.controller.get_all_applications()
        self.assertEqual(len(remaining_apps), 1)
    
    def test_validation_errors(self):
        """Test that validation errors are properly handled."""
        # Empty company name
        success, error = self.controller.create_application(
            company_name="",
            position="Developer",
            country="USA",
            city="NYC"
        )
        
        self.assertFalse(success)
        self.assertIsNotNone(error)
        
        # Empty required fields
        success, error = self.controller.create_application(
            company_name="Tech Corp",
            position="",
            country="USA",
            city="NYC"
        )
        
        self.assertFalse(success)
    
    def test_theme_toggle(self):
        """Test theme toggling functionality."""
        from src.config import Theme
        
        # Initial theme
        initial_theme = self.controller.get_theme_config().current_theme
        self.assertEqual(initial_theme, Theme.LIGHT)
        
        # Toggle
        self.controller.toggle_theme()
        new_theme = self.controller.get_theme_config().current_theme
        self.assertEqual(new_theme, Theme.DARK)
        
        # Toggle back
        self.controller.toggle_theme()
        final_theme = self.controller.get_theme_config().current_theme
        self.assertEqual(final_theme, Theme.LIGHT)


if __name__ == '__main__':
    unittest.main()
