"""Main window view for Job Tracker application using PyQt5."""
import logging
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QDialog, QLabel, QLineEdit,
    QTextEdit, QComboBox, QMessageBox, QHeaderView, QAbstractItemView
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont, QColor
from datetime import datetime
from typing import Optional

from ..controllers import JobTrackerController
from ..config import AppConfig

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """
    Main window view for Job Tracker application.
    
    Handles all UI rendering and user interactions using PyQt5.
    Delegates business logic to the controller.
    """
    
    def __init__(self, controller: JobTrackerController, config: AppConfig):
        """
        Initialize main window.
        
        Args:
            controller: JobTrackerController instance
            config: AppConfig instance
        """
        super().__init__()
        logger.info("Initializing main window")
        self.controller = controller
        self.config = config
        self.theme_config = controller.get_theme_config()
        
        # Setup window
        logger.debug("Setting up window")
        self._setup_window()
        
        # Create widgets
        logger.debug("Creating widgets")
        self._create_widgets()
        
        # Apply initial theme
        logger.debug("Applying theme")
        self._apply_theme()
        
        # Load data
        logger.debug("Loading initial data")
        self.refresh_table()
        logger.info("Main window initialization complete")
    
    def _setup_window(self):
        """Setup main window properties."""
        self.setWindowTitle(self.config.APP_NAME)
        self.setGeometry(100, 100, self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT)
        self.setMinimumSize(self.config.WINDOW_MIN_WIDTH, self.config.WINDOW_MIN_HEIGHT)
    
    def _create_widgets(self):
        """Create all UI widgets."""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # Create buttons
        self.add_button = QPushButton("Add Application")
        self.add_button.clicked.connect(self._show_new_application_dialog)
        self.add_button.setMinimumHeight(40)
        
        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.clicked.connect(self._delete_selected)
        self.delete_button.setMinimumHeight(40)
        
        self.toggle_theme_button = QPushButton("Toggle Theme")
        self.toggle_theme_button.clicked.connect(self._toggle_theme)
        self.toggle_theme_button.setMinimumHeight(40)
        
        # Add buttons to layout
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addStretch()
        button_layout.addWidget(self.toggle_theme_button)
        
        # Create table
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.config.TABLE_COLUMNS))
        self.table.setHorizontalHeaderLabels(self.config.TABLE_COLUMNS)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.doubleClicked.connect(self._on_double_click)
        
        # Add widgets to main layout
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)
    
    def _apply_theme(self):
        """Apply current theme to all widgets."""
        colors = self.theme_config.get_colors()
        
        # Build stylesheet
        stylesheet = f"""
            QMainWindow {{
                background-color: {colors.bg};
            }}
            QWidget {{
                background-color: {colors.bg};
                color: {colors.fg};
                font-family: {self.config.DEFAULT_FONT};
                font-size: {self.config.DEFAULT_FONT_SIZE}px;
            }}
            QPushButton {{
                background-color: {colors.button_bg};
                color: {colors.button_fg};
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {colors.button_bg};
                opacity: 0.8;
            }}
            QPushButton:pressed {{
                background-color: {colors.button_bg};
            }}
            QPushButton#secondary {{
                background-color: {colors.header_bg};
                color: {colors.fg};
            }}
            QTableWidget {{
                background-color: {colors.tree_bg};
                color: {colors.tree_fg};
                border: 1px solid {colors.header_bg};
                border-radius: 8px;
                gridline-color: {colors.header_bg};
            }}
            QTableWidget::item {{
                padding: 8px;
            }}
            QTableWidget::item:selected {{
                background-color: {colors.button_bg};
                color: {colors.button_fg};
            }}
            QHeaderView::section {{
                background-color: {colors.header_bg};
                color: {colors.header_fg};
                padding: 8px;
                border: none;
                font-weight: bold;
            }}
            QLineEdit, QTextEdit, QComboBox {{
                background-color: {colors.entry_bg};
                color: {colors.fg};
                border: 1px solid {colors.header_bg};
                border-radius: 4px;
                padding: 8px;
            }}
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
                border: 2px solid {colors.button_bg};
            }}
            QLabel {{
                color: {colors.fg};
            }}
            QDialog {{
                background-color: {colors.bg};
            }}
        """
        
        self.setStyleSheet(stylesheet)
        
        # Refresh table to apply status colors
        self.refresh_table()
    
    def _toggle_theme(self):
        """Toggle application theme."""
        logger.info("User clicked 'Toggle Theme' button")
        self.controller.toggle_theme()
        self._apply_theme()
        logger.info(f"Theme toggled to: {self.theme_config.current_theme.value}")
    
    def refresh_table(self):
        """Refresh the applications table."""
        logger.debug("Refreshing table data")
        # Clear existing items
        self.table.setRowCount(0)
        
        # Get applications from controller
        applications = self.controller.get_all_applications()
        logger.info(f"Loaded {len(applications)} applications from database")
        
        # Insert applications
        for row, app in enumerate(applications):
            self.table.insertRow(row)
            
            values = [
                str(app.id),
                app.company_name,
                app.position,
                app.country,
                app.city,
                app.date_applied.strftime('%Y-%m-%d'),
                app.status.value,
                app.notes or ""
            ]
            
            for col, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                
                # Apply status color
                if col == 6:  # Status column
                    status_color = self.theme_config.get_status_color(app.status.value)
                    item.setBackground(QColor(status_color))
                
                self.table.setItem(row, col, item)
    
    def _show_new_application_dialog(self):
        """Show dialog for creating new application."""
        logger.info("User clicked 'Add Application' button")
        dialog = QDialog(self)
        dialog.setWindowTitle("New Application")
        dialog.setFixedSize(600, 650)
        
        colors = self.theme_config.get_colors()
        dialog.setStyleSheet(f"QDialog {{ background-color: {colors.bg}; }}")
        
        # Layout
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)
        
        # Title
        title = QLabel("New Job Application")
        title_font = QFont(self.config.DEFAULT_FONT, 16, QFont.Bold)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Form fields
        fields = {}
        field_names = ["Company Name", "Position", "Country", "City", "Notes", "Job Description"]
        
        for field_name in field_names:
            label = QLabel(field_name)
            label_font = QFont(self.config.DEFAULT_FONT, self.config.DEFAULT_FONT_SIZE, QFont.Bold)
            label.setFont(label_font)
            layout.addWidget(label)
            
            if field_name in ["Notes", "Job Description"]:
                widget = QTextEdit()
                widget.setMinimumHeight(80 if field_name == "Notes" else 100)
            else:
                widget = QLineEdit()
            
            fields[field_name] = widget
            layout.addWidget(widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("secondary")
        cancel_btn.clicked.connect(dialog.reject)
        
        submit_btn = QPushButton("Add Application")
        submit_btn.clicked.connect(lambda: self._submit_application(dialog, fields))
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(submit_btn)
        layout.addLayout(button_layout)
        
        # Apply theme
        dialog.setStyleSheet(self.styleSheet())
        dialog.exec_()
    
    def _submit_application(self, dialog: QDialog, fields: dict):
        """Submit new application."""
        logger.info("User submitting new application form")
        
        # Get values
        company_name = fields["Company Name"].text()
        position = fields["Position"].text()
        country = fields["Country"].text()
        city = fields["City"].text()
        notes = fields["Notes"].toPlainText().strip() or None
        job_description = fields["Job Description"].toPlainText().strip() or None
        
        logger.debug(f"Form data: company={company_name}, position={position}, country={country}, city={city}")
        
        # Create through controller
        success, error = self.controller.create_application(
            company_name=company_name,
            position=position,
            country=country,
            city=city,
            notes=notes,
            job_description=job_description
        )
        
        if success:
            logger.info("Application created successfully - closing dialog")
            dialog.accept()
            self.refresh_table()
        else:
            logger.error(f"Failed to create application: {error}")
            QMessageBox.critical(self, "Error", error)
    
    def _delete_selected(self):
        """Delete selected applications."""
        logger.info("User clicked 'Delete Selected' button")
        selected_rows = set(item.row() for item in self.table.selectedItems())
        
        if not selected_rows:
            logger.warning("No rows selected for deletion")
            QMessageBox.warning(self, "No selection", "Please select an application to delete.")
            return
        
        logger.info(f"User selected {len(selected_rows)} row(s) for deletion")
        
        # Confirm deletion
        reply = QMessageBox.question(
            self, "Delete Confirmation",
            "Are you sure you want to delete the selected application(s)?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        # Get IDs
        app_ids = [int(self.table.item(row, 0).text()) for row in selected_rows]
        
        # Delete through controller
        success, error = self.controller.delete_multiple_applications(app_ids)
        
        if success:
            self.refresh_table()
        else:
            QMessageBox.critical(self, "Error", error)
    
    def _on_double_click(self, index):
        """Handle double-click on table row."""
        row = index.row()
        app_id = int(self.table.item(row, 0).text())
        self._show_job_details(app_id)
    
    def _show_job_details(self, app_id: int):
        """Show detailed view of job application."""
        application = self.controller.get_application(app_id)
        
        if not application:
            QMessageBox.critical(self, "Error", "Could not retrieve job details.")
            return
        
        colors = self.theme_config.get_colors()
        
        # Create details dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Job Details")
        dialog.setFixedSize(560, 700)
        
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # Display fields
        fields = [
            ("Company Name", application.company_name),
            ("Position", application.position),
            ("Country", application.country),
            ("City", application.city),
            ("Date Applied", application.date_applied.strftime('%Y-%m-%d')),
            ("Status", application.status.value),
            ("Notes", application.notes or "N/A")
        ]
        
        for label_text, value in fields:
            label = QLabel(f"{label_text}:")
            label_font = QFont(self.config.DEFAULT_FONT, self.config.DEFAULT_FONT_SIZE, QFont.Bold)
            label.setFont(label_font)
            layout.addWidget(label)
            
            value_label = QLabel(value)
            value_label.setWordWrap(True)
            layout.addWidget(value_label)
        
        # Job description
        desc_label = QLabel("Job Description:")
        desc_label_font = QFont(self.config.DEFAULT_FONT, self.config.DEFAULT_FONT_SIZE, QFont.Bold)
        desc_label.setFont(desc_label_font)
        layout.addWidget(desc_label)
        
        description_text = QTextEdit()
        description_text.setPlainText(application.job_description or "N/A")
        description_text.setReadOnly(True)
        description_text.setMaximumHeight(100)
        layout.addWidget(description_text)
        
        # Status update section
        status_label = QLabel("Change Status:")
        layout.addWidget(status_label)
        
        status_combo = QComboBox()
        status_combo.addItems(["applied", "rejected", "invited to interview"])
        status_combo.setCurrentText(application.status.value)
        layout.addWidget(status_combo)
        
        # Interview date
        date_label = QLabel("Interview Date (YYYY-MM-DD):")
        layout.addWidget(date_label)
        
        interview_date_entry = QLineEdit()
        if application.interview_date:
            interview_date_entry.setText(application.interview_date.strftime('%Y-%m-%d'))
        layout.addWidget(interview_date_entry)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("secondary")
        cancel_btn.clicked.connect(dialog.reject)
        
        update_btn = QPushButton("Update Status")
        update_btn.clicked.connect(
            lambda: self._update_status(dialog, app_id, status_combo.currentText(),
                                       interview_date_entry.text() or None)
        )
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(update_btn)
        layout.addLayout(button_layout)
        
        # Apply theme
        dialog.setStyleSheet(self.styleSheet())
        dialog.exec_()
    
    def _update_status(self, dialog: QDialog, app_id: int, new_status: str, interview_date: Optional[str]):
        """Update application status."""
        success, error = self.controller.update_status(
            app_id=app_id,
            new_status=new_status,
            interview_date=interview_date
        )
        
        if success:
            self.refresh_table()
            dialog.accept()
        else:
            QMessageBox.critical(self, "Error", error)
