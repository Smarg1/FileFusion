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

import logging
import os
from datetime import datetime

class Logger:
    def __init__(self):
        format = "[%(asctime)s] [%(name)s/%(levelname)s]: %(message)s"
        logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
        os.makedirs(logs_dir, exist_ok=True)
        log_file = os.path.join(logs_dir, f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

        self.logger = logging.getLogger(__class__.__name__)
        self.logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        file_formatter = logging.Formatter(format, datefmt="%H:%M:%S")
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        console_formatter = logging.Formatter(format, datefmt="%H:%M:%S")
        console_handler.setFormatter(console_formatter)

        self.logger.addHandler(console_handler)

    def debug(self, message):
        self.logger.debug(message)
    
    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)
        print(message)
    
    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

if '__main__' == __name__:
    log = Logger()
    log.debug("Debug")
    log.warning("Warning")
    log.info("Information")
    log.critical("Critical")
    log.error("Error")