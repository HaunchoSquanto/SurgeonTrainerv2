"""
Database Backup Utility for SurgeonTrainer

Provides automated backup functionality with:
- Manual backups on demand
- Scheduled automatic backups
- Rotation policy (keeps last N backups)
- Compression support
- Backup verification
"""
import os
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional, List
import gzip
import json


class DatabaseBackup:
    """Handles database backup operations"""
    
    def __init__(
        self,
        db_path: str = "surgeontrainer.db",
        backup_dir: str = "backups",
        max_backups: int = 10,
        compress: bool = True
    ):
        """
        Initialize backup manager
        
        Args:
            db_path: Path to the database file
            backup_dir: Directory to store backups
            max_backups: Maximum number of backups to keep (oldest deleted)
            compress: Whether to compress backups with gzip
        """
        self.db_path = Path(db_path)
        self.backup_dir = Path(backup_dir)
        self.max_backups = max_backups
        self.compress = compress
        
        # Create backup directory if it doesn't exist
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
    def create_backup(self, backup_name: Optional[str] = None) -> Path:
        """
        Create a database backup
        
        Args:
            backup_name: Optional custom name for backup file
            
        Returns:
            Path to the created backup file
        """
        if not self.db_path.exists():
            raise FileNotFoundError(f"Database not found: {self.db_path}")
        
        # Generate backup filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if backup_name:
            filename = f"{backup_name}_{timestamp}.db"
        else:
            filename = f"surgeontrainer_backup_{timestamp}.db"
        
        backup_path = self.backup_dir / filename
        
        print(f"Creating backup: {backup_path}")
        
        # Use SQLite backup API for safe backup
        try:
            self._sqlite_backup(self.db_path, backup_path)
            print(f"✓ Database backed up successfully")
        except Exception as e:
            print(f"✗ Backup failed: {e}")
            raise
        
        # Compress if enabled
        if self.compress:
            compressed_path = self._compress_backup(backup_path)
            backup_path.unlink()  # Remove uncompressed version
            backup_path = compressed_path
            print(f"✓ Backup compressed: {backup_path}")
        
        # Get file size
        size_mb = backup_path.stat().st_size / (1024 * 1024)
        print(f"✓ Backup size: {size_mb:.2f} MB")
        
        # Save backup metadata
        self._save_metadata(backup_path, size_mb)
        
        # Clean up old backups
        self._cleanup_old_backups()
        
        return backup_path
    
    def _sqlite_backup(self, source: Path, destination: Path):
        """
        Use SQLite backup API for safe backup while database is in use
        
        Args:
            source: Source database path
            destination: Destination backup path
        """
        # Connect to source and destination databases
        source_conn = sqlite3.connect(str(source))
        dest_conn = sqlite3.connect(str(destination))
        
        try:
            # Perform the backup
            with dest_conn:
                source_conn.backup(dest_conn)
        finally:
            source_conn.close()
            dest_conn.close()
    
    def _compress_backup(self, backup_path: Path) -> Path:
        """
        Compress backup file with gzip
        
        Args:
            backup_path: Path to uncompressed backup
            
        Returns:
            Path to compressed backup
        """
        compressed_path = backup_path.with_suffix(backup_path.suffix + '.gz')
        
        with open(backup_path, 'rb') as f_in:
            with gzip.open(compressed_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        return compressed_path
    
    def _save_metadata(self, backup_path: Path, size_mb: float):
        """
        Save backup metadata (timestamp, size, etc.)
        
        Args:
            backup_path: Path to backup file
            size_mb: Size in megabytes
        """
        metadata = {
            "filename": backup_path.name,
            "created_at": datetime.now().isoformat(),
            "size_mb": round(size_mb, 2),
            "compressed": self.compress,
            "source_db": str(self.db_path)
        }
        
        metadata_path = backup_path.with_suffix('.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def _cleanup_old_backups(self):
        """Remove oldest backups if exceeding max_backups limit"""
        # Get all backup files (both .db and .db.gz)
        backup_files = sorted(
            [f for f in self.backup_dir.glob("surgeontrainer_backup_*.db*") 
             if f.suffix in ['.db', '.gz']],
            key=lambda x: x.stat().st_mtime
        )
        
        # Remove oldest if exceeding limit
        while len(backup_files) > self.max_backups:
            oldest = backup_files.pop(0)
            print(f"Removing old backup: {oldest.name}")
            oldest.unlink()
            
            # Also remove metadata file
            metadata_path = oldest.with_suffix('.json')
            if metadata_path.exists():
                metadata_path.unlink()
    
    def list_backups(self) -> List[dict]:
        """
        List all available backups with metadata
        
        Returns:
            List of backup information dictionaries
        """
        backups = []
        
        for metadata_file in sorted(self.backup_dir.glob("*.json")):
            try:
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                    backups.append(metadata)
            except Exception as e:
                print(f"Warning: Could not read metadata for {metadata_file}: {e}")
        
        return backups
    
    def restore_backup(self, backup_filename: str, target_path: Optional[str] = None):
        """
        Restore database from backup
        
        Args:
            backup_filename: Name of backup file to restore
            target_path: Optional target path (defaults to original db_path)
        """
        backup_path = self.backup_dir / backup_filename
        
        if not backup_path.exists():
            raise FileNotFoundError(f"Backup not found: {backup_path}")
        
        target = Path(target_path) if target_path else self.db_path
        
        print(f"Restoring backup: {backup_filename} -> {target}")
        
        # Decompress if needed
        if backup_path.suffix == '.gz':
            temp_path = backup_path.with_suffix('')
            with gzip.open(backup_path, 'rb') as f_in:
                with open(temp_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            backup_path = temp_path
        
        # Copy backup to target
        shutil.copy2(backup_path, target)
        
        # Clean up temp file if decompressed
        if backup_path.suffix != '.gz' and backup_filename.endswith('.gz'):
            backup_path.unlink()
        
        print(f"✓ Database restored successfully")
    
    def verify_backup(self, backup_filename: str) -> bool:
        """
        Verify backup integrity
        
        Args:
            backup_filename: Name of backup file to verify
            
        Returns:
            True if backup is valid, False otherwise
        """
        backup_path = self.backup_dir / backup_filename
        
        if not backup_path.exists():
            print(f"✗ Backup not found: {backup_path}")
            return False
        
        print(f"Verifying backup: {backup_filename}")
        
        try:
            # Decompress if needed
            if backup_path.suffix == '.gz':
                temp_path = backup_path.with_suffix('')
                with gzip.open(backup_path, 'rb') as f_in:
                    with open(temp_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                check_path = temp_path
            else:
                check_path = backup_path
            
            # Try to open and query the database
            conn = sqlite3.connect(str(check_path))
            cursor = conn.cursor()
            
            # Run integrity check
            cursor.execute("PRAGMA integrity_check")
            result = cursor.fetchone()[0]
            
            conn.close()
            
            # Clean up temp file
            if backup_path.suffix == '.gz':
                check_path.unlink()
            
            if result == "ok":
                print(f"✓ Backup is valid")
                return True
            else:
                print(f"✗ Backup integrity check failed: {result}")
                return False
                
        except Exception as e:
            print(f"✗ Backup verification failed: {e}")
            return False


def main():
    """CLI interface for backup utility"""
    import argparse
    
    parser = argparse.ArgumentParser(description="SurgeonTrainer Database Backup Utility")
    parser.add_argument(
        "action",
        choices=["backup", "list", "restore", "verify"],
        help="Action to perform"
    )
    parser.add_argument(
        "--db",
        default="surgeontrainer.db",
        help="Path to database file (default: surgeontrainer.db)"
    )
    parser.add_argument(
        "--backup-dir",
        default="backups",
        help="Backup directory (default: backups)"
    )
    parser.add_argument(
        "--name",
        help="Backup name (for backup action) or filename (for restore/verify)"
    )
    parser.add_argument(
        "--max-backups",
        type=int,
        default=10,
        help="Maximum number of backups to keep (default: 10)"
    )
    parser.add_argument(
        "--no-compress",
        action="store_true",
        help="Disable compression"
    )
    
    args = parser.parse_args()
    
    # Initialize backup manager
    backup_manager = DatabaseBackup(
        db_path=args.db,
        backup_dir=args.backup_dir,
        max_backups=args.max_backups,
        compress=not args.no_compress
    )
    
    # Execute action
    if args.action == "backup":
        backup_path = backup_manager.create_backup(args.name)
        print(f"\n✓ Backup created: {backup_path}")
        
    elif args.action == "list":
        backups = backup_manager.list_backups()
        if backups:
            print(f"\nFound {len(backups)} backup(s):\n")
            for backup in backups:
                print(f"  {backup['filename']}")
                print(f"    Created: {backup['created_at']}")
                print(f"    Size: {backup['size_mb']} MB")
                print(f"    Compressed: {backup['compressed']}")
                print()
        else:
            print("\nNo backups found.")
            
    elif args.action == "restore":
        if not args.name:
            print("Error: --name required for restore action")
            return
        backup_manager.restore_backup(args.name)
        
    elif args.action == "verify":
        if not args.name:
            print("Error: --name required for verify action")
            return
        backup_manager.verify_backup(args.name)


if __name__ == "__main__":
    main()
