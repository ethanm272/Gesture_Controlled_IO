import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import time

# Designate and set path to model
model_path = '/Users/ethanmylett/Projects/Gesture_Controlled_IO/gesture_recognizer.task'
base_options = mp.tasks.BaseOptions(model_asset_path=model_path)

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# Create a gesture recognizer instance with the live stream mode:
def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    print('gesture recognition result: {}'.format(result))

def show_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    pass

options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)
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
        rec_result = rec.recognize_async(mp_frame, ts)

        # Quit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break;
