import unittest
import sys
import os

# Add the ai directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ai')))

from model import AIModel

class TestAIModel(unittest.TestCase):

    def setUp(self):
        self.model = AIModel()
       
        self.training_data = [
            {'name': 'example_document.pdf', 'size': 2048, 'type': 'application/pdf', 'category': 'Documents'},
            {'name': 'example_image.jpg', 'size': 1024, 'type': 'image/jpeg', 'category': 'Images'},
            {'name': 'example_audio.mp3', 'size': 4096, 'type': 'audio/mpeg', 'category': 'Audio'},
        ]
        self.model.train(self.training_data) 

    # Test the predict_category method
    def test_predict_category(self):
   
        test_file_metadata = {
            'name': 'example_document.pdf',
            'size': 2048,
            'type': 'application/pdf'
        }
        predicted_category = self.model.predict_category(test_file_metadata)
        self.assertEqual(predicted_category, 'Documents')

    # Test the predict_category method with an edge case
    def test_predict_category_edge_case(self):
    
        test_file_metadata = {
            'name': 'unknown_file.xyz',
            'size': 1024,
            'type': 'application/x-unknown'
        }
        predicted_category = self.model.predict_category(test_file_metadata)
        self.assertEqual(predicted_category, 'Others')

    # Test the model accuracy
    def test_model_accuracy(self):
   
        test_data = [
            {'name': 'example_document.pdf', 'size': 2048, 'type': 'application/pdf', 'category': 'Documents'},
            {'name': 'example_image.jpg', 'size': 1024, 'type': 'image/jpeg', 'category': 'Images'},
            {'name': 'example_audio.mp3', 'size': 4096, 'type': 'audio/mpeg', 'category': 'Audio'},
        ]
        accuracy = self.model.evaluate(test_data)
        self.assertGreaterEqual(accuracy, 0.8)  

if __name__ == '__main__':
    unittest.main()