import os
import subprocess
import logging
from datetime import datetime
from app.core.config import settings

logger = logging.getLogger("BackupManager")

class BackupManager:
    """
    Disaster Recovery (DR) and Business Continuity Manager.
    Handles automated backups, Point-in-Time Recovery (PITR), and snapshot management.
    """
    
    BACKUP_DIR = os.getenv("BACKUP_DIR", "/var/backups/world_sim")

    @classmethod
    def ensure_backup_dir(cls):
        os.makedirs(cls.BACKUP_DIR, exist_ok=True)

    @classmethod
    def create_database_backup(cls, tag: str = "automated") -> str:
        """
        Creates a pg_dump backup of the database.
        """
        cls.ensure_backup_dir()
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"db_backup_{tag}_{timestamp}.sql.gz"
        filepath = os.path.join(cls.BACKUP_DIR, filename)

        # Ensure environment variables are passed to pg_dump
        env = os.environ.copy()
        env["PGPASSWORD"] = settings.POSTGRES_PASSWORD

        command = [
            "pg_dump",
            "-h", settings.POSTGRES_SERVER,
            "-p", str(settings.POSTGRES_PORT),
            "-U", settings.POSTGRES_USER,
            "-d", settings.POSTGRES_DB,
            "-F", "c", # custom format for pg_restore
            "-f", filepath
        ]

        try:
            logger.info(f"Starting database backup: {filepath}")
            subprocess.run(command, env=env, check=True)
            logger.info(f"Database backup completed successfully: {filepath}")
            return filepath
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to create database backup: {e}")
            raise RuntimeError("Database backup failed") from e

    @classmethod
    def restore_database_backup(cls, filepath: str):
        """
        Restores a database from a pg_dump custom format backup.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Backup file not found: {filepath}")

        env = os.environ.copy()
        env["PGPASSWORD"] = settings.POSTGRES_PASSWORD

        command = [
            "pg_restore",
            "-h", settings.POSTGRES_SERVER,
            "-p", str(settings.POSTGRES_PORT),
            "-U", settings.POSTGRES_USER,
            "-d", settings.POSTGRES_DB,
            "-1", # run in single transaction
            "-c", # clean before restore
            filepath
        ]

        try:
            logger.info(f"Starting database restore from: {filepath}")
            subprocess.run(command, env=env, check=True)
            logger.info(f"Database restore completed successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to restore database: {e}")
            raise RuntimeError("Database restore failed") from e
