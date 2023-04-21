# Road Lane Detection
This project aims to develop a computer vision system that can accurately detect and track road lanes in real time using a combination of image-processing techniques

## Description
This project involves capturing and decoding a video file, converting the RGB frames to grayscale, reducing noise using a Gaussian filter, detecting edges using the Canny Edge Detector, and defining the region of interest using a polygonal mask. The Hough Line Transform is then applied to detect straight lines in the region of interest. The Probabilistic Hough Line Transform is used to output the extremes of the detected lines, which represent the road lanes in the video.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.

```bash
pip install -r requirements.txt
```

## Usage

```python
python main.py
```

## License

[MIT](https://choosealicense.com/licenses/mit/)