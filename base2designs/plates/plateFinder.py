import cv2
import numpy as np
from PIL import Image

class PlateFinder:

    def __init__(self, minConfidence, categoryIdx):
        self.minConfidence = minConfidence
        self.categoryIdx = categoryIdx

    def findPlatesOnly(self, boxes, scores, labels):

        licensePlateFound = False

        # Discard all boxes below min score, and move plate boxes to separate list
        plateBoxes = []
        plateScores = []

        # loop over all the boxes and associated scores and labels
        for (i, (box, score, label)) in enumerate(zip(boxes, scores, labels)):
            if score < self.minConfidence:
                continue

            label = self.categoryIdx[label]
            label = "{}".format(label["name"])
            # if label is plate, then append data to new lists
            if label == "plate":
                licensePlateFound = True
                plateBoxes.append(box)
                plateScores.append(score)

        return licensePlateFound, plateBoxes, plateScores