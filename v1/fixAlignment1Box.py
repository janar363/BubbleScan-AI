import cv2
import os
import numpy as np

# Alignment check with Center box

def find_center_box(image_path):

    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours based on their area
    contours = [c for c in contours if cv2.boundingRect(c)[1] < gray.shape[0] * 0.1]
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    
    # Identifing the Center box by aspect ratio and position
    center_box = None
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = w / float(h)
        if 2 < aspect_ratio < 10:
            center_box = cnt
            break

    if center_box is not None:
        x, y, w, h = cv2.boundingRect(center_box)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return center_box
    else:
        print("Center box not found.")
        return None


def rotate_image_based_on_center_box(image_path, center_box):
    image = cv2.imread(image_path)

    # minAreaRect around the center box
    rect = cv2.minAreaRect(center_box)
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    # longest edge of the Center box
    edge_lengths = [np.linalg.norm(box[i] - box[(i + 1) % 4]) for i in range(4)]
    longest_edge_index = np.argmax(edge_lengths)
    longest_edge = (box[longest_edge_index], box[(longest_edge_index + 1) % 4])

    # Calculating the angle of the longest edge relative to the horizontal
    dx, dy = longest_edge[1][0] - longest_edge[0][0], longest_edge[1][1] - longest_edge[0][1]
    angle = np.degrees(np.arctan2(dy, dx))

    if angle < -45:
        angle += 180
    elif angle > 135:
        angle -= 180

    # Adjusting the angle to determine the correct rotation
    if angle > 45:
        angle -= 90
    elif angle < -45:
        angle += 90

    # Rotation matrix
    center = (image.shape[1] // 2, image.shape[0] // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)

    rotated_image = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return rotated_image



# input_path = 'Image_misaligned3.jpg'

# center_box = find_center_box(input_path)

# if center_box is not None:
#     rotated_image = rotate_image_based_on_center_box(input_path, center_box)

#     cv2.imshow('Rotated Image', rotated_image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

#     output_path = 'rotated_image.jpg'
#     cv2.imwrite(output_path, rotated_image)
# else:
#     print("Could not find Center box to base the rotation on.")


def process_folder(folder_path):

    all_files = os.listdir(folder_path)
    
    image_files = [file for file in all_files if file.lower().endswith(('.jpg','.png'))]

    output_folder = os.path.join(folder_path, 'rotatedImages')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        print(f'Processing {image_path}')
        
        center_box = find_center_box(image_path)
        
        if center_box is not None:
            rotated_image = rotate_image_based_on_center_box(image_path, center_box)
            
            # Saving the rotated image
            name, ext = os.path.splitext(image_file)
            output_path = os.path.join(output_folder, f'{name}_rotated{ext}')
            cv2.imwrite(output_path, rotated_image)
            print(f'Saved rotated image to {output_path}')
        else:
            print("Could not find both center box and bottom box to base the rotation on for image:", image_path)

folder_path = 'testAlignment'
process_folder(folder_path)