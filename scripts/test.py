import cv2
from ultralytics import YOLO

from functions import detected_boxes_with_resize

# model = YOLO('models/guinea-pig-v3+chons.pt')
model = YOLO('models/guinea-pig-v3+chons+camera-v1.pt')

# img = cv2.imread('datasets/test/315534888_863531564803278_2461991379783231489_n.jpg')
img = cv2.imread('datasets/test/Camera_screenshot_04.06.2024.png')

results = model(img)

img = detected_boxes_with_resize(model, img, results, 1024, 768)

cv2.imshow("Image", img)
cv2.waitKey(0)

cv2.destroyAllWindows()
