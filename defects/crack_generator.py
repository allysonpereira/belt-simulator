import numpy as np
import cv2
import random

def generate_random_walk_crack(image_size, start_x, start_y, end_y, thickness, rotation_angle):
    # Convert relative coordinates to absolute pixel values
    start_x = int(start_x * image_size)
    start_y = int(start_y * image_size)
    end_y = int(end_y * image_size)
    thickness = int(thickness * image_size)

    # Create an empty mask for the crack
    mask = np.zeros((image_size, image_size), dtype=np.float32)
    x = start_x

    # Adjust the step size based on the thickness to maintain roughness
    min_step = 1
    max_step = max(1, thickness // 2)  # Ensure max_step is at least 1
    
    # Generate a random walk to create a crack
    for y in range(start_y, end_y):
        step = random.randint(min_step, max_step) * random.choice([-1, 1])
        x += step
        x = np.clip(x, 0, image_size - 1)

        # Draw overlapping shapes to create a thicker and rougher line
        for thick_y in range(y - thickness // 2, y + thickness // 2 + 1):
            for thick_x in range(x - thickness // 2, x + thickness // 2 + 1):
                if 0 <= thick_x < image_size and 0 <= thick_y < image_size:
                    mask[thick_y, thick_x] = 1.0
    
    # Rotate the crack if specified
    if rotation_angle != 0:
        center = (image_size // 2, image_size // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, rotation_angle, 1.0)
        mask = cv2.warpAffine(mask, rotation_matrix, (image_size, image_size), flags=cv2.INTER_LINEAR)

    return mask

def apply_distance_transform(mask):
    # Convert mask to uint8 format
    mask_uint8 = (mask * 255).astype(np.uint8)
    
    # Apply distance transform to the mask
    dist_transform = cv2.distanceTransform(mask_uint8, cv2.DIST_L2, 3)
    
    # Normalize the distance transform to the range [0, 1]
    dist_transform_normalized = np.zeros_like(dist_transform)
    cv2.normalize(dist_transform, dist_transform_normalized, 0, 1, cv2.NORM_MINMAX)
    
    return dist_transform_normalized

def display_cracks(random_walk_crack, distance_transformed_crack):
    # Convert masks to uint8 format for display
    random_walk_crack_display = (random_walk_crack * 255).astype(np.uint8)
    distance_transformed_crack_display = (distance_transformed_crack * 255).astype(np.uint8)

    # Display the random walk crack and the distance transformed crack
    cv2.imshow('Random Walk Crack', random_walk_crack_display)
    cv2.imshow('Distance Transformed Crack', distance_transformed_crack_display)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Parameters for crack generation
    image_size = 640
    start_x = 0.5
    start_y = 0.5
    end_y = 0.85
    line_thickness = 0.015
    rotation_angle = random.randint(0, 180)

    # Generate random walk crack
    random_walk_crack = generate_random_walk_crack(image_size, start_x, start_y, end_y, line_thickness, rotation_angle)
    
    # Apply distance transform to the random walk crack
    distance_transformed_crack = apply_distance_transform(random_walk_crack)
    
    # Display the generated cracks
    display_cracks(random_walk_crack, distance_transformed_crack)
