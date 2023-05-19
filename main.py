import cv2
from pyzbar import pyzbar
import pygame

# Initialize pygame
pygame.init()

# Set screen dimensions
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540

# Set volume range
MIN_VOLUME = 0
MAX_VOLUME = 1

# Set tracks
TRACKS = [
    {"path": "ODESZA.mp3", "qr_key": "temp"},
]

# Initialize tracks
track_objects = {}
for track in TRACKS:
    track_path = track["path"]
    track_qr_key = track["qr_key"]
    track_objects[track_qr_key] = pygame.mixer.Sound(track_path).play(-1)

# Create VideoCapture object with RTMP URL
rtmp_url = '192.168.137.172'  # Replace with your RTMP stream URL
# rtmp_url = "rtmp://172.20.10.3:1935/live"  # Replace with your RTMP stream URL
cap = cv2.VideoCapture(2)

# Check if VideoCapture object was successfully initialized
if not cap.isOpened():
    print("Failed to open RTMP stream")
    exit()

# Create named window with specified properties
cv2.namedWindow("camera", cv2.WINDOW_NORMAL)
cv2.resizeWindow("camera", WINDOW_WIDTH, WINDOW_HEIGHT)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to read frame from RTMP stream")
        break
    # Convert the frame to grayscale for QR code detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect QR codes in the frame
    decoded_objects = pyzbar.decode(gray)
    # Loop over the detected QR codes
    for obj in decoded_objects:
        # Extract the bounding box coordinates
        x, y, w, h = obj.rect
        qr_code_data = obj.data.decode("utf-8")

        # Calculate vertical coordinate ratio
        y_ratio = y / WINDOW_HEIGHT
        x_ratio = x / WINDOW_WIDTH

        # Adjust audio volume based on vertical coordinate ratio
        volume = MIN_VOLUME + (MAX_VOLUME - MIN_VOLUME) * y_ratio
        phase = x_ratio
        left_value = volume * (1 - phase)
        right_value = volume * phase

        track_objects.get(qr_code_data).set_volume(left_value, right_value)

        # Draw a green rectangle around the QR code
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Extract and display the QR code data
        cv2.putText(frame, qr_code_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the frame with QR codes
    cv2.imshow("camera", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
