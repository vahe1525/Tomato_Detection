import cv2 as cv
import numpy as np

# Constants.
INPUT_WIDTH = 640
INPUT_HEIGHT = 640
SCORE_THRESHOLD = 0.5
NMS_THRESHOLD = 0.45
CONFIDENCE_THRESHOLD = 0.45

# Text parameters.
FONT_FACE = cv.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.2
THICKNESS = 1

# Colors.
BLACK  = (0, 0, 0)
BLUE   = (255, 178, 50)
RED   = (0, 0, 255)
GREEN   = (0, 255, 0)
YELLOW = (0, 255, 255)

class Position:
    def __init__(self):
        self.PosX = 0
        self.PosY = 0

def draw_cross(im, x, y, size=3, color=GREEN, thickness=2):
    """Draw a cross at location (x, y) with the specified size, color, and thickness."""
    cv.line(im, (x - size, y - size), (x + size, y + size), color, thickness)
    cv.line(im, (x + size, y - size), (x - size, y + size), color, thickness)

def pre_process(input_image, net):
    # Create a 4D blob from a frame.
    blob = cv.dnn.blobFromImage(input_image, 1/255, (INPUT_WIDTH, INPUT_HEIGHT), [0, 0, 0], 1, crop=False)
    # Set the input to the network.
    net.setInput(blob)
    # Run the forward pass to get output of the output layers.
    outputs = net.forward(net.getUnconnectedOutLayersNames())
    return outputs

# Colors for different classes.
COLOR_MAP = {
    0: (0, 255, 0),  # Green for riped tomato
    1: (0, 0, 255)   # Red for unriped tomato
}

def post_process(input_image, outputs):
    # Lists to hold respective values while unwrapping.
    class_ids = []
    confidences = []
    boxes = []
    tomato_positions = []  # List to store the Position objects

    # Rows.
    rows = outputs[0].shape[1]
    image_height, image_width = input_image.shape[:2]
    # Resizing factor.
    x_factor = image_width / INPUT_WIDTH
    y_factor = image_height / INPUT_HEIGHT
    # Iterate through detections.
    for r in range(rows):
        row = outputs[0][0][r]
        confidence = row[4]
        # Discard bad detections and continue.
        if confidence >= CONFIDENCE_THRESHOLD:
            classes_scores = row[5:]
            # Get the index of max class score.
            class_id = np.argmax(classes_scores)
            # Continue if the class score is above threshold.
            if classes_scores[class_id] > SCORE_THRESHOLD:
                confidences.append(confidence)
                class_ids.append(class_id)
                cx, cy, w, h = row[0], row[1], row[2], row[3]
                left = int((cx - w / 2) * x_factor)
                top = int((cy - h / 2) * y_factor)
                width = int(w * x_factor)
                height = int(h * y_factor)
                box = np.array([left, top, width, height])
                boxes.append(box)
    
    indices = cv.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
    for i in indices:
        if confidences[i] > 0.80:
            box = boxes[i]
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]
            # Calculate the center coordinates of the bounding box
            center_x = left + width // 2
            center_y = top + height // 2
            
            # Create a Position object and store the coordinates
            position = Position()
            position.PosX = int(center_x)
            position.PosY = int(center_y)
            tomato_positions.append(position)
    
    return tomato_positions  # Return the list of Position objects

def start():
    # Load class names.
    classes = ["riped tomato", "unriped tomato", "diseased"]
    # Give the weight files to the model and load the network using them.
    modelWeights = "best.onnx"
    net = cv.dnn.readNet(modelWeights)
    cap = cv.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Process image.
        detections = pre_process(frame, net)
        tomato_positions = post_process(frame.copy(), detections)

        # Optional: You can draw the crosses on the frame if you want to visualize the detections
        for pos in tomato_positions:
            draw_cross(frame, pos.PosX, pos.PosY)

        # Optional: Display the frame
        t, _ = net.getPerfProfile()
        label = 'Inference time: %.2f ms' % (t * 1000.0 / cv.getTickFrequency())
        cv.putText(frame, label, (20, 40), FONT_FACE, FONT_SCALE, (0, 0, 255), THICKNESS, cv.LINE_AA)

        window_name = 'Output'
        cv.namedWindow(window_name, cv.WINDOW_NORMAL)
        cv.resizeWindow(window_name, frame.shape[1], frame.shape[0])

        cv.imshow(window_name, frame)
        if cv.waitKey(1) == ord('x'):
            break

        # Break after processing one frame to return the list
        cap.release()
        cv.destroyAllWindows()
        return tomato_positions  # Return the list of positions

    cap.release()
    cv.destroyAllWindows()
    return []

#if __name__ == '__main__':
 #   positions = start()
  #  for pos in positions:
   #     print(f"Tomato Position - X: {pos.PosX}, Y: {pos.PosY}")

