"""JobApplication entity model with validation."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class ApplicationStatus(Enum):
    """Enum for application status values."""
    APPLIED = "applied"
    REJECTED = "rejected"
    INVITED_TO_INTERVIEW = "invited to interview"
    
    @classmethod
    def from_string(cls, status: str) -> 'ApplicationStatus':
        """Convert string to ApplicationStatus."""
        status_map = {
            "applied": cls.APPLIED,
            "rejected": cls.REJECTED,
            "invited to interview": cls.INVITED_TO_INTERVIEW
        }
        return status_map.get(status.lower(), cls.APPLIED)


@dataclass
class JobApplication:
    """
    JobApplication entity representing a job application record.
    
    This is the domain model that encapsulates all business rules
    related to a job application.
    """
    company_name: str
    position: str
    country: str
    city: str
    date_applied: datetime
    status: ApplicationStatus = field(default=ApplicationStatus.APPLIED)
    id: Optional[int] = None
    interview_date: Optional[datetime] = None
    notes: Optional[str] = None
    job_description: Optional[str] = None
    
    def __post_init__(self):
        """Validate entity after initialization."""
        self._validate()
    
    def _validate(self):
        """Validate the job application data."""
        # For existing records from legacy database, be more lenient
        if self.id is None:  # Only enforce strict validation on new records
            if not self.company_name or not self.company_name.strip():
                raise ValueError("Company name cannot be empty")
            
            if not self.position or not self.position.strip():
                raise ValueError("Position cannot be empty")
            
            if not self.country or not self.country.strip():
                raise ValueError("Country cannot be empty")
            
            if not self.city or not self.city.strip():
                raise ValueError("City cannot be empty")
        
        if self.date_applied > datetime.now():
            raise ValueError("Date applied cannot be in the future")
        
        if self.status == ApplicationStatus.INVITED_TO_INTERVIEW and not self.interview_date:
            # Interview date is optional even for invited status
            pass
        
        if self.interview_date and self.interview_date < self.date_applied:
            raise ValueError("Interview date cannot be before application date")
    
    def update_status(self, new_status: ApplicationStatus, interview_date: Optional[datetime] = None):
        """
        Update the application status.
        
        Args:
            new_status: The new status to set
            interview_date: Optional interview date (required if status is INVITED_TO_INTERVIEW)
        
        Raises:
            ValueError: If validation fails
        """
        self.status = new_status
        if new_status == ApplicationStatus.INVITED_TO_INTERVIEW:
            self.interview_date = interview_date
        else:
            self.interview_date = None
        
        self._validate()
    
    def to_dict(self) -> dict:
        """Convert entity to dictionary representation."""
        return {
            'id': self.id,
            'company_name': self.company_name,
            'position': self.position,
            'country': self.country,
            'city': self.city,
            'date_applied': self.date_applied.strftime('%Y-%m-%d'),
            'status': self.status.value,
            'interview_date': self.interview_date.strftime('%Y-%m-%d') if self.interview_date else None,
            'notes': self.notes,
            'job_description': self.job_description
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'JobApplication':
        """Create JobApplication from dictionary."""
        date_applied = data['date_applied']
        if isinstance(date_applied, str):
            date_applied = datetime.strptime(date_applied, '%Y-%m-%d')
        
        interview_date = data.get('interview_date')
        if interview_date and isinstance(interview_date, str):
            interview_date = datetime.strptime(interview_date, '%Y-%m-%d')
        
        status = data.get('status', 'applied')
        if isinstance(status, str):
            status = ApplicationStatus.from_string(status)
        
        return cls(
            id=data.get('id'),
            company_name=data['company_name'],
            position=data['position'],
            country=data['country'],
            city=data['city'],
            date_applied=date_applied,
            status=status,
            interview_date=interview_date,
            notes=data.get('notes'),
            job_description=data.get('job_description')
        )
