#@markdown We implemented some functions to visualize the object detection results. <br/> Run the following cell to activate the functions.
import cv2
import numpy as np
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import matplotlib.pyplot as plt


MARGIN = 10  # pixels
ROW_SIZE = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
TEXT_COLOR = (255, 0, 0)  # red
IMAGE_FILE = './assets/img.png'


# def visualize(
#     image,
#     detection_result
# ) -> np.ndarray:
#   """Draws bounding boxes on the input image and return it.
#   Args:
#     image: The input RGB image.
#     detection_result: The list of all "Detection" entities to be visualize.
#   Returns:
#     Image with bounding boxes.
#   """
#   for detection in detection_result.detections:
    
#     bbox = detection.bounding_box
#     start_point = bbox.origin_x, bbox.origin_y
#     end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
#     cv2.rectangle(image, start_point, end_point, TEXT_COLOR, 3)

#     category = detection.categories[0]
#     category_name = category.category_name
#     probability = round(category.score, 2)
#     result_text = category_name + ' (' + str(probability) + ')'
#     text_location = (MARGIN + bbox.origin_x,
#                      MARGIN + ROW_SIZE + bbox.origin_y)
#     cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
#                 FONT_SIZE, TEXT_COLOR, FONT_THICKNESS)

#   return image

# def predict_image():
   
#     base_options = python.BaseOptions(model_asset_path='./models/efficientdet.tflite')
#     options = vision.ObjectDetectorOptions(base_options=base_options,
#                                         score_threshold=0.5)
#     detector = vision.ObjectDetector.create_from_options(options)

#     image = mp.Image.create_from_file(IMAGE_FILE)

#     detection_result = detector.detect(image)

#     detection_of_people = [person for person in detection_result.detections if person.categories[0].category_name == 'person']
#     people_count = len(detection_of_people)
#     print("People count: ",people_count)
#     image_copy = np.copy(image.numpy_view())
#     annotated_image = visualize(image_copy, detection_result)
#     rgb_annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
#     cv2.imwrite('./assets/annotated_img.jpg', rgb_annotated_image)
 


# if __name__ == '__main__':
    
#     predict_image()


class TemplateImg:
  def __init__(self):
    self.img = cv2.imread('./assets/img.png')

  def visualize(self,
    image,
    detection_result
) -> np.ndarray:
    for detection in detection_result.detections:
        
        bbox = detection.bounding_box
        start_point = bbox.origin_x, bbox.origin_y
        end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
        cv2.rectangle(image, start_point, end_point, TEXT_COLOR, 3)

        category = detection.categories[0]
        category_name = category.category_name
        probability = round(category.score, 2)
        result_text = category_name + ' (' + str(probability) + ')'
        text_location = (MARGIN + bbox.origin_x,
                        MARGIN + ROW_SIZE + bbox.origin_y)
        cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                    FONT_SIZE, TEXT_COLOR, FONT_THICKNESS)

    return image
  
  def predict_image(self, model_path: str) -> int:
   
    base_options = python.BaseOptions(model_asset_path=model_path)
    options = vision.ObjectDetectorOptions(base_options=base_options,
                                        score_threshold=0.5)
    detector = vision.ObjectDetector.create_from_options(options)

    image = mp.Image.create_from_file(IMAGE_FILE)

    detection_result = detector.detect(image)

    detection_of_people = [person for person in detection_result.detections if person.categories[0].category_name == 'person']
    people_count = len(detection_of_people)
    print("People count: ",people_count)
    image_copy = np.copy(image.numpy_view())
    annotated_image = self.visualize(image_copy, detection_result)
    rgb_annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
    cv2.imwrite('./assets/annotated_img.jpg', rgb_annotated_image)
    return people_count
 
