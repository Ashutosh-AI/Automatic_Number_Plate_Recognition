import datetime
from datetime import date
import glob
import cv2
from imutils.video import VideoStream
from base2designs.utils import detector_utils
from base2designs.utils.detector_utils import Predicter
from base2designs.plates.plateFinder import PlateFinder
from base2designs.plates.plateDisplay import PlateDisplay
from base2designs.utils import ocr

detection_graph, sess = detector_utils.load_inference_graph()


if __name__ == "__main__":

    vs = VideoStream("traffic.mp4").start()
    #vs = cv2.VideoCapture(0)
    cv2.namedWindow("Detection", cv2.WINDOW_NORMAL)

    #out = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*"MJPG"), 5.0, (640,480))

    start_time = datetime.datetime.now()
    num_frames = 0
    score_thresh = 0.60
    num_vehicles_detect = 20

    try:
        while True:
            frame = vs.read()
            print(frame.shape)

            im_height, im_width = frame.shape[:2]

            # Convert image to RGB, opencv reads BGR formats
            try:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            except:
                print("Error Converting to RGB Format")


            plateFinder = PlateFinder(score_thresh, detector_utils.category_index)
            predicter = Predicter(detection_graph, sess)
            plate_display = PlateDisplay()

            boxes, scores, labels = predicter.predictPlates(frame)

            licensePlateFound_pred, plateBoxes_pred, plateScores_pred = plateFinder.findPlatesOnly(boxes, scores, labels)

            #cropped_img = plate_display.getBoundingBox(frame, plateBoxes_pred, imagePath)

            frame = predicter.draw_box_on_image(score_thresh=score_thresh, num_vehicles_detect=num_vehicles_detect, scores=scores,
                                      boxes=boxes, classes=labels, im_width=im_width, im_height=im_height, image_np=frame)

            frame = ocr.ocr_on_image(frame, plateBoxes_pred, im_height, im_width)

            num_frames +=1
            elapsed_time = (datetime.datetime.now() - start_time).total_seconds()
            fps = num_frames/elapsed_time
            detector_utils.draw_text_on_image(fps, frame)

            #out.write(frame)
            cv2.imshow("Detection", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            if cv2.waitKey(1) & 0xFF == ("q"):
                cv2.destroyAllWindows()
                vs.stop()
                break


        print("Average FPS: ", str("{0:.2f}".format(fps)))

    except KeyboardInterrupt:
        today = date.today()
        print("Average FPS: ", str("{0:.2f}".format(fps)))