# Services Package

Backup System Ready
Create backups:
python -m services.backup backup

List backups:
python -m services.backup list

Verify integrity:
python -m services.backup verify --name surgeontrainer_backup_20251113_104932.db.gz

Restore:
python -m services.backup restore --name surgeontrainer_backup_20251113_104932.db.gz




Utility services for SurgeonTrainer system maintenance and operations.

## Available Services

### Database Backup (`backup.py`)

Comprehensive backup solution with:
- **Manual backups**: Create on-demand backups
- **Compression**: Automatic gzip compression
- **Rotation**: Keeps only last N backups (default: 10)
- **Verification**: Check backup integrity
- **Restore**: Restore from any backup
- **Metadata tracking**: JSON metadata for each backup

## Usage Examples

### Python API

```python
from services.backup import DatabaseBackup

# Initialize backup manager
backup = DatabaseBackup(
    db_path="surgeontrainer.db",
    backup_dir="backups",
    max_backups=10,
    compress=True
)

# Create a backup
backup_path = backup.create_backup()
print(f"Backup created: {backup_path}")

# Create a named backup
backup.create_backup(backup_name="before_migration")

# List all backups
backups = backup.list_backups()
for b in backups:
    print(f"{b['filename']} - {b['size_mb']} MB - {b['created_at']}")

# Verify a backup
is_valid = backup.verify_backup("surgeontrainer_backup_20251113_120000.db.gz")

# Restore from backup
backup.restore_backup("surgeontrainer_backup_20251113_120000.db.gz")
```

### Command Line Interface

```powershell
# Create a backup
python services/backup.py backup

# Create a named backup
python services/backup.py backup --name "before_migration"

# List all backups
python services/backup.py list

# Verify a backup
python services/backup.py verify --name "surgeontrainer_backup_20251113_120000.db.gz"

# Restore from backup
python services/backup.py restore --name "surgeontrainer_backup_20251113_120000.db.gz"

# Custom options
python services/backup.py backup --db "path/to/db.db" --backup-dir "custom_backups" --max-backups 20 --no-compress
```

### Integration with FastAPI

```python
from fastapi import APIRouter
from services.backup import DatabaseBackup

router = APIRouter(prefix="/admin/backup", tags=["Admin"])

@router.post("/create")
async def create_backup():
    """Create a database backup"""
    backup = DatabaseBackup()
    backup_path = backup.create_backup()
    return {"success": True, "backup_path": str(backup_path)}

@router.get("/list")
async def list_backups():
    """List all available backups"""
    backup = DatabaseBackup()
    return {"backups": backup.list_backups()}
```

## Backup Storage

- **Location**: `backups/` directory (configurable)
- **Format**: `surgeontrainer_backup_YYYYMMDD_HHMMSS.db.gz`
- **Metadata**: Each backup has a `.json` file with timestamp, size, compression info
- **Compression**: gzip compression (typically 70-90% size reduction)
- **Rotation**: Automatically removes oldest backups when limit exceeded

## Safety Features

1. **SQLite Backup API**: Uses safe online backup (works while DB is in use)
2. **Integrity Verification**: Can verify backup integrity before restore
3. **Metadata Tracking**: JSON metadata for each backup
4. **No Data Loss**: Backups created atomically
5. **Compression**: Reduces storage footprint

## Best Practices

1. **Regular Backups**: Run backups before:
   - Database migrations
   - Major data imports
   - System updates
   - End of day/week

2. **Verification**: Periodically verify backup integrity

3. **Off-site Storage**: Copy backups to external storage for disaster recovery

4. **Retention**: Adjust `max_backups` based on storage and requirements

## Security Note

⚠️ **Backups contain PHI/PII data** - ensure proper security:
- Store backups in secure location
- Encrypt backups for transmission
- Follow HIPAA compliance requirements
- Never commit backups to version control
