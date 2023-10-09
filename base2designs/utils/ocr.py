import cv2
import pytesseract as pt
pt.pytesseract.tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def ocr_on_image(image, plateBoxes, im_height, im_width):

    for plateBox in plateBoxes:

        y_min = int(plateBox[0] * im_height)
        x_min = int(plateBox[1] * im_width)
        y_max = int(plateBox[2] * im_height)
        x_max = int(plateBox[3] * im_width)

        point = (int(x_min + 70), int(y_min-10))

        roi = image[y_min:y_max, x_min:x_max]
        roi = cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY)

        cv2.imwrite("images/app_ocr/ocr.jpg", roi)

        text = pt.image_to_string(roi)
        #print(text)
        if text:
            text = "NumberPlate: " + text

        cv2.putText(image, text, point, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,0,200), 2)

    return image

def ocr_on_video_app(image, plateBoxes, im_height, im_width):
    for plateBox in plateBoxes:

        y_min = int(plateBox[0] * im_height)
        x_min = int(plateBox[1] * im_width)
        y_max = int(plateBox[2] * im_height)
        x_max = int(plateBox[3] * im_width)

        point = (int(x_min + 70), int(y_min - 10))

        roi = image[y_min:y_max, x_min:x_max]
        roi = cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY)

        cv2.imwrite("images/app_ocr/ocr.jpg", roi)
        img = QImage("images/app_ocr/ocr.jpg")
        pm = QPixmap.fromImage(img)
        self.roi1.setPixmap(pm)

        text = pt.image_to_string(roi)
        # print(text)
        if text:
            text = "NumberPlate: " + text

        cv2.putText(image, text, point, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 0, 200), 2)

    return image


"""
import io

from google.cloud import vision
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ""

client = vision.ImageAnnotatorClient()

def detection(img):
    with io.open (img, "rb") as image_file:
        content = image_file.read()

        image = vision_v1.types.Image(content = content)
        response = client.text_detection(image = image)
        texts = response.text_annotations

"""