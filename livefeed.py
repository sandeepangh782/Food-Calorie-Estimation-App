import cv2
import numpy as np

# Define your custom class names
class_names = ["bread","half-egg","idli","vada","banana","full-egg"]

# Load YOLO weights and configuration
net = cv2.dnn.readNet("yolov3-tiny_obj_final.weights", "finalfoodcnn.cfg")

# Set up the camera
cap = cv2.VideoCapture(0)  # 0 represents the default camera (usually the built-in webcam)

while True:
    ret, frame = cap.read()
    
    if not ret:
        break

    height, width, _ = frame.shape

    # Create a blob from the input frame and set it as the input to the network
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)

    # Get the output layer names
    output_layer_names = net.getUnconnectedOutLayersNames()

    # Run forward pass through the network
    detections = net.forward(output_layer_names)

    # Process each detection
    for detection in detections:
        for obj in detection:
            scores = obj[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:  # Adjust this threshold to control detection sensitivity
                center_x = int(obj[0] * width)
                center_y = int(obj[1] * height)
                w = int(obj[2] * width)
                h = int(obj[3] * height)

                # Calculate bounding box coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                # Draw bounding box and label on the frame using custom class names
                color = (0, 255, 0)  # Green color for the bounding box
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                label = f"{class_names[class_id]}: {confidence:.2f}"
                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Display the resulting frame
    cv2.imshow("Object Detection", frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
