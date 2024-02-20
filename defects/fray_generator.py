import numpy as np
import cv2
import random

def generate_fray(image_size, start_y, end_y, direction='left'):
    # Adjust coordinates from 0-1 to image resolution
    start_y = int(start_y * image_size)
    end_y = int(end_y * image_size)

    mask = np.zeros((image_size, image_size), dtype=np.float32)

    # Start the fray at the leftmost edge
    x_position = 0

    # Loop over the y-axis to generate the fray line
    for y in range(start_y, end_y):
        # Randomly change the x position to simulate the fray
        x_position += random.randint(-1, 1)  # Allow the fray to move left or right
        x_position = max(x_position, 0)  # Keep the fray within the image bounds

        # Everything to the left of the x_position is considered frayed (white)
        # mask[y, :x_position] = 1.0
        if direction == 'left':
            mask[y, :x_position] = 1.0
        elif direction == 'right':
            mask[y, image_size-x_position:] = 1.0


    return mask

# This part will only run if the file is executed directly, not when imported
if __name__ == "__main__":
    image_size = 640  # Resolution of the image
    start_y = random.uniform(0, 0.5)  # Starting y-coordinate in range 0-1
    end_y = random.uniform(0.5, 1)  # Ending y-coordinate in range 0-1

    fray_mask = generate_fray(image_size, start_y, end_y, direction='right')
    fray_mask2 = generate_fray(image_size, start_y, end_y, direction='left')

    cv2.imshow('Fray left', (fray_mask * 255).astype(np.uint8))

    cv2.imshow('Fray right', (fray_mask2 * 255).astype(np.uint8))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
