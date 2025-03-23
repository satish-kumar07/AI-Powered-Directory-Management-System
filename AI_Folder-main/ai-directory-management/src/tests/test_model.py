import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ai')))

from model import AIModel

class TestAIModel(unittest.TestCase):

    def setUp(self):
        self.model = AIModel()
        # Mock training data
        self.training_data = [
            {'name': 'example_document.pdf', 'size': 2048, 'type': 'application/pdf', 'category': 'Documents'},
            {'name': 'example_image.jpg', 'size': 1024, 'type': 'image/jpeg', 'category': 'Images'},
            {'name': 'example_audio.mp3', 'size': 4096, 'type': 'audio/mpeg', 'category': 'Audio'},
        ]
        self.model.train(self.training_data)  # Provide the mock training data

    def test_predict_category(self):
        # Test with a known input
        test_file_metadata = {
            'name': 'example_document.pdf',
            'size': 2048,
            'type': 'application/pdf'
        }
        predicted_category = self.model.predict_category(test_file_metadata)
        self.assertEqual(predicted_category, 'Documents')

    def test_predict_category_edge_case(self):
        # Test with an unknown file type
        test_file_metadata = {
            'name': 'unknown_file.xyz',
            'size': 1024,
            'type': 'application/x-unknown'
        }
        predicted_category = self.model.predict_category(test_file_metadata)
        self.assertEqual(predicted_category, 'Others')

    def test_model_accuracy(self):
        # Mock test data
        test_data = [
            {'name': 'example_document.pdf', 'size': 2048, 'type': 'application/pdf', 'category': 'Documents'},
            {'name': 'example_image.jpg', 'size': 1024, 'type': 'image/jpeg', 'category': 'Images'},
            {'name': 'example_audio.mp3', 'size': 4096, 'type': 'audio/mpeg', 'category': 'Audio'},
        ]
        accuracy = self.model.evaluate(test_data)
        self.assertGreaterEqual(accuracy, 0.8)  # Expecting at least 80% accuracy

if __name__ == '__main__':
    unittest.main()