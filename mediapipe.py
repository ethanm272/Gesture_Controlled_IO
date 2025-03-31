import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import time
import pyautogui as pag
import mouse_controller

# Designate and set path to model
model_path = '/Users/ethanmylett/Projects/Gesture_Controlled_IO/gesture_recognizer.task'
base_options = mp.tasks.BaseOptions(model_asset_path=model_path)

# Initialize option variables
BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# Mouse Controller
MOUSE_MOVEMENT_GESTURE = 'Pointing_Up'
mc = mouse_controller.mouse_controller(MOUSE_MOVEMENT_GESTURE, round(1000 * time.time()))

# Callback function
def show_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    if (len(result.gestures) == 0):
        return # if no hand detected
        
    mc.move_mouse((result.hand_landmarks[0][8].x, result.hand_landmarks[0][8].y), result.gestures[0][0].category_name, timestamp_ms)

options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=show_result)

with GestureRecognizer.create_from_options(options) as rec:
    video = cv2.VideoCapture(0)
    
    while (True):
        # Get timestamp
        ts = round(1000 * time.time())

        # Capture frame
        ret, frame = video.read()

        # Convert frame to MediaPipe image object
        mp_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

        # Send image to perform recognition
        rec.recognize_async(mp_frame, ts)

        # Show frame
        cv2.imshow('Gesture Recognition', frame)

        # Quit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break;
