"""
Acts as an watchdog to detect any changes in the working directory and run the script each time a change is detected
"""

import subprocess
import time
import os
import psutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
	"""
	Acts as an watchdog to detect any changes in the working directory and run the script each time a change is detected
	"""

    def __init__(self):
        self.last_event_time = 0

    def on_modified(self, event):
        if "__pycache__" in event.src_path:
            return  # Ignore changes in the __pycache__ directory

        current_time = time.time()
        if current_time - self.last_event_time > 5:  # Wait 5 seconds between events
            self.last_event_time = current_time
            print(f'Change detected: {event.event_type} - {event.src_path}')
            self.restart_script()

    def restart_script(self):
        for proc in psutil.process_iter():
            try:
                if "python" in proc.name() and "main.py" in " ".join(proc.cmdline()):
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        subprocess.Popen(["python", "main.py"])  # Run main.py

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(MyHandler(), ".", recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)  # Sleep to avoid a high CPU usage
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
