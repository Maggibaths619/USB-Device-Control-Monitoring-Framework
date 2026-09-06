import os
import hashlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from modules.logger import get_logger

logger = get_logger("FileAuditor")

def calculate_sha256(filepath):
    """Calculates the SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        return f"ERROR: {str(e)}"

class AuditEventHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.event_count = 0

    def _count(self):
        self.event_count += 1

    def on_created(self, event):
        if not event.is_directory:
            self._count()
            logger.info(f"[FILE CREATED] {event.src_path}")
            # Hash the file for integrity tracking
            file_hash = calculate_sha256(event.src_path)
            logger.info(f"[FILE HASH]    {event.src_path} -> SHA256: {file_hash}")

    def on_deleted(self, event):
        if not event.is_directory:
            self._count()
            logger.info(f"[FILE DELETED] {event.src_path}")

    def on_modified(self, event):
        if not event.is_directory:
            self._count()
            logger.info(f"[FILE MODIFIED] {event.src_path}")

    def on_moved(self, event):
        if not event.is_directory:
            self._count()
            logger.info(f"[FILE MOVED] {event.src_path} -> {event.dest_path}")

class FileAuditor:
    def __init__(self):
        self.observers = {}  # Map of drive_letter -> observer

    def start_monitoring(self, drive_path):
        """
        Starts monitoring a specific drive or path.
        Example drive_path: 'E:\\'
        """
        if drive_path in self.observers:
            logger.warning(f"Already monitoring {drive_path}")
            return

        if not os.path.exists(drive_path):
            logger.error(f"Cannot monitor {drive_path}: Path does not exist.")
            return

        logger.info(f"Starting file audit on drive: {drive_path}")
        event_handler = AuditEventHandler()
        observer = Observer()
        observer.schedule(event_handler, drive_path, recursive=True)
        observer.start()
        
        self.observers[drive_path] = observer

    def stop_monitoring(self, drive_path):
        """
        Stops monitoring a specific drive.
        """
        if drive_path in self.observers:
            logger.info(f"Stopping file audit on drive: {drive_path}")
            observer = self.observers.pop(drive_path)
            observer.stop()
            observer.join()
        else:
            logger.warning(f"Was not monitoring {drive_path}")

    def stop_all(self):
        for drive_path, observer in list(self.observers.items()):
            self.stop_monitoring(drive_path)
