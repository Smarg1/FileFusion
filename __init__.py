import os
import shutil
import time
import psutil
import sys
from datetime import datetime

class FileFusion:
    def __init__(self):
        try:
            print(f"Starting {self.__class__.__name__}...")

            # Ensure only one instance of the app is running
            self.check_single_instance()

            while 1:
                # Get Source Folder
                source = self.getpath("Enter Source location: ")

                # Get Destination Folder
                dest = self.getpath("Enter Destination location: ")
                if os.path.abspath(source) == os.path.abspath(dest):
                    print("Source and destination folders must be different.\n")
                else:
                    break

            # Optimize
            self.optimize(source, dest)
        except KeyboardInterrupt:
            print("App was interrupted by User.")
    
    def getpath(self, message: str):
        while True:
            try:
                path = input(message)
                if not os.path.exists(path):
                    raise NotADirectoryError
                return path
            except NotADirectoryError:
                print("Folder Not Found! Please enter a Valid Path")

    def optimize(self, source, dest):
        
        print("Optimizing...")
        photo_extensions = ('.jpg', '.jpeg', '.png', '.gif')
        video_extensions = ('.mp4', '.mov', '.avi', '.mkv')

        photo_destination = os.path.join(dest, 'Photos')
        video_destination = os.path.join(dest, 'Videos')
        
        os.makedirs(photo_destination, exist_ok=True)
        os.makedirs(video_destination, exist_ok=True)

        for root, dirs, files in os.walk(source):
            for file in files:
                file_path = os.path.join(root, file)
                file_extension = os.path.splitext(file)[1].lower()
                
                creation_time = os.path.getctime(file_path)
                creation_date = datetime.fromtimestamp(creation_time)
                year = creation_date.year
                month = creation_date.strftime('%B')
                
                if file_extension in photo_extensions:
                    target_folder = os.path.join(photo_destination, str(year), month)
                elif file_extension in video_extensions:
                    target_folder = os.path.join(video_destination, str(year), month)
                else:
                    continue
                
                os.makedirs(target_folder, exist_ok=True)

                destination_path = os.path.join(target_folder, file)
                if os.path.abspath(file_path) == os.path.abspath(destination_path):
                    print(f"Skipping {file} as it is already in the target folder.")
                    continue
                
                retries = 5
                for attempt in range(retries):  # Retry up to 5 times
                    try:
                        with open(file_path, 'rb'):  # Read-only access
                            shutil.copy2(file_path, destination_path)
                        print(f"Copied {file} to {target_folder}")
                        break
                    except PermissionError:
                        print(f"PermissionError: Could not copy {file}. Retrying... ({attempt + 1}/{retries})")
                        time.sleep(1 + attempt)  # Increasing delay with each retry
                else:
                    print(f"Failed to copy {file} after multiple attempts.")
                
        self.cleanup()

    def cleanup(self):
        try:
            print("Optimized!\nError Code: 0")
            sys.exit(0)
        except Exception as e:
            print(f"Error Code: 1\n{e}")
            sys.exit(1)

    def check_single_instance(self):
        current_pid = os.getpid()
        current_process = psutil.Process(current_pid)
        current_script = current_process.cmdline()[1]

        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            if proc.info['pid'] != current_pid:
                try:
                    if proc.info['cmdline'] and current_script in proc.info['cmdline']:
                        print("Another instance of this app is already running. Exiting...")
                        sys.exit(0)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass

if __name__ == "__main__":
    FileFusion()
