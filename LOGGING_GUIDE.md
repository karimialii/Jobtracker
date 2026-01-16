# Logging System Documentation

## Overview

The Job Tracker application now includes **comprehensive logging** throughout all layers to track user actions, monitor application health, and debug issues.

## Features

### 1. Multi-Level Logging
- **DEBUG:** Detailed diagnostic information
- **INFO:** General application flow and user actions
- **WARNING:** Potentially problematic situations
- **ERROR:** Error events with stack traces
- **CRITICAL:** Severe errors that may crash the application

### 2. Dual Output
- **Console:** INFO and above displayed during runtime
- **File:** All logs (DEBUG+) saved to timestamped files in `logs/` directory

### 3. Structured Format
```
YYYY-MM-DD HH:MM:SS - module.name - LEVEL - message
```

## Log File Locations

Logs are automatically saved to:
```
logs/jobtracker_YYYYMMDD_HHMMSS.log
```

Example: `logs/jobtracker_20260116_165037.log`

## What Gets Logged

### Application Lifecycle
- ✅ Startup initialization (all layers)
- ✅ Database connection and schema setup
- ✅ Configuration loading
- ✅ Window creation and display
- ✅ Shutdown events

### User Interactions
- ✅ Button clicks ("Add Application", "Delete Selected", "Toggle Theme")
- ✅ Dialog opens/closes
- ✅ Form submissions
- ✅ Table row selections
- ✅ Double-click events

### Business Operations
- ✅ Creating new applications
- ✅ Updating application status
- ✅ Deleting applications
- ✅ Retrieving application data
- ✅ Data validation

### Database Operations
- ✅ All SQL queries (INSERT, UPDATE, DELETE, SELECT)
- ✅ Connection management
- ✅ Transaction handling
- ✅ Schema initialization

### Errors & Exceptions
- ✅ Validation errors
- ✅ Database errors
- ✅ UI errors
- ✅ Unexpected exceptions with full stack traces

## Example Log Session

```log
2026-01-16 16:50:37 - src.config.logging_config - INFO - Logging initialized. Log file: logs/jobtracker_20260116_165037.log
2026-01-16 16:50:37 - __main__ - INFO - ============================================================
2026-01-16 16:50:37 - __main__ - INFO - Job Tracker Application Starting
2026-01-16 16:50:37 - __main__ - INFO - ============================================================
2026-01-16 16:50:37 - src.repositories.job_application_repository - INFO - Initializing JobApplicationRepository with database: job_applications.db
2026-01-16 16:50:37 - src.repositories.job_application_repository - INFO - Database schema initialized successfully
2026-01-16 16:50:37 - src.views.main_window - INFO - Main window initialization complete
2026-01-16 16:50:42 - src.views.main_window - INFO - User clicked 'Add Application' button
2026-01-16 16:50:51 - src.views.main_window - INFO - User submitting new application form
2026-01-16 16:50:51 - src.views.main_window - DEBUG - Form data: company=TechCorp, position=Software Engineer, country=USA, city=San Francisco
2026-01-16 16:50:51 - src.services.job_application_service - INFO - Creating new application: TechCorp - Software Engineer
2026-01-16 16:50:51 - src.services.job_application_service - DEBUG - Details: country=USA, city=San Francisco, has_notes=True
2026-01-16 16:50:51 - src.services.job_application_service - INFO - Application created successfully with ID: 1
2026-01-16 16:50:51 - src.views.main_window - INFO - Application created successfully - closing dialog
```

## Using Logs for Debugging

### Identify User Actions
Search for "User clicked" or "User submitting" to see what actions the user took:
```bash
grep "User" logs/jobtracker_*.log
```

### Find Errors
Search for ERROR or CRITICAL messages:
```bash
grep -E "ERROR|CRITICAL" logs/jobtracker_*.log
```

### Track Performance
Use timestamps to identify slow operations:
```bash
grep "Creating new application\|created successfully" logs/jobtracker_*.log
```

### Analyze User Flow
Follow a complete session chronologically to understand the sequence of events leading to an issue.

## Benefits

1. **Debugging:** Quickly identify the root cause of issues
2. **Monitoring:** Track application health and usage patterns
3. **Auditing:** See exactly what users did and when
4. **Performance:** Identify bottlenecks in the application
5. **Support:** Provide detailed information when reporting bugs

## Configuration

Logging is configured in [src/config/logging_config.py](../src/config/logging_config.py):

- **Log Level:** DEBUG (all messages logged)
- **Console Level:** INFO (only important messages shown)
- **Format:** Timestamp - Module - Level - Message
- **File Rotation:** New file per application run

## Log Retention

Logs are not automatically deleted. To manage log files:

```bash
# View all logs
ls -lh logs/

# Delete old logs (keep last 7 days)
find logs/ -name "*.log" -mtime +7 -delete

# View specific log
cat logs/jobtracker_20260116_165037.log
```

## Security Notes

⚠️ **Warning:** Log files may contain sensitive information:
- Company names
- Job positions
- User input data
- File paths

Do NOT share log files publicly without reviewing their contents first.

## Troubleshooting

### Logs Not Created
- Check that `logs/` directory exists (created automatically)
- Verify write permissions
- Check console for initialization errors

### Missing Log Entries
- Ensure logging is initialized before actions
- Check log level configuration
- Verify logger names match module paths

### Large Log Files
- Logs accumulate over time
- Implement rotation or cleanup script
- Consider log aggregation tools for production

## Future Enhancements

- [ ] Log rotation (max size/count)
- [ ] Log compression for old files
- [ ] Remote log shipping for monitoring
- [ ] Performance metrics logging
- [ ] User session IDs for tracking
