import os
import time
import shutil
import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from processor import process_file
from config import WATCH_FOLDER, PROCESSED_FOLDER, FAILED_FOLDER, LOG_FILE

# Setup logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
processed_files_set = set()
def wait_for_file(file_path, timeout=10):
    """Wait until file is fully available"""
    start_time = time.time()

    while True:
        try:
            with open(file_path, "rb"):
                return True
        except PermissionError:
            if time.time() - start_time > timeout:
                return False
            time.sleep(1)

class FileHandler(FileSystemEventHandler):

  def on_any_event(self, event):
    if event.is_directory:
        return
    filename = os.path.basename(event.src_path)
    # Ignore temp Excel files
    if filename.startswith("~$"):
        return
    if not filename.endswith(".xlsx"):
        return

    print("Processing:", event.src_path)

    filename = os.path.basename(event.src_path)
    dest_path = os.path.join(PROCESSED_FOLDER, filename)

    try:
        # ✅ WAIT until file is ready
        if not wait_for_file(event.src_path):
            raise Exception("File not ready")

        # ✅ Copy after file is free
        shutil.copy(event.src_path, dest_path)

        success = process_file(dest_path)

        if not success:
            raise Exception("Processing failed")

    except Exception as e:
        print("ERROR:", str(e))

        failed_path = os.path.join(FAILED_FOLDER, filename)

        # Only move if file exists
        if os.path.exists(dest_path):
            shutil.move(dest_path, failed_path)


if __name__ == "__main__":
    os.makedirs(WATCH_FOLDER, exist_ok=True)
    os.makedirs(PROCESSED_FOLDER, exist_ok=True)
    os.makedirs(FAILED_FOLDER, exist_ok=True)

    observer = Observer()
    observer.schedule(FileHandler(), WATCH_FOLDER, recursive=False)

    observer.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()