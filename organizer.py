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
import json
import mimetypes
from logger import Logger

logger = Logger()

class FileOrganizer:
    def __init__(self, source, dest, ext=None):
        self.source = source
        self.dest = dest
        self.rules = self.load_rules(ext)
        self.process_files()

    def process_files(self):
        """ Process files in the source directory """	
        start_time = time.time()
        file_count, total_size = 0, 0

        if os.path.exists(self.source):
            for root, _, files in os.walk(self.source):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_count += 1
                    total_size += os.path.getsize(file_path)

                    self.file_attributes = self.get_file_attributes(file_path)
                    
                    if "_duplicate_check" in self.rules and self.rules["_duplicate_check"]:
                        if self.is_duplicate(file_path):
                            continue

                    target_directory = self.get_target_directory(file_path)
                    self.move_file(file_path, target_directory)

        print(f"\nProcessed {file_count} files ({total_size / (1024 * 1024):.2f} MB) in {time.time() - start_time:.3f} seconds")

    def get_target_directory(self, file_path):
        """ Determines the best matching directory for the file based on conditions """
        best_match = None
        best_match_score = 0

        for folder, conditions in self.rules.items():
            if folder.startswith("_"):
                continue

            match_score = 0
            conditions_met = True

            for condition in conditions:
                if "->" in condition:
                    source_ext, target_ext = condition.split("->")
                    if self.file_attributes["$type"] == source_ext.strip():
                        self.file_attributes["$type"] = target_ext.strip()
                        match_score += 1
                else:
                    try:
                        condition_eval = eval(condition, {}, self.file_attributes)
                        if not condition_eval:
                            conditions_met = False
                            break
                        match_score += 1
                    except Exception as e:
                        print(f"Error evaluating condition '{condition}': {e}")
                        conditions_met = False
                        break

            if conditions_met and match_score > best_match_score:
                best_match = folder
                best_match_score = match_score

        if best_match:
            final_path = os.path.join(self.dest, best_match.format(**self.file_attributes))
        else:
            final_path = self.dest

        return final_path

    def load_rules(self, ext_files):
        """ Load rules from JSON files and merge them into a single dictionary"""
        jsonext = {}
        for v in ext_files:
            try:
                with open(f"{v}.json", 'r') as file:
                    tmp = json.load(file)
                    jsonext = {**jsonext, **tmp}
            except FileNotFoundError:
                print(f"File not found: {v}")
            except Exception as e:
                print(f"An error occurred while reading {v}.json: {e}")
            finally:
                file.close()
        return jsonext
    
    def is_duplicate(self, file_path):
        """ Check for duplicates in the source directory """
        file_name = os.path.basename(file_path)
        duplicates = [f for f in os.listdir(self.source) if f == file_name]
        return len(duplicates) > 1

    def convert_files(self, file, conversion_format):
        """ Convert files to the specified format """
        pass

    def move_file(self, file_path, target_directory):
        """ Moves file to the target directory """
        os.makedirs(target_directory, exist_ok=True)
        shutil.move(file_path, os.path.join(target_directory, os.path.basename(file_path)))
        print(f"Moved: {file_path} -> {target_directory}")

    def get_file_attributes(self, file_path):
        """ Extract file attributes like size, type, date modified, and associated app """
        file_stat = os.stat(file_path)
        file_size = file_stat.st_size / (1024 * 1024)
        file_ext = os.path.splitext(file_path)[-1].lower()
        mod_time = datetime.fromtimestamp(file_stat.st_mtime)
        app_used = mimetypes.guess_type(file_path)[0] or "unknown"

        return {
            "$size": file_size,
            "$type": file_ext,
            "$date": mod_time.strftime('%Y-%m-%d'),
            "$app": app_used
        }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=True, description="Organize Files in a Folder")

    parser.add_argument('inputs', nargs='*', help="Source and Destination Folders (Destination at the last place)")
    parser.add_argument("-m", "--method", nargs="+", required=True, help="All Sorting methods to Use")
    args = parser.parse_args()

    FileOrganizer(args.inputs[:-1], args.inputs[-1], ext=args.method)