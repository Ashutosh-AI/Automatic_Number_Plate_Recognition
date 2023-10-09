import numpy as np
import cv2


class PlateDisplay:
    def __init__(self):
        self.saved_location = "images/plates_roi/"

    def getBoundingBox(self, image, plateBoxes, imagePath):
        filename = imagePath.split("/")[-1].split(".")[0]
        (H, W) = image.shape[:2]
        crop_bbox_images = []
        i = 0
        for plateBox in plateBoxes:
            # scale the bbox from range [0, 1] to [W, H]
            (startY, startX, endY, endX) = plateBox
            startX = int(startX * W)
            startY = int(startY * H)
            endX = int(endX * W)
            endY = int(endY * H)

            try:
                cropped_image = image[startY:endY, startX:endX]
                cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_RGB2GRAY)
                crop_bbox_images.append(cropped_image)
                cv2.imwrite("images/plates_roi/" + filename + "{}.jpg".format(i), cropped_image)
                i += 1
            except Exception as e:
                print("This is ", e)

        return np.array(crop_bbox_images)