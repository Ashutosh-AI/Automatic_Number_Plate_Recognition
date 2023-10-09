'''import os

import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUiType
import sys

import cv2
import datetime
from imutils.video import VideoStream
import pytesseract as pt
pt.pytesseract.tesseract_cmd=r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from base2designs.utils import detector_utils
from base2designs.utils.detector_utils import Predicter
from base2designs.plates.plateFinder import PlateFinder
from base2designs.plates.plateDisplay import PlateDisplay
from base2designs.utils import ocr

# This function generates and loads a .ui file at runtime, and it returns a tuple containing the reference to the Python class, and the base class.
ui, _ = loadUiType("anpr.ui")
#print("UI", ui, "UI type", type(ui))


class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.startButton.clicked.connect(self.start_monitoring)
        self.stopButton.clicked.connect(self.stop_monitoring)
        #self.Date.setText("Date :" + date)
        #self.Time.setText(" Time :" + time)
        #self.FPS.setText("FPS : " + "22")



    def start_monitoring(self):
        print("Start monitoring button clicked")
        self.setDate()

        detection_graph, sess = detector_utils.load_inference_graph()

        #self.vs = VideoStream(0).start()
        vs = VideoStream("traffic.mp4").start()

        start_time = datetime.datetime.now()
        num_frames = 0
        score_thresh = 0.60
        num_vehicles_detect = 20

        try:
            while True:
                self.setTime()
                frame = vs.read()

                try:
                    im_height, im_width = frame.shape[:2]
                    print("try1 running")
                except:
                    print("try1 Error")

                # Convert image to RGB, opencv reads BGR formats
                try:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                except:
                    print("Error Converting to RGB Format")

                try:
                    plateFinder = PlateFinder(score_thresh, detector_utils.category_index)
                    predicter = Predicter(detection_graph, sess)
                    plate_display = PlateDisplay()
                    print("try2 running")
                except:
                    print("try2 Error")

                try:
                    boxes, scores, labels = predicter.predictPlates(frame)
                    print("try3 running")
                except:
                    print("try3 Error")

                try:
                    licensePlateFound_pred, plateBoxes_pred, plateScores_pred = plateFinder.findPlatesOnly(boxes, scores, labels)

                    frame = predicter.draw_box_on_image(score_thresh=score_thresh, num_vehicles_detect=num_vehicles_detect,
                                        scores=scores,
                                        boxes=boxes, classes=labels, im_width=im_width, im_height=im_height,
                                        image_np=frame)
                    print("try4 running")
                except:
                    print("try4 Error")

                #frame = ocr.ocr_on_image(frame, plateBoxes_pred, im_height, im_width)
                try:
                    frame = self.ocr_on_video_app(frame, plateBoxes_pred, im_height, im_width)
                    print("try5 running")
                except:
                    print("try5 Error")

                try:
                    num_frames += 1
                    elapsed_time = (datetime.datetime.now() - start_time).total_seconds()
                    fps = num_frames / elapsed_time
                    self.setFps(fps)
                    print("try6 running")
                except:
                    print("try6 Error")

                try:
                    cv2.imwrite("images/app_img/captured.jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                    img = QImage("images/app_img/captured.jpg")
                    pm = QPixmap.fromImage(img)
                    self.Image.setPixmap(pm)
                    cv2.waitKey(50)
                    print("try7 running")
                except:
                    print("try7 Error")

            print(fps)

        except:
            print("getting an exception")

    def stop_monitoring(self):
        self.close()
        self.vs.release()
        cv2.destroyAllWindows()
        print("Stop monitoring button clicked")

    def setDate(self):
        date = datetime.datetime.now().strftime("%d/%m/%Y")
        self.Date.setText(" Date :" + date)

    def setTime(self):
        time = datetime.datetime.now().strftime("%H:%M:%S")
        self.Time.setText(" Time :" + time)

    def setFps(self, fps):
        self.FPS.setText(" FPS :" + str(np.round_(fps,2)))

    def ocr_on_video_app(self, image, plateBoxes, im_height, im_width):
        i = 0
        for plateBox in plateBoxes:

            y_min = int(plateBox[0] * im_height)
            x_min = int(plateBox[1] * im_width)
            y_max = int(plateBox[2] * im_height)
            x_max = int(plateBox[3] * im_width)

            point = (int(x_min + 70), int(y_min - 10))

            roi = image[y_min:y_max, x_min:x_max]
            roi = cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY)

            text = pt.image_to_string(roi)

            cv2.imwrite("images/app_ocr/ocr.jpg", roi)
            img = QImage("images/app_ocr/ocr.jpg")
            pm = QPixmap.fromImage(img)

            if i == 0:
                self.roi1.setPixmap(pm)
                text1 = text
                self.roi1_ocr.setText(text1)
            elif i == 1:
                self.roi2.setPixmap(pm)
                text2 = text
                self.roi2_ocr.setText(text2)
            elif i == 2:
                self.roi3.setPixmap(pm)
                text3 = text
                self.roi3_ocr.setText(text3)
            elif i == 3:
                self.roi4.setPixmap(pm)
                text4 = text
                self.roi4_ocr.setText(text4)
            elif i == 4:
                self.roi5.setPixmap(pm)
                text5 = text
                self.roi5_ocr.setText(tex5)
            elif i == 5:
                self.roi6.setPixmap(pm)
                text6 = text
                self.roi6_ocr.setText(text6)
            elif i == 6:
                self.roi7.setPixmap(pm)
                text7 = text
                self.roi7_ocr.setText(text7)
            elif i == 7:
                self.roi8.setPixmap(pm)
                text8 = text
                self.roi8_ocr.setText(text8)
            elif i == 8:
                self.roi9.setPixmap(pm)
                text9 = text
                self.roi9_ocr.setText(text9)

            i+=1
            # print(text)
            if text:
                text = "NumberPlate: " + text

            cv2.putText(image, text, point, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 0, 200), 2)

        return image

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
'''