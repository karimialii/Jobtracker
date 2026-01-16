"""Application configuration."""
import os
from dataclasses import dataclass


@dataclass
class AppConfig:
    """
    Application configuration.
    
    Centralized configuration for the Job Tracker application.
    """
    # Application metadata
    APP_NAME: str = "Job Application Tracker"
    APP_VERSION: str = "2.0.0"
    
    # Window settings - Liquid Glass design (borderless, floating)
    WINDOW_WIDTH: int = 1100
    WINDOW_HEIGHT: int = 750
    WINDOW_MIN_WIDTH: int = 900
    WINDOW_MIN_HEIGHT: int = 600
    BORDERLESS: bool = False  # Set to True for production borderless window
    
    # Database settings
    DB_PATH: str = "job_applications.db"
    DB_TEST_PATH: str = ":memory:"
    
    # UI settings - macOS 26 Tahoe Liquid Glass typography
    DEFAULT_FONT: str = ".AppleSystemUIFont"  # SF Pro for body
    HEADER_FONT: str = ".SF Pro Rounded"  # SF Pro Rounded for headers/navigation
    DEFAULT_FONT_SIZE: int = 13
    HEADING_FONT_SIZE: int = 15  # Larger for prominence
    TITLE_FONT_SIZE: int = 17  # Window/section titles
    
    # Icon settings
    ICON_SIZE: tuple = (24, 24)
    DELETE_ICON_PATH: str = "icons/Delete.png"
    NEW_ICON_PATH: str = "icons/New.png"
    
    # Table columns
    TABLE_COLUMNS: tuple = (
        "ID", "Company", "Position", "Country", 
        "City", "Date Applied", "Status", "Notes"
    )
    
    @classmethod
    def get_db_path(cls, test_mode: bool = False) -> str:
        """
        Get database path.
        
        Args:
            test_mode: Whether to use test database
            
        Returns:
            Path to database file
        """
        return cls.DB_TEST_PATH if test_mode else cls.DB_PATH
    
    @classmethod
    def ensure_directories(cls):
        """Ensure required directories exist."""
        directories = ['icons']
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
