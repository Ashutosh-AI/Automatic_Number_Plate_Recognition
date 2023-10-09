import cv2

from base2designs.utils import detector_utils
from base2designs.utils.detector_utils import Predicter
from base2designs.plates.plateFinder import PlateFinder
from base2designs.plates.plateDisplay import PlateDisplay
from base2designs.utils import ocr

detection_graph, sess = detector_utils.load_inference_graph()


if __name__ == "__main__":

    #imagePath = input("Please enter Image path")
    imagePath = "images/anpr.jpg"
    img = cv2.imread(imagePath)
    im_height, im_width = img.shape[:2]
    score_thresh = 0.10
    num_vehicles_detect = 20

    plateFinder = PlateFinder(score_thresh, detector_utils.category_index)
    predicter = Predicter(detection_graph, sess)
    plate_display = PlateDisplay()

    boxes, scores, labels = predicter.predictPlates(img)

    licensePlateFound_pred, plateBoxes_pred, plateScores_pred = plateFinder.findPlatesOnly(boxes, scores, labels)

    cropped_img = plate_display.getBoundingBox(img, plateBoxes_pred, imagePath)

    img = predicter.draw_box_on_image(score_thresh=score_thresh, num_vehicles_detect=num_vehicles_detect, scores=scores, boxes=boxes,
                                classes=labels,im_width=im_width, im_height=im_height, image_np=img)

    img = ocr.ocr_on_image(img, plateBoxes_pred, im_height, im_width)

    cv2.imwrite("images/detect_plate/"+"detect_"+ imagePath.split("/")[-1], img)
    cv2.namedWindow("Detection", cv2.WINDOW_NORMAL)
    cv2.imshow("Detection", img)
    if cv2.waitKey(5000) & 0xFF == ("q"):
        cv2.destroyAllWindows()
