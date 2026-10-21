"""
Road Lane Detection Using Digital Image Processing

Lab semester project for EE 449L, Digital Image Processing.
Namal University Mianwali, Department of Electrical Engineering.

What this program does:
1. Opens a small window where you pick a road photo.
2. Finds white and yellow lane markings using HSV colour thresholds.
3. Lets you click a polygon around the road so the background is ignored.
4. Paints the detected lane pixels red on the original photo.

You need opencv, numpy and matplotlib installed to run it.
Tkinter comes with most Python installs.
"""

import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
import matplotlib.pyplot as plt

# This holds the path of the image the user picked.
# It stays empty until they click the upload button.
file_path = None


# ===============================
# Upload Image
# ===============================
def upload_image():
    # We change the global path so process_image can use it later.
    global file_path

    # Open the normal file picker window.
    file_path = filedialog.askopenfilename(title="Select an image")

    # Show only the file name under the button, not the whole path.
    path_label.config(text=file_path.split("/")[-1])


# ===============================
# Process Image
# ===============================
def process_image():
    # Stop early if the user forgot to pick an image.
    if not file_path:
        print("No image selected")
        return

    # OpenCV reads images in BGR order.
    img = cv2.imread(file_path)

    # Matplotlib expects RGB, so we make a copy in that order for display.
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Convert to HSV because colours are easier to separate there.
    # H is the colour type, S is how pure it is, V is how bright it is.
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Divide by 255 to bring the channels to a small decimal scale.
    # OpenCV hue only goes up to 179, so H ends up near 0.7 at most.
    # The yellow thresholds in the GUI were chosen on this scale.
    H = hsv[:, :, 0] / 255
    S = hsv[:, :, 1] / 255
    V = hsv[:, :, 2] / 255

    # Read the white thresholds typed into the GUI.
    white_s = float(whiteS_entry.get())
    white_v = float(whiteV_entry.get())

    # Read the yellow thresholds typed into the GUI.
    h_min = float(yellowHmin_entry.get())
    h_max = float(yellowHmax_entry.get())
    s_min = float(yellowS_entry.get())
    v_min = float(yellowV_entry.get())

    # White paint has low saturation and high brightness.
    whiteMask = (S < white_s) & (V > white_v)

    # Yellow paint sits inside a hue range and needs enough colour and light.
    yellowMask = (H >= h_min) & (H <= h_max) & (S >= s_min) & (V >= v_min)

    # A pixel counts as a lane candidate if it is white or yellow.
    colorMask = whiteMask | yellowMask

    # Next comes the region of interest.
    # Show the image so the user can mark the road area.
    # Left click adds a point. Press Enter or middle click to finish.
    plt.figure()
    plt.imshow(img_rgb)
    plt.title("Select ROI (click points, press Enter to finish)")
    roi_points = plt.ginput(n=-1, timeout=0)
    plt.close()

    # A polygon needs at least three corners.
    if len(roi_points) < 3:
        print("ROI not selected properly")
        return

    # Turn the clicked points into whole pixel positions.
    roi_points = np.array(roi_points, dtype=np.int32)

    # Start with a black image and fill the chosen polygon with ones.
    roi_mask = np.zeros(img.shape[:2], dtype=np.uint8)
    cv2.fillPoly(roi_mask, [roi_points], 1)

    # Change it to True and False so we can combine it with other masks.
    roi_mask = roi_mask.astype(bool)

    # Keep only the lane coloured pixels that are inside the road area.
    finalMask = colorMask & roi_mask

    # Paint those pixels pure red on a copy of the original image.
    finalOutput = img_rgb.copy()
    finalOutput[finalMask] = [255, 0, 0]

    # Finally we show every step in one window.
    # It has six panels, two per row.
    plt.figure(figsize=(15, 10))

    # Panel 1: the photo we started with.
    plt.subplot(3, 2, 1)
    plt.imshow(img_rgb)
    plt.title("Original Image")
    plt.axis("off")

    # Panel 2: everything the white rule picked up.
    plt.subplot(3, 2, 2)
    plt.imshow(whiteMask, cmap='gray')
    plt.title("White Mask")
    plt.axis("off")

    # Panel 3: everything the yellow rule picked up.
    plt.subplot(3, 2, 3)
    plt.imshow(yellowMask, cmap='gray')
    plt.title("Yellow Mask")
    plt.axis("off")

    # Panel 4: white and yellow joined together.
    plt.subplot(3, 2, 4)
    plt.imshow(colorMask, cmap='gray')
    plt.title("Combined Mask")
    plt.axis("off")

    # Panel 5: the road area the user selected.
    plt.subplot(3, 2, 5)
    plt.imshow(roi_mask, cmap='gray')
    plt.title("ROI Mask")
    plt.axis("off")

    # Panel 6: the final answer with lanes in red.
    plt.subplot(3, 2, 6)
    plt.imshow(finalOutput)
    plt.title("Final Output (Red Detection)")
    plt.axis("off")

    # Stop the panels from overlapping, then open the window.
    plt.tight_layout()
    plt.show()


# ===============================
# GUI Layout
# ===============================
# Main window
root = Tk()
root.title("HSV Threshold Configuration Panel")
root.geometry("420x420")
root.resizable(False, False)

# Heading at the top
Label(root, text="HSV Color Threshold Configuration",
      font=("Arial", 12, "bold")).pack(pady=8)

# Upload button and a small label that shows the chosen file name
Button(root, text="Upload Image", command=upload_image).pack()
path_label = Label(root, text="No file selected", fg="gray")
path_label.pack(pady=3)


# ===============================
# White Mask Section
# ===============================
Label(root, text="White Color Conditions",
      font=("Arial", 10, "bold")).pack(pady=6)

# A frame keeps the labels and boxes lined up in a grid.
frame_white = Frame(root)
frame_white.pack()

# Saturation must be below this value. Default is 0.30.
Label(frame_white, text="S").grid(row=0, column=0)
Label(frame_white, text="<").grid(row=0, column=1)
whiteS_entry = Entry(frame_white, width=8)
whiteS_entry.grid(row=0, column=2, padx=5)
whiteS_entry.insert(0, "0.30")

# Brightness must be above this value. Default is 0.70.
Label(frame_white, text="V").grid(row=1, column=0)
Label(frame_white, text=">").grid(row=1, column=1)
whiteV_entry = Entry(frame_white, width=8)
whiteV_entry.grid(row=1, column=2, padx=5)
whiteV_entry.insert(0, "0.70")


# ===============================
# Yellow Mask Section
# ===============================
Label(root, text="Yellow Color Conditions",
      font=("Arial", 10, "bold")).pack(pady=8)

frame_yellow = Frame(root)
frame_yellow.pack()

# Lowest hue allowed. Default is 0.024.
Label(frame_yellow, text="H").grid(row=0, column=0)
Label(frame_yellow, text="≥").grid(row=0, column=1)
yellowHmin_entry = Entry(frame_yellow, width=8)
yellowHmin_entry.grid(row=0, column=2, padx=5)
yellowHmin_entry.insert(0, "0.024")

# Highest hue allowed. Default is 0.196.
Label(frame_yellow, text="H").grid(row=1, column=0)
Label(frame_yellow, text="≤").grid(row=1, column=1)
yellowHmax_entry = Entry(frame_yellow, width=8)
yellowHmax_entry.grid(row=1, column=2, padx=5)
yellowHmax_entry.insert(0, "0.196")

# Lowest saturation allowed. Default is 0.314.
Label(frame_yellow, text="S").grid(row=2, column=0)
Label(frame_yellow, text="≥").grid(row=2, column=1)
yellowS_entry = Entry(frame_yellow, width=8)
yellowS_entry.grid(row=2, column=2, padx=5)
yellowS_entry.insert(0, "0.314")

# Lowest brightness allowed. Default is 0.314.
Label(frame_yellow, text="V").grid(row=3, column=0)
Label(frame_yellow, text="≥").grid(row=3, column=1)
yellowV_entry = Entry(frame_yellow, width=8)
yellowV_entry.grid(row=3, column=2, padx=5)
yellowV_entry.insert(0, "0.314")


# ===============================
# Process Button
# ===============================
# Green button that starts the detection.
Button(root, text="Run Detection",
       bg="#2E8B57", fg="white",
       font=("Arial", 10, "bold"),
       command=process_image).pack(pady=15)

# Keep the window open and wait for the user.
root.mainloop()
