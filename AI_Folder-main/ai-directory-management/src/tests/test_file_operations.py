import os
import unittest
import sys

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'utils')))

from file_operations import move_file, categorize_file

class TestFileOperations(unittest.TestCase):

    def setUp(self):
        self.test_source_dir = 'test_source'
        self.test_target_dir = 'test_target'
        os.makedirs(self.test_source_dir, exist_ok=True)
        os.makedirs(self.test_target_dir, exist_ok=True)

        # Create test files
        self.test_files = {
            'image.jpg': 'This is a test image file.',
            'document.pdf': 'This is a test document file.',
            'audio.mp3': 'This is a test audio file.',
            'video.mp4': 'This is a test video file.',
            'script.py': 'print("Hello World")',
        }

        for file_name, content in self.test_files.items():
            with open(os.path.join(self.test_source_dir, file_name), 'w') as f:
                f.write(content)

    def tearDown(self):
        for file_name in self.test_files.keys():
            try:
                os.remove(os.path.join(self.test_source_dir, file_name))
            except FileNotFoundError:
                pass
        try:
            os.rmdir(self.test_source_dir)
            os.rmdir(self.test_target_dir)
        except OSError:
            pass

    def test_categorize_file(self):
        categories = {
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
            "Documents": [".txt", ".doc", ".docx", ".pdf", ".xls", ".xlsx"],
            "Videos": [".mp4", ".mkv", ".avi", ".mov"],
            "Audio": [".mp3", ".wav", ".flac"],
            "Code": [".py", ".java", ".cpp", ".html", ".css", ".js"],
            "Archives": [".zip", ".rar", ".tar", ".gz"],
            "Others": [] 
        }
        self.assertEqual(categorize_file('image.jpg', categories), 'Images')
        self.assertEqual(categorize_file('document.pdf', categories), 'Documents')
        self.assertEqual(categorize_file('audio.mp3', categories), 'Audio')
        self.assertEqual(categorize_file('video.mp4', categories), 'Videos')
        self.assertEqual(categorize_file('script.py', categories), 'Code')
        self.assertEqual(categorize_file('unknown_file.xyz', categories), 'Others')

    def test_move_file(self):
        move_file(os.path.join(self.test_source_dir, 'image.jpg'), os.path.join(self.test_target_dir, 'image.jpg'))
        self.assertTrue(os.path.exists(os.path.join(self.test_target_dir, 'image.jpg')))
        self.assertFalse(os.path.exists(os.path.join(self.test_source_dir, 'image.jpg')))

if __name__ == '__main__':
    unittest.main()