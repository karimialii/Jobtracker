"""Job Application Service - Business Logic Layer."""
from datetime import datetime
from typing import List, Optional

from ..models import JobApplication, ApplicationStatus
from ..repositories import IJobApplicationRepository


class JobApplicationService:
    """
    Service layer for JobApplication business logic.
    
    This class contains all business rules and orchestrates
    operations between the UI and data layers. It ensures
    Single Responsibility and Dependency Inversion principles.
    """
    
    def __init__(self, repository: IJobApplicationRepository):
        """
        Initialize service with repository dependency.
        
        Args:
            repository: Repository implementation for data access
        """
        self._repository = repository
    
    def create_application(
        self,
        company_name: str,
        position: str,
        country: str,
        city: str,
        notes: Optional[str] = None,
        job_description: Optional[str] = None
    ) -> JobApplication:
        """
        Create a new job application.
        
        Args:
            company_name: Company name
            position: Job position
            country: Country
            city: City
            notes: Optional notes
            job_description: Optional job description
            
        Returns:
            Created JobApplication entity
            
        Raises:
            ValueError: If validation fails
            Exception: If creation fails
        """
        try:
            # Create entity with business rules validation
            application = JobApplication(
                company_name=company_name.strip(),
                position=position.strip(),
                country=country.strip(),
                city=city.strip(),
                date_applied=datetime.now(),
                status=ApplicationStatus.APPLIED,
                notes=notes.strip() if notes else None,
                job_description=job_description.strip() if job_description else None
            )
            
            # Persist to database
            return self._repository.create(application)
            
        except ValueError as e:
            raise ValueError(f"Validation error: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to create application: {str(e)}")
    
    def get_application(self, app_id: int) -> Optional[JobApplication]:
        """
        Get a job application by ID.
        
        Args:
            app_id: Application ID
            
        Returns:
            JobApplication if found, None otherwise
        """
        return self._repository.get_by_id(app_id)
    
    def get_all_applications(self) -> List[JobApplication]:
        """
        Get all job applications.
        
        Returns:
            List of all JobApplication entities
        """
        return self._repository.get_all()
    
    def update_application_status(
        self,
        app_id: int,
        new_status: ApplicationStatus,
        interview_date: Optional[datetime] = None
    ) -> bool:
        """
        Update the status of a job application.
        
        Args:
            app_id: Application ID
            new_status: New status to set
            interview_date: Optional interview date (required if status is INVITED_TO_INTERVIEW)
            
        Returns:
            True if update successful, False otherwise
            
        Raises:
            ValueError: If application not found or validation fails
        """
        # Retrieve existing application
        application = self._repository.get_by_id(app_id)
        if not application:
            raise ValueError(f"Application with ID {app_id} not found")
        
        # Business rule: If invited to interview, interview date should be provided
        if new_status == ApplicationStatus.INVITED_TO_INTERVIEW and not interview_date:
            # Allow optional interview date
            pass
        
        # Update status using entity method (ensures validation)
        application.update_status(new_status, interview_date)
        
        # Persist changes
        return self._repository.update(application)
    
    def delete_application(self, app_id: int) -> bool:
        """
        Delete a job application.
        
        Args:
            app_id: Application ID to delete
            
        Returns:
            True if deletion successful, False otherwise
        """
        return self._repository.delete(app_id)
    
    def delete_multiple_applications(self, app_ids: List[int]) -> bool:
        """
        Delete multiple job applications.
        
        Args:
            app_ids: List of application IDs to delete
            
        Returns:
            True if all deletions successful, False otherwise
            
        Raises:
            ValueError: If app_ids is empty
        """
        if not app_ids:
            raise ValueError("No application IDs provided for deletion")
        
        return self._repository.delete_multiple(app_ids)
    
    def get_applications_by_status(self, status: ApplicationStatus) -> List[JobApplication]:
        """
        Get all applications with a specific status.
        
        Args:
            status: Status to filter by
            
        Returns:
            List of JobApplication entities with the specified status
        """
        all_applications = self._repository.get_all()
        return [app for app in all_applications if app.status == status]
    
    def get_statistics(self) -> dict:
        """
        Get statistics about job applications.
        
        Returns:
            Dictionary containing application statistics
        """
        applications = self._repository.get_all()
        
        total = len(applications)
        applied = len([app for app in applications if app.status == ApplicationStatus.APPLIED])
        rejected = len([app for app in applications if app.status == ApplicationStatus.REJECTED])
        invited = len([app for app in applications if app.status == ApplicationStatus.INVITED_TO_INTERVIEW])
        
        return {
            'total': total,
            'applied': applied,
            'rejected': rejected,
            'invited_to_interview': invited,
            'rejection_rate': (rejected / total * 100) if total > 0 else 0,
            'interview_rate': (invited / total * 100) if total > 0 else 0
        }
