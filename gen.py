# Import necessary libraries
import cv2
import numpy as np

# Load belt data from a CSV file
belt_data = np.loadtxt("data/belt_data.csv", delimiter=",")

# Constants for belt and scanner copied from gen.py
belt_distance_mm = 1200.0 
points_per_scan_x = 640  
total_scans = 640 * 100
defect_depth = 5.0

# Constants for visualization copied from gen.py
scans_to_display = 1000
max_defect_mm = 10

# Update the belt data for visualization
def update_belt_data(belt_data, current_scan):
    return belt_data[current_scan - scans_to_display:current_scan, :]

# Visualize the belt data
def visualize_belt_data(belt_data, scan_number):
    if belt_data.shape[0] < scans_to_display:
        print("Not enough data to display")
        exit()

    # Print information about the current frame
    print("-----FRAME START-----")
    print("belt_data.shape, belt_data.dtype", belt_data.shape, belt_data.dtype)
    print("max, min of belt_data", np.max(belt_data), np.min(belt_data))

    # Normalize the data for visualization
    normalized_data = (belt_data - (belt_distance_mm - max_defect_mm)) / (2 * max_defect_mm)
    print("normalized_data.shape, normalized_data.dtype", normalized_data.shape, normalized_data.dtype)
    print("max, min of normalized_data", np.max(normalized_data), np.min(normalized_data))

    # Apply color mapping to visualize defects
    colored_data = cv2.applyColorMap((normalized_data * 255).astype(np.uint8), cv2.COLORMAP_JET)
    print("colored_data.shape, colored_data.dtype", colored_data.shape, colored_data.dtype)
    print("max, min of colored_data", np.max(colored_data), np.min(colored_data))
    print("-----FRAME END-----\n\n")

    # Add scan number to the visualization
    cv2.putText(colored_data, f"Scan: {scan_number}", (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Display the visualization
    cv2.imshow('Belt Scanner Visualization', colored_data)

    # Wait for a key press and exit if any key is pressed
    if cv2.waitKey(1) > 0:
        exit()

# Visualization loop
for current_scan in range(scans_to_display, total_scans + 1):
    visible_belt_data = update_belt_data(belt_data, current_scan)
    visualize_belt_data(visible_belt_data, current_scan)

# Close all OpenCV windows
cv2.destroyAllWindows()
