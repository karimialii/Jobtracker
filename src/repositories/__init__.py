"""Repositories package for data access layer."""
from .job_application_repository import (
    IJobApplicationRepository,
    JobApplicationRepository
)

__all__ = ['IJobApplicationRepository', 'JobApplicationRepository']
