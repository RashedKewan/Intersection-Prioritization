import os
from openpyxl import load_workbook
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen.canvas import Canvas
import GlobalData as GD
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import PDFReport as pdf
import FileController as fc

import unittest

class TestPDFReport(unittest.TestCase):
    def test_excel_to_image(self):
# Test if the function converts the Excel file to an image correctly
        image_height = pdf.excel_to_image('configuration/vehicles_db.xlsx')
        self.assertGreater(image_height, 0)
        self.assertIsInstance(image_height, int)
        self.assertEqual(os.path.exists('temp/vehicles_db.png'), True)


    def test_create_report(self):
       
        path , current_time = fc.create_directory()
        pdf.create_report(path, current_time)
        
        # Check that a PDF file was created at the specified path
        self.assertTrue(os.path.exists(f"{path}/report.pdf"))

if __name__ == '__main__':
    unittest.main()