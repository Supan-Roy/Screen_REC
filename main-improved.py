import datetime
import cv2
import numpy as np
from PIL import ImageGrab
from win32api import GetSystemMetrics
import time

# Screen size
width = GetSystemMetrics(0)
height = GetSystemMetrics(1)

# Timestamped filename
time_stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
file_name = f"recording_{time_stamp}.mp4"

# Video writer setup
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(file_name, fourcc, 20.0, (width, height))

# Open webcam
webcam = cv2.VideoCapture(0)
if not webcam.isOpened():
    print("⚠️ Warning: Could not access webcam.")
    webcam = None

# Frame rate control
desired_fps = 20
frame_duration = 1 / desired_fps

print("🎥 Recording started. Press 'q' to stop.")

try:
    while True:
        start_time = time.time()

        # Capture screen
        screen = ImageGrab.grab(bbox=(0, 0, width, height))
        screen_np = np.array(screen)
        frame = cv2.cvtColor(screen_np, cv2.COLOR_BGR2RGB)

        # Add webcam overlay if available
        if webcam:
            ret, cam_frame = webcam.read()
            if ret:
                cam_small = cv2.resize(cam_frame, (320, 240))
                frame[0:240, 0:320] = cam_small

        # Show and write frame
        cv2.imshow("Recording Preview", frame)
        out.write(frame)

        # Break on 'q' key
        if cv2.waitKey(1) == ord('q'):
            print("🛑 Stopped recording.")
            break

        # Control the loop to match desired FPS
        elapsed = time.time() - start_time
        if elapsed < frame_duration:
            time.sleep(frame_duration - elapsed)

except KeyboardInterrupt:
    print("⏹️ Interrupted by user.")

finally:
    out.release()
    if webcam:
        webcam.release()
    cv2.destroyAllWindows()
