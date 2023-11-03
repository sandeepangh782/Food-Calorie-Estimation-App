import cv2
import numpy as np

# Load YOLO
net = cv2.dnn.readNet("yolov3-tiny_obj_10000.weights", "finalfoodcnn.cfg")

# Specify the classes for object detection
classes = ["bread","half-egg","idli","vada","banana","full-egg"]  # Replace with your custom class names

# Load an image
image = cv2.imread("idli.jpeg")

# Get image dimensions


height, width = image.shape[:2]

# Prepare input blob
blob = cv2.dnn.blobFromImage(image, 1/255, (416, 416), swapRB=True, crop=False)

# Set input blob for the network
net.setInput(blob)

# Get output layer names
output_layers = net.getUnconnectedOutLayersNames()

# Forward pass
outputs = net.forward(output_layers)

# Initialize lists for detected objects
class_ids = []
confidences = []
boxes = []

# Process the outputs
for output in outputs:
    for detection in output:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:  # Adjust the confidence threshold as needed
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)
            
            # Rectangle coordinates
            x = int(center_x - w / 2)
            y = int(center_y - h / 2)
            
            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

# Perform non-maximum suppression
indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)  # Adjust thresholds if needed
print(len(boxes))
# Draw bounding boxes and labels
for i in range(len(boxes)):
    if i in indexes:
        x, y, w, h = boxes[i]
        label = classes[class_ids[i]]
        confidence = confidences[i]
        color = (0, 255, 0)  # BGR color for bounding box (green)
        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
        cv2.putText(image, f"{label}: {confidence:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

# Display the result

cv2.imshow("Custom Object Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
