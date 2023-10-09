import numpy as np
import tensorflow as tf
import os
import cv2
from base2designs.utils import label_map_util


TRAINED_MODEL_DIR = "E:/Projects/Automatic Number Plate/Trained_model/experiment_ssd/exported_model"
PATH_TO_CKPT = TRAINED_MODEL_DIR + "/frozen_inference_graph.pb"
PATH_TO_LABELS = TRAINED_MODEL_DIR + "/classes.pbtxt"
NUM_CLASSES = 37


# load label map using utils provided by tensorflow object detection api
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
#print(label_map)

categories = label_map_util.convert_label_map_to_categories(
    label_map=label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
#print(categories)

# Creates dictionary of COCO compatible categories keyed by category id
category_index = label_map_util.create_category_index(categories)
#print(category_index)

def load_inference_graph():
    # load frozen tensorflow model into memory

    print("> ====== Loading frozen graph into memory")
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
        sess = tf.Session(graph=detection_graph)
    print(">  ====== Inference graph loaded.")
    return detection_graph, sess

# Show fps value on image
def draw_text_on_image(fps, image_np):
    cv2.putText(image_np, "FPS : " + str("{0:.2f}".format(fps)),
                (20,70), cv2.FONT_HERSHEY_SIMPLEX, 2, (77,255,9), 5)

class Predicter():

    def __init__(self, detection_graph, sess):

        self.sess = sess
        self.imageTensor = detection_graph.get_tensor_by_name("image_tensor:0")
        self.boxesTensor = detection_graph.get_tensor_by_name("detection_boxes:0")
        self.scoresTensor = detection_graph.get_tensor_by_name("detection_scores:0")
        self.classesTensor = detection_graph.get_tensor_by_name("detection_classes:0")
        self.numDetections = detection_graph.get_tensor_by_name("num_detections:0")


    def predictPlates(self, image):

        image_tf = np.expand_dims(image, axis=0)

        (boxes, scores, labels, num) = self.sess.run(
            [self.boxesTensor, self.scoresTensor, self.classesTensor, self.numDetections],
            feed_dict = {self.imageTensor : image_tf})

        # squeeze the lists into a single dimension, when we want to remove single-dimensional entries from the shape of an array
        boxes = np.squeeze(boxes)
        scores = np.squeeze(scores)
        labels = np.squeeze(labels)

        return boxes, scores, labels


    def draw_box_on_image(self, score_thresh, num_vehicles_detect, scores, boxes, classes, im_width, im_height, image_np):

        for i in range(num_vehicles_detect):
            
            if scores[i] >= score_thresh:

                if classes[i] == 1:
                    id = "Plate"
                    color0 = (0, 153, 153)
                else:
                    id = "Not Plate"
                    color0 = (0, 255, 0)


                y_min, x_min, y_max, x_max = (boxes[i][0] * im_height, boxes[i][1] * im_width,
                                              boxes[i][2] * im_height, boxes[i][3] * im_width)

                p1 = (int(x_min), int(y_min))
                p2 = (int(x_max), int(y_max))
                p3 = (int(x_min), int(y_min - 40))
                p4 = (int(x_max), int(y_min-6))

                cv2.rectangle(image_np, pt1=p1, pt2=p2, color=color0, thickness=2)
                cv2.rectangle(image_np, pt1=p3, pt2=p4, color=color0, thickness=-1)

                cv2.putText(image_np, id+ ": " + str(i), (int(x_min), int(y_min - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,0,200), 2)
                cv2.putText(image_np, "Confidence: " + str(np.round(scores[i], 2)), (int(x_min), int(y_min-25)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,0,200), 2)

        return image_np
