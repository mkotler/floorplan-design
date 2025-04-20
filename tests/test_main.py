import unittest
from unittest.mock import patch
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from src.main import MainWindow
import os


class TestFloorplanImageUpload(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["TEST_ENV"] = "1"  # Set the TEST_ENV environment variable
        cls.app = QApplication([])

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()
        del os.environ["TEST_ENV"]  # Clear the TEST_ENV environment variable

    def setUp(self):
        self.window = MainWindow()
        self.window.show()

    def tearDown(self):
        self.window.close()

    def test_upload_button_exists(self):
        # Ensure the upload button is initialized and visible
        self.assertIsNotNone(self.window.upload_button)
        self.assertTrue(
            self.window.upload_button.isEnabled()
        )  # Check if the button is enabled

    def test_open_image_dialog(self):
        # Simulate clicking the upload button
        QTest.mouseClick(self.window.upload_button, Qt.LeftButton)

        # Ensure the button click does not cause errors
        self.assertTrue(self.window.upload_button.isEnabled())


if __name__ == "__main__":
    unittest.main()
