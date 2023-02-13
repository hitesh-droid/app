import os
import uuid
from PIL import Image
from fpdf import FPDF


class ImageToPDF:
    def __init__(self, images, filename):
        self.images = images
        self.filename = filename

    def convert(self):
        pdf = FPDF()
        for file in self.images:
            # Create a temporary file
            filename = str(uuid.uuid4()) + '.jpg'
            file.save(filename)
            # Add a page to the PDF and add the image
            pdf.add_page()
            im = Image.open(filename)
            im = im.convert("CMYK")
            im.save(filename)
            pdf.image(filename, 0, 0, 210, 297)
            # Delete the temporary file
            os.remove(filename)
        return pdf
