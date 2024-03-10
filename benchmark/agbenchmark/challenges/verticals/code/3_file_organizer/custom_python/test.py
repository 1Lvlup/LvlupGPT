import os
import subprocess
import shutil
import unittest

class TestOrganizeFiles(unittest.TestCase):
    def setUp(self):
        # Create temporary directory
        self.test_dir = tempfile.mkdtemp()

        # File types and their corresponding directory
        self.file_types = {
            "test_image.png": "images",
            "test_doc.txt": "documents",
            "test_audio.mp3": "audio",
        }

        # Create test files
        for file_name in self.file_types.keys():
            file_path = os.path.join(self.test_dir, file_name)
            with open(file_path, "w") as f:
                f.write("Test content")

