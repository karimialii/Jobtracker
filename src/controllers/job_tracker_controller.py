"""Job Tracker Controller - UI Logic Layer."""
import logging
from datetime import datetime
from typing import List, Optional

from ..models import JobApplication, ApplicationStatus
from ..services import JobApplicationService
from ..config import ThemeConfig

logger = logging.getLogger(__name__)


class JobTrackerController:
    """
    Controller for Job Tracker application.
    
    Handles user interactions and orchestrates communication
    between the View and Service layers. Follows MVC pattern.
    """
    
    def __init__(self, service: JobApplicationService, theme_config: ThemeConfig):
        """
        Initialize controller with service and theme configuration.
        
        Args:
            service: JobApplicationService instance
            theme_config: ThemeConfig instance
        """
        self._service = service
        self._theme_config = theme_config
    
    def create_application(
        self,
        company_name: str,
        position: str,
        country: str,
        city: str,
        notes: Optional[str] = None,
        job_description: Optional[str] = None
    ) -> tuple[bool, Optional[str]]:
        """
        Handle create application request.
        
        Args:
            company_name: Company name
            position: Job position
            country: Country
            city: City
            notes: Optional notes
            job_description: Optional job description
            
        Returns:
            Tuple of (success: bool, error_message: Optional[str])
        """
        try:
            # Validate inputs
            if not all([company_name, position, country, city]):
                return False, "All required fields must be filled"
            
            # Create application through service
            self._service.create_application(
                company_name=company_name,
                position=position,
                country=country,
                city=city,
                notes=notes,
                job_description=job_description
            )
            
            return True, None
            
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"An unexpected error occurred: {str(e)}"
    
    def get_all_applications(self) -> List[JobApplication]:
        """
        Get all job applications.
        
        Returns:
            List of JobApplication entities
        """
        return self._service.get_all_applications()
    
    def get_application(self, app_id: int) -> Optional[JobApplication]:
        """
        Get a specific application by ID.
        
        Args:
            app_id: Application ID
            
        Returns:
            JobApplication if found, None otherwise
        """
        return self._service.get_application(app_id)
    
    def update_status(
        self,
        app_id: int,
        new_status: str,
        interview_date: Optional[str] = None
    ) -> tuple[bool, Optional[str]]:
        """
        Handle update status request.
        
        Args:
            app_id: Application ID
            new_status: New status string
            interview_date: Optional interview date string (YYYY-MM-DD)
            
        Returns:
            Tuple of (success: bool, error_message: Optional[str])
        """
        try:
            # Convert status string to enum
            status = ApplicationStatus.from_string(new_status)
            
            # Parse interview date if provided
            parsed_date = None
            if interview_date:
                try:
                    parsed_date = datetime.strptime(interview_date, '%Y-%m-%d')
                except ValueError:
                    return False, "Invalid interview date format. Use YYYY-MM-DD"
            
            # Update through service
            success = self._service.update_application_status(
                app_id=app_id,
                new_status=status,
                interview_date=parsed_date
            )
            
            if success:
                return True, None
            else:
                return False, "Failed to update status"
                
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"An unexpected error occurred: {str(e)}"
    
    def delete_application(self, app_id: int) -> tuple[bool, Optional[str]]:
        """
        Handle delete application request.
        
        Args:
            app_id: Application ID to delete
            
        Returns:
            Tuple of (success: bool, error_message: Optional[str])
        """
        try:
            success = self._service.delete_application(app_id)
            
            if success:
                return True, None
            else:
                return False, "Failed to delete application"
                
        except Exception as e:
            return False, f"An unexpected error occurred: {str(e)}"
    
    def delete_multiple_applications(self, app_ids: List[int]) -> tuple[bool, Optional[str]]:
        """
        Handle delete multiple applications request.
        
        Args:
            app_ids: List of application IDs to delete
            
        Returns:
            Tuple of (success: bool, error_message: Optional[str])
        """
        try:
            if not app_ids:
                return False, "No applications selected"
            
            success = self._service.delete_multiple_applications(app_ids)
            
            if success:
                return True, None
            else:
                return False, "Failed to delete applications"
                
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"An unexpected error occurred: {str(e)}"
    
    def toggle_theme(self):
        """Toggle application theme."""
        self._theme_config.toggle_theme()
    
    def get_theme_config(self) -> ThemeConfig:
        """Get theme configuration."""
        return self._theme_config
    
    def get_statistics(self) -> dict:
        """
        Get application statistics.
        
        Returns:
            Dictionary containing statistics
        """
        return self._service.get_statistics()
