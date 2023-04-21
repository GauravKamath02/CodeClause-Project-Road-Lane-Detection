import cv2
import os

# Open the video file
video = cv2.VideoCapture('sample.mp4')

# Create a directory to save the frames
os.makedirs('frames', exist_ok=True)

# Loop over all frames in the video
frame_num = 0
while True:
    # Read the next frame from the video
    ret, frame = video.read()

    # If the frame is empty, we've reached the end of the video
    if not ret:
        break

    # Save the frame as an image file
    filename = f'frame_{frame_num:04d}.png'
    filepath = os.path.join('frames', filename)
    cv2.imwrite(filepath, frame)

    # Increment the frame number
    frame_num += 1

# Release the video object and close all windows
video.release()
cv2.destroyAllWindows()
