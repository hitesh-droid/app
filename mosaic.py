import cv2
import numpy as np


class ImageProcessor:
    def __init__(self, image, rows):
        self.image = image
        self.rows = rows

    def process(self):
        img = cv2.imdecode(np.fromstring(self.image.read(), np.uint8), cv2.IMREAD_UNCHANGED)

        # Resize the image to fit multiple copies on an A4 sheet
        img_height, img_width = img.shape[:2]
        target_height = int(45 / 35 * img_width)
        img = cv2.resize(img, (img_width, target_height))

        if self.rows != 0:
            # Calculate the number of columns
            a4_width = int(2100)
            a4_height = int(2970)
            cols = a4_width // (img_width + 20)

            # Create an empty canvas
            canvas = np.ones((a4_height, a4_width, 3), dtype="uint8") * 255

            # Copy the resized images onto the canvas
            for i in range(self.rows):
                for j in range(cols):
                    x_offset = j * (img_width + 30) + 100
                    y_offset = i * (target_height + 30) + 30
                    canvas[y_offset:y_offset + target_height, x_offset:x_offset + img_width, :] = img

            _, buffer = cv2.imencode(".jpg", canvas)
        else:
            _, buffer = cv2.imencode(".jpg", img)
        return buffer.tobytes()

