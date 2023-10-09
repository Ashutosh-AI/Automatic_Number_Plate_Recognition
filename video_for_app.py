from google.cloud import vision
#from google.cloud.vision import types
from google.cloud.vision_v1 import types
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_cloud_vision.json"
client = vision.ImageAnnotatorClient()

image = types.Image()
image.source.imageUrl = "images/anpr.jpg"

response_label = client.label_detection(image = image)