"""Unit tests for JobApplicationRepository."""
import unittest
import os
from datetime import datetime

from src.models import JobApplication, ApplicationStatus
from src.repositories import JobApplicationRepository


class TestJobApplicationRepository(unittest.TestCase):
    """Test cases for JobApplicationRepository."""
    
    def setUp(self):
        """Set up test database before each test."""
        self.test_db = ":memory:"
        self.repository = JobApplicationRepository(self.test_db)
    
    def test_create_application(self):
        """Test creating an application."""
        app = JobApplication(
            company_name="Tech Corp",
            position="Developer",
            country="USA",
            city="NYC",
            date_applied=datetime.now()
        )
        
        created_app = self.repository.create(app)
        
        self.assertIsNotNone(created_app.id)
        self.assertEqual(created_app.company_name, "Tech Corp")
    
    def test_get_by_id(self):
        """Test retrieving application by ID."""
        app = JobApplication(
            company_name="Tech Corp",
            position="Developer",
            country="USA",
            city="NYC",
            date_applied=datetime.now()
        )
        
        created_app = self.repository.create(app)
        retrieved_app = self.repository.get_by_id(created_app.id)
        
        self.assertIsNotNone(retrieved_app)
        self.assertEqual(retrieved_app.company_name, "Tech Corp")
        self.assertEqual(retrieved_app.position, "Developer")
    
    def test_get_by_id_not_found(self):
        """Test retrieving non-existent application returns None."""
        result = self.repository.get_by_id(999)
        self.assertIsNone(result)
    
    def test_get_all(self):
        """Test retrieving all applications."""
        app1 = JobApplication(
            company_name="Tech Corp",
            position="Developer",
            country="USA",
            city="NYC",
            date_applied=datetime.now()
        )
        
        app2 = JobApplication(
            company_name="StartupXYZ",
            position="Engineer",
            country="Canada",
            city="Toronto",
            date_applied=datetime.now()
        )
        
        self.repository.create(app1)
        self.repository.create(app2)
        
        all_apps = self.repository.get_all()
        
        self.assertEqual(len(all_apps), 2)
    
    def test_update_application(self):
        """Test updating an application."""
        app = JobApplication(
            company_name="Tech Corp",
            position="Developer",
            country="USA",
            city="NYC",
            date_applied=datetime.now()
        )
        
        created_app = self.repository.create(app)
        created_app.position = "Senior Developer"
        
        success = self.repository.update(created_app)
        
        self.assertTrue(success)
        
        updated_app = self.repository.get_by_id(created_app.id)
        self.assertEqual(updated_app.position, "Senior Developer")
    
    def test_delete_application(self):
        """Test deleting an application."""
        app = JobApplication(
            company_name="Tech Corp",
            position="Developer",
            country="USA",
            city="NYC",
            date_applied=datetime.now()
        )
        
        created_app = self.repository.create(app)
        success = self.repository.delete(created_app.id)
        
        self.assertTrue(success)
        
        deleted_app = self.repository.get_by_id(created_app.id)
        self.assertIsNone(deleted_app)
    
    def test_delete_multiple_applications(self):
        """Test deleting multiple applications."""
        app1 = JobApplication(
            company_name="Tech Corp",
            position="Developer",
            country="USA",
            city="NYC",
            date_applied=datetime.now()
        )
        
        app2 = JobApplication(
            company_name="StartupXYZ",
            position="Engineer",
            country="Canada",
            city="Toronto",
            date_applied=datetime.now()
        )
        
        created_app1 = self.repository.create(app1)
        created_app2 = self.repository.create(app2)
        
        success = self.repository.delete_multiple([created_app1.id, created_app2.id])
        
        self.assertTrue(success)
        
        all_apps = self.repository.get_all()
        self.assertEqual(len(all_apps), 0)


if __name__ == '__main__':
    unittest.main()
