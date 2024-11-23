"""
Copyright 2024 Smarg1

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import shutil
import time
import argparse
from datetime import datetime
from enums import enum

class FileOrganizer:
    def __init__(self, source, dest, ext=None, converter=False, duplicates=False):
        self.__iter_files(source, dest, converter, duplicates, list(ext))

    def __iter_files(self, source, dest, con, dup, ext):
        start = time.time()
        if os.path.exists(source):
            for root, dirs, files in os.walk(source):
                for file in files:
                    file_count =+ 1
                    file_path = os.path.join(root, file)
                    file_size =+ os.path.getsize(file_path)
                    if con: self.convert_files(file_path)
                    if dup: self.duplicate_find(file_path)
                    self.organize(file_path, dest, ext)
        else:
            print(f"Source folder '{source}' does not exist. Skipping...")
                
        print(f"\nOrganized {file_count}({file_size/1073741824}) files in {time.time() - start:.3f} seconds")

    def organize(self, file_path: str, dest, ext:list):
        try:
            for v in ext:
                if v == enum.DATE.value:
                    file_time = os.path.getmtime(file_path)
                    date = datetime.fromtimestamp(file_time)
                    year_folder = os.path.join(dest, str(date.year))
                    month_folder = os.path.join(year_folder, date.strftime("%B"))
                    os.makedirs(month_folder, exist_ok=True)
                    shutil.copy2(file_path, os.path.join(month_folder, os.path.basename(file_path)))
                    file_path = os.path.join(month_folder, os.path.basename(file_path))
                if v == enum.APP.value: pass
                if v == enum.TYPE.value: pass
                if v == enum.SIZE.value: pass

        except Exception as e:
            print(f"Error organizing file: '{file_path}': {e}")
    
    def duplicate_find(self, file):
        pass

    def convert_files(self, file):
        pass

if __name__ == "__main__":
    enums = enum()
    parser = argparse.ArgumentParser()
    parser.add_argument('inputs', nargs='*', required=True)

    parser.add_argument('-c','--convert', action='store_true')
    parser.add_argument('-d','--duplicate', action='store_true')
    parser.add_argument('-h','--help', action='store_true')

    parser.add_argument(
        "--ext", 
        nargs="+",
        required=True
    )

    args = parser.parse_args()
    if not args.help:
        FileOrganizer(args.inputs[:-1],
                    args.inputs[-1],
                    args.ext,
                    converter=args.convert,
                    duplicates=args.duplicate)
    else:
        print(""" """)
    

