"""Unit tests for JobApplication model."""
import unittest
from datetime import datetime, timedelta

from src.models import JobApplication, ApplicationStatus


class TestJobApplication(unittest.TestCase):
    """Test cases for JobApplication entity."""
    
    def test_create_valid_application(self):
        """Test creating a valid job application."""
        app = JobApplication(
            company_name="Tech Corp",
            position="Software Engineer",
            country="USA",
            city="San Francisco",
            date_applied=datetime.now()
        )
        
        self.assertEqual(app.company_name, "Tech Corp")
        self.assertEqual(app.position, "Software Engineer")
        self.assertEqual(app.status, ApplicationStatus.APPLIED)
        self.assertIsNone(app.interview_date)
    
    def test_empty_company_name_raises_error(self):
        """Test that empty company name raises ValueError."""
        with self.assertRaises(ValueError) as context:
            JobApplication(
                company_name="",
                position="Developer",
                country="USA",
                city="NYC",
                date_applied=datetime.now()
            )
        
        self.assertIn("Company name cannot be empty", str(context.exception))
    
    def test_empty_position_raises_error(self):
        """Test that empty position raises ValueError."""
        with self.assertRaises(ValueError):
            JobApplication(
                company_name="Tech Corp",
                position="",
                country="USA",
                city="NYC",
                date_applied=datetime.now()
            )
    
    def test_future_date_raises_error(self):
        """Test that future application date raises ValueError."""
        future_date = datetime.now() + timedelta(days=1)
        
        with self.assertRaises(ValueError) as context:
            JobApplication(
                company_name="Tech Corp",
                position="Developer",
                country="USA",
                city="NYC",
                date_applied=future_date
            )
        
        self.assertIn("cannot be in the future", str(context.exception))
    
    def test_interview_date_before_application_date_raises_error(self):
        """Test that interview date before application date raises ValueError."""
        app_date = datetime.now()
        interview_date = app_date - timedelta(days=1)
        
        with self.assertRaises(ValueError):
            JobApplication(
                company_name="Tech Corp",
                position="Developer",
                country="USA",
                city="NYC",
                date_applied=app_date,
                interview_date=interview_date
            )
    
    def test_update_status_to_invited(self):
        """Test updating status to invited to interview."""
        app = JobApplication(
            company_name="Tech Corp",
            position="Developer",
            country="USA",
            city="NYC",
            date_applied=datetime.now()
        )
        
        interview_date = datetime.now() + timedelta(days=7)
        app.update_status(ApplicationStatus.INVITED_TO_INTERVIEW, interview_date)
        
        self.assertEqual(app.status, ApplicationStatus.INVITED_TO_INTERVIEW)
        self.assertEqual(app.interview_date, interview_date)
    
    def test_update_status_to_rejected_clears_interview_date(self):
        """Test that updating status to rejected clears interview date."""
        app = JobApplication(
            company_name="Tech Corp",
            position="Developer",
            country="USA",
            city="NYC",
            date_applied=datetime.now(),
            status=ApplicationStatus.INVITED_TO_INTERVIEW,
            interview_date=datetime.now() + timedelta(days=7)
        )
        
        app.update_status(ApplicationStatus.REJECTED)
        
        self.assertEqual(app.status, ApplicationStatus.REJECTED)
        self.assertIsNone(app.interview_date)
    
    def test_to_dict(self):
        """Test converting application to dictionary."""
        app_date = datetime(2026, 1, 15)
        app = JobApplication(
            id=1,
            company_name="Tech Corp",
            position="Developer",
            country="USA",
            city="NYC",
            date_applied=app_date,
            status=ApplicationStatus.APPLIED,
            notes="Test notes"
        )
        
        result = app.to_dict()
        
        self.assertEqual(result['id'], 1)
        self.assertEqual(result['company_name'], "Tech Corp")
        self.assertEqual(result['date_applied'], "2026-01-15")
        self.assertEqual(result['status'], "applied")
    
    def test_from_dict(self):
        """Test creating application from dictionary."""
        data = {
            'id': 1,
            'company_name': 'Tech Corp',
            'position': 'Developer',
            'country': 'USA',
            'city': 'NYC',
            'date_applied': '2026-01-15',
            'status': 'applied',
            'interview_date': None,
            'notes': 'Test notes',
            'job_description': 'Great job'
        }
        
        app = JobApplication.from_dict(data)
        
        self.assertEqual(app.id, 1)
        self.assertEqual(app.company_name, 'Tech Corp')
        self.assertEqual(app.status, ApplicationStatus.APPLIED)
        self.assertEqual(app.date_applied.year, 2026)


if __name__ == '__main__':
    unittest.main()
