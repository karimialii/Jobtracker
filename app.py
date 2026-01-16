"""Job Application Tracker - Main Entry Point."""
import sys
import logging
from PyQt5.QtWidgets import QApplication

from src.repositories import JobApplicationRepository
from src.services import JobApplicationService
from src.controllers import JobTrackerController
from src.views import MainWindow
from src.config import AppConfig, ThemeConfig
from src.config.logging_config import setup_logging


def main():
    """
    Main application entry point.
    
    Initializes all layers with proper dependency injection
    following Clean Architecture principles.
    """
    # Setup logging
    log_file = setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("="*60)
    logger.info("Job Tracker Application Starting")
    logger.info(f"Log file: {log_file}")
    logger.info("="*60)
    
    try:
        # Ensure required directories exist
        AppConfig.ensure_directories()
        logger.info("Application directories verified")
    
        # Initialize layers from bottom to top (Dependency Injection)
        # Data Layer
        logger.info(f"Initializing database repository: {AppConfig.DB_PATH}")
        repository = JobApplicationRepository(AppConfig.DB_PATH)
        logger.info("Repository initialized successfully")
        
        # Business Logic Layer
        logger.info("Initializing service layer")
        service = JobApplicationService(repository)
        logger.info("Service layer initialized successfully")
        
        # Configuration
        logger.info("Initializing theme configuration")
        theme_config = ThemeConfig()
        logger.info("Theme configuration initialized successfully")
        
        # Controller Layer
        logger.info("Initializing controller layer")
        controller = JobTrackerController(service, theme_config)
        logger.info("Controller initialized successfully")
        
        # Presentation Layer (PyQt5)
        logger.info("Initializing PyQt5 application")
        app = QApplication(sys.argv)
        logger.info("Creating main window")
        window = MainWindow(controller, AppConfig)
        window.show()
        logger.info("Main window displayed successfully")
        logger.info("Application startup complete - entering event loop")
        
        # Start application
        sys.exit(app.exec_())
        
    except Exception as e:
        logger.critical(f"FATAL ERROR during application startup: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
