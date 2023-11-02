import cv2
import numpy as np
import conveyor

# Function to calculate the dominant color in an image
def get_dominant_color(image):
    # Convert image to RGB (OpenCV uses BGR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pixels = np.float32(image.reshape(-1, 3))

    # Using k-means to cluster pixels
    pixels = np.float32(pixels)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(pixels, 1, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Take the first center as the dominant color
    dominant_color = centers[0].astype(int)
    return tuple(dominant_color)

# Function to match the dominant color to the closest color name
def match_color_name(dominant_color):
    colors = {
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'yellow': (255, 255, 0)
    }
    min_distances = {k: np.linalg.norm(np.array(v) - np.array(dominant_color)) for k, v in colors.items()}
    return min(min_distances, key=min_distances.get)

# Open the video capture
cap = cv2.VideoCapture(0)

# Get the size of the video frame
ret, frame = cap.read()
height, width = frame.shape[:2]
center_x, center_y = width // 2, height // 2

# Define the size of the fixed bounding box (100x100)
bbox_size = 100
bbox_top_left = (center_x - bbox_size // 2, center_y - bbox_size // 2)
bbox_bottom_right = (center_x + bbox_size // 2, center_y + bbox_size // 2)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Draw the fixed bounding box centered on the screen
    cv2.rectangle(frame, bbox_top_left, bbox_bottom_right, (255, 255, 255), 2)

    # Extract the region of interest (ROI) within the bounding box
    roi = frame[bbox_top_left[1]:bbox_bottom_right[1], bbox_top_left[0]:bbox_bottom_right[0]]

    # Get the dominant color in the ROI
    dominant_color = get_dominant_color(roi)

    # Match the dominant color to the closest named color
    color_name = match_color_name(dominant_color)

    if color_name == "green":
        conveyor.send_message("g")
    if color_name == "red":
        conveyor.send_message("s")
    if color_name == "blue":
        conveyor.send_message("b")


    # Put the color name text on the frame
    text_position = (center_x - 20, center_y + bbox_size)
    cv2.putText(frame, color_name, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow('Frame with Dominant Color Name', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
