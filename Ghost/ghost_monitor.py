import os
import shutil
import getpass
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ===== CONFIGURATION =====
WATCH_DIR = r"C:\Users\Admin\Desktop\Hackathon\Ghost\watch_dir"
SHADOW_DIR = r"C:\Users\Admin\Desktop\Hackathon\Ghost\.Shadow"
RECYCLE_DIR = r"C:\Users\Admin\Desktop\Hackathon\Ghost\RecycleBin"

# Ensure recycle directory exists
os.makedirs(RECYCLE_DIR, exist_ok=True)


class GhostHandler(FileSystemEventHandler):

    def on_deleted(self, event):
        if event.is_directory:
            return

        deleted_path = event.src_path

        try:
            # Get relative path
            rel_path = os.path.relpath(deleted_path, WATCH_DIR)
            shadow_path = os.path.join(SHADOW_DIR, rel_path)

            if not os.path.exists(shadow_path):
                print(f"[!] Shadow file not found: {shadow_path}")
                return

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            username = getpass.getuser()

            safe_name = rel_path.replace("\\", "_").replace("/", "_")

            recycled_file = os.path.join(
                RECYCLE_DIR,
                f"{safe_name}_deleted_at_{timestamp}"
            )

            metadata_file = os.path.join(
                RECYCLE_DIR,
                f"{safe_name}_metadata_{timestamp}.txt"
            )

            # Copy from Shadow
            shutil.copy2(shadow_path, recycled_file)

            # Create metadata
            with open(metadata_file, "w") as meta:
                meta.write(f"Original Path: {deleted_path}\n")
                meta.write(f"Deleted By: {username}\n")
                meta.write(f"Deletion Time: {timestamp}\n")
                meta.write(f"Recovered Time: {datetime.now()}\n")
                meta.write(f"File Size: {os.path.getsize(recycled_file)} bytes\n")

            print(f"[✓] Recovered: {deleted_path}")

        except Exception as e:
            print(f"[ERROR] {e}")


if __name__ == "__main__":
    print("Ghost File Recovery Monitor Running...")
    print(f"Watching: {WATCH_DIR}")

    event_handler = GhostHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIR, recursive=True)
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
