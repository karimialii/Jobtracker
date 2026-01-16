"""Job Application Repository - Data Access Layer."""
import sqlite3
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from ..models import JobApplication, ApplicationStatus


class IJobApplicationRepository(ABC):
    """Interface for JobApplication repository following Repository Pattern."""
    
    @abstractmethod
    def create(self, application: JobApplication) -> JobApplication:
        """Create a new job application."""
        pass
    
    @abstractmethod
    def get_by_id(self, app_id: int) -> Optional[JobApplication]:
        """Get a job application by ID."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[JobApplication]:
        """Get all job applications."""
        pass
    
    @abstractmethod
    def update(self, application: JobApplication) -> bool:
        """Update an existing job application."""
        pass
    
    @abstractmethod
    def delete(self, app_id: int) -> bool:
        """Delete a job application by ID."""
        pass
    
    @abstractmethod
    def delete_multiple(self, app_ids: List[int]) -> bool:
        """Delete multiple job applications."""
        pass


class JobApplicationRepository(IJobApplicationRepository):
    """
    SQLite implementation of JobApplication repository.
    
    Encapsulates all database operations and provides abstraction
    over the data access layer.
    """
    
    def __init__(self, db_path: str = 'job_applications.db'):
        """
        Initialize repository with database connection.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._conn = None
        if db_path == ":memory:":
            # For in-memory databases, maintain a persistent connection
            self._conn = sqlite3.connect(db_path)
            self._conn.row_factory = sqlite3.Row
        self._initialize_database()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection."""
        if self._conn:
            return self._conn
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _initialize_database(self):
        """Initialize database schema."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT NOT NULL,
                position TEXT NOT NULL,
                country TEXT NOT NULL,
                city TEXT NOT NULL,
                date_applied TEXT NOT NULL,
                status TEXT CHECK(status IN ('applied', 'rejected', 'invited to interview')) DEFAULT 'applied',
                interview_date TEXT,
                notes TEXT,
                job_description TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        if not self._conn:
            conn.close()
    
    def create(self, application: JobApplication) -> JobApplication:
        """
        Create a new job application.
        
        Args:
            application: JobApplication entity to create
            
        Returns:
            JobApplication with populated ID
            
        Raises:
            sqlite3.Error: If database operation fails
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO applications 
                (company_name, position, country, city, date_applied, status, interview_date, notes, job_description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                application.company_name,
                application.position,
                application.country,
                application.city,
                application.date_applied.strftime('%Y-%m-%d'),
                application.status.value,
                application.interview_date.strftime('%Y-%m-%d') if application.interview_date else None,
                application.notes,
                application.job_description
            ))
            conn.commit()
            application.id = cursor.lastrowid
            return application
        except sqlite3.Error as e:
            raise Exception(f"Failed to create application: {str(e)}")
        finally:
            if not self._conn:
                conn.close()
    
    def get_by_id(self, app_id: int) -> Optional[JobApplication]:
        """
        Get a job application by ID.
        
        Args:
            app_id: Application ID
            
        Returns:
            JobApplication if found, None otherwise
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM applications WHERE id = ?', (app_id,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_entity(row)
            return None
        finally:
            if not self._conn:
                conn.close()
    
    def get_all(self) -> List[JobApplication]:
        """
        Get all job applications.
        
        Returns:
            List of all JobApplication entities
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM applications ORDER BY date_applied DESC')
            rows = cursor.fetchall()
            return [self._row_to_entity(row) for row in rows]
        finally:
            if not self._conn:
                conn.close()
    
    def update(self, application: JobApplication) -> bool:
        """
        Update an existing job application.
        
        Args:
            application: JobApplication entity with updated data
            
        Returns:
            True if update successful, False otherwise
        """
        if not application.id:
            raise ValueError("Application ID is required for update")
        
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE applications
                SET company_name = ?, position = ?, country = ?, city = ?,
                    date_applied = ?, status = ?, interview_date = ?,
                    notes = ?, job_description = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (
                application.company_name,
                application.position,
                application.country,
                application.city,
                application.date_applied.strftime('%Y-%m-%d'),
                application.status.value,
                application.interview_date.strftime('%Y-%m-%d') if application.interview_date else None,
                application.notes,
                application.job_description,
                application.id
            ))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error:
            return False
        finally:
            if not self._conn:
                conn.close()
    
    def delete(self, app_id: int) -> bool:
        """
        Delete a job application by ID.
        
        Args:
            app_id: Application ID to delete
            
        Returns:
            True if deletion successful, False otherwise
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM applications WHERE id = ?', (app_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            if not self._conn:
                conn.close()
    
    def delete_multiple(self, app_ids: List[int]) -> bool:
        """
        Delete multiple job applications.
        
        Args:
            app_ids: List of application IDs to delete
            
        Returns:
            True if all deletions successful, False otherwise
        """
        if not app_ids:
            return False
        
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            placeholders = ','.join('?' * len(app_ids))
            cursor.execute(f'DELETE FROM applications WHERE id IN ({placeholders})', app_ids)
            conn.commit()
            return cursor.rowcount > 0
        finally:
            if not self._conn:
                conn.close()
    
    def _row_to_entity(self, row: sqlite3.Row) -> JobApplication:
        """
        Convert database row to JobApplication entity.
        
        Args:
            row: Database row
            
        Returns:
            JobApplication entity
        """
        return JobApplication(
            id=row['id'],
            company_name=row['company_name'],
            position=row['position'],
            country=row['country'],
            city=row['city'],
            date_applied=datetime.strptime(row['date_applied'], '%Y-%m-%d'),
            status=ApplicationStatus.from_string(row['status']),
            interview_date=datetime.strptime(row['interview_date'], '%Y-%m-%d') if row['interview_date'] else None,
            notes=row['notes'],
            job_description=row['job_description']
        )
