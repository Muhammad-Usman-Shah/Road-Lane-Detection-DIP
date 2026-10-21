

# Road Lane Detection Using Digital Image Processing

**DIP Semester Project | EE 449L – Digital Image Processing**

Department of Electrical Engineering  
Namal University, Mianwali, Pakistan

## Project Overview

This project detects white and yellow lane markings in road images using digital image processing techniques.

The system uses HSV colour segmentation, thresholding, binary masks and a manually selected Region of Interest (ROI). Detected lane pixels are highlighted in red on the original image.

A Tkinter interface allows users to upload road images and adjust colour thresholds.

## Digital Image Processing Techniques

- RGB to HSV colour space conversion
- White and yellow colour thresholding
- Binary mask generation
- Mask combination
- Polygon-based Region of Interest (ROI)
- Image masking
- Lane pixel highlighting
- Image visualisation

## Processing Steps

1. Upload a road image.
2. Convert the image from RGB to HSV.
3. Apply thresholds for white lane markings.
4. Apply thresholds for yellow lane markings.
5. Combine the binary colour masks.
6. Select the road region using a polygon.
7. Apply the ROI mask.
8. Highlight detected lane pixels in red.
9. Display the processed image.

## Tools and Libraries

- Python
- OpenCV
- NumPy
- Matplotlib
- Tkinter

## Project Files

- [Source Code](Lane_Detection_Source_Code.py.py)
- [Project Report](Lane_Detection_Project_Report.pdf.pdf)
- [Presentation](Lane_Detection_Presentation.pdf.pdf)
- [Detection Results](Lane_Detection_Results.pdf.pdf)
- [Process Flowchart](Lane_Detection_Flowchart.pdf.pdf)

## How to Run

Install the required libraries:

```bash
pip install opencv-python numpy matplotlib
```

Run:

```bash
python DIP_Lane_Detection.py
```

Upload a road image through the interface. Select the road region using the mouse and press Enter to complete the ROI selection.

## Results

The method detects white and yellow lane markings in clear daytime road images, including solid and dashed markings.

Detection becomes less reliable in shadows, poor lighting and areas containing bright objects.

## Limitations

- The ROI must be selected manually.
- Performance depends on lighting and colour conditions.
- The method highlights lane pixels without fitting complete lane boundaries.

## Future Improvements

- Automatic ROI selection
- Canny edge detection
- Hough line transform
- Perspective transformation
- Improved colour thresholding
- Video-based lane detection

## Project Team

- Muhammad Usman Shah
- Muhammad Wajid Jamal

**Submitted to:** Ms. Zulaikha Kiran and Ms. Aliza  
**Course:** EE 449L – Digital Image Processing  
**University:** Namal University, Mianwali
