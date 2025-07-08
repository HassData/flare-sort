import os
import re
import zipfile
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

# === CONFIG ===
DOWNLOADS_DIR = str(Path.home() / "Downloads")
UNZIP_DIR = str(Path.home() / "Downloads/agent-extracts")

# Ensure output directory exists
os.makedirs(UNZIP_DIR, exist_ok=True)

# === MAIN EXTRACT FUNCTION ===
def extract_zip_to_folder(zip_path):
    filename = os.path.basename(zip_path)

    # Only handle datadog-agent debug zips
    match = re.match(r'datadog-agent-.*?\.zip', filename)
    if not match:
        print(f"❌ Skipping unrelated file: {filename}")
        return

    # Peek inside the ZIP to determine the host folder name
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        namelist = zip_ref.namelist()
        top_folder = namelist[0].split('/')[0] if '/' in namelist[0] else 'unknown_host'

    # Prepare destination path
    target_base = os.path.join(UNZIP_DIR, top_folder)
    os.makedirs(target_base, exist_ok=True)

    # Create next available numbered subfolder
    index = 1
    while os.path.exists(os.path.join(target_base, str(index))):
        index += 1
    target_dir = os.path.join(target_base, str(index))
    os.makedirs(target_dir)

    # Extract files
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(target_dir)

    print(f"✅ Extracted {filename} → {target_dir}")

    # === CLEANUP ZIP FILE ===
    try:
        os.remove(zip_path)
        print(f"🧹 Deleted original zip file: {zip_path}")
    except Exception as e:
        print(f"⚠️ Failed to delete zip file: {e}")

# === WATCHDOG EVENT HANDLER ===
class ZipHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.zip'):
            # Give the file a moment to finish copying
            time.sleep(2)
            extract_zip_to_folder(event.src_path)

# === RUN WATCHDOG ===
if __name__ == "__main__":
    print(f"👀 Watching {DOWNLOADS_DIR} for .zip files...")
    observer = Observer()
    handler = ZipHandler()
    observer.schedule(handler, DOWNLOADS_DIR, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
