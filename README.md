# 📁 Project Files

traffic_counter.py

parking_space_marker.py

parking_space_checker.py

# 1️⃣ traffic_counter.py

Counts vehicles in a traffic video using background subtraction and contour detection.

Features

Reads video file (traffic.mp4)

Detects moving vehicles

Draws bounding boxes around detected vehicles

Displays total vehicle count on screen

Usage
python traffic_counter.py

# 2️⃣ parking_space_marker.py

Used to manually select and save parking space locations on an image.

Features

Loads parking lot image (your.jpg)

Left click → Add parking space

Right click → Remove parking space

Saves selected positions into a file

Usage
python parking_space_marker.py

# 3️⃣ parking_space_checker.py

Checks whether parking spaces are occupied or free using image processing.

Features

Loads parking image (your.jpg)

Reads saved parking positions

Applies thresholding and filtering

Marks:

# 🟢 Green → Free space

# 🔴 Red → Occupied space

Usage
python parking_space_checker.py

# 🛠 Requirements

Python 3.x

OpenCV

NumPy

Install dependencies:

pip install opencv-python numpy

# 📷 Input Files

traffic.mp4 → Traffic video

your.jpg → Parking lot image

points.pkl → Parking slot positions (auto-generated)

# 🎯 Purpose

This project demonstrates:

Vehicle detection and counting

Interactive parking slot selection

Parking occupancy detection

It can be extended for:

Smart parking systems

Real-time camera monitoring

AI-based vehicle detection
