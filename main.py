import cv2
import numpy as np



def detect_lane(image, canny_threshold_low = 50, canny_threshold_high = 150, hough_threshold = 50, rho = 2, theta = np.pi/180, min_line_length = 40, max_line_gap = 20):
    # convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # apply Gaussian blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # apply Canny edge detection
    edges = cv2.Canny(blur, canny_threshold_low, canny_threshold_high)

    # define region of interest
    height, width = edges.shape[:2]
    vertices = np.array([[(0, height), (width/2, height/2), (width, height)]], dtype=np.int32)
    mask = np.zeros_like(edges)
    cv2.fillPoly(mask, vertices, 255)
    masked_edges = cv2.bitwise_and(edges, mask)

    # detect lines using Hough transform
    lines = cv2.HoughLinesP(masked_edges, rho, theta, hough_threshold, np.array([]),
                            minLineLength=min_line_length, maxLineGap=max_line_gap)

    # separate lines into left and right lanes
    left_lines = []
    right_lines = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if x2 == x1:
            continue  # ignore vertical lines
        slope = (y2 - y1) / (x2 - x1)
        if slope < 0:
            left_lines.append(line)
        else:
            right_lines.append(line)

    # fit lines to left and right lanes using least squares
    def fit_lane(lines):
        x = []
        y = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            x += [x1, x2]
            y += [y1, y2]
        if len(x) == 0:
            return None
        fit = np.polyfit(x, y, 1)
        return fit

    left_fit = fit_lane(left_lines)
    right_fit = fit_lane(right_lines)

    # draw lanes on original image
    if left_fit is not None and right_fit is not None:
        y1 = height
        y2 = int(height/2 + 50)
        left_x1 = int((y1 - left_fit[1]) / left_fit[0])
        left_x2 = int((y2 - left_fit[1]) / left_fit[0])
        right_x1 = int((y1 - right_fit[1]) / right_fit[0])
        right_x2 = int((y2 - right_fit[1]) / right_fit[0])
        cv2.line(image, (left_x1, y1), (left_x2, y2), (0, 255, 0), 10)
        cv2.line(image, (right_x1, y1), (right_x2, y2), (0, 255, 0), 10)
    
    return image


if __name__ == "__main__":
    cap = cv2.VideoCapture('sample.mp4')
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        output = detect_lane(frame)
        cv2.imshow('output', output)
        if cv2.waitKey(1) == ord('q'):
            break
    # Cleanup
    cap.release()
    cv2.destroyAllWindows