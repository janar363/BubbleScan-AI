import cv2
import os
import numpy as np

# Alignment check with Center box and Bottom box

def find_boxes(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours based on their area
    contours = [c for c in contours if cv2.boundingRect(c)[1] < gray.shape[0] * 1.0]
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # Identifying the center box and bottom box by aspect ratio and position
    center_box = None
    bottom_box = None

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = w / float(h)
        area = w * h

        if y < gray.shape[0] * 0.4 and 2 < aspect_ratio < 10:
            if center_box is None:
                center_box = cnt

        if y > gray.shape[0] * 0.6 and 1 < aspect_ratio < 8 and h > 70:
                bottom_box = cnt
               # print("Height  of Bottom Box : ",h)
                

        if center_box is not None and bottom_box is not None:
            break

    if center_box is not None:
        x, y, w, h = cv2.boundingRect(center_box)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if bottom_box is not None:
        x, y, w, h = cv2.boundingRect(bottom_box)
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # cv2.imshow('Input Image with Bounding Boxes', image)
    # cv2.imwrite("boxes.jpg",image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return center_box, bottom_box

def rotate_image_based_on_boxes(image_path, center_box, bottom_box):
    image = cv2.imread(image_path)

    # rotation angle based on center box
    rect = cv2.minAreaRect(center_box)
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    edge_lengths = [np.linalg.norm(box[i] - box[(i + 1) % 4]) for i in range(4)]
    longest_edge_index = np.argmax(edge_lengths)
    longest_edge = (box[longest_edge_index], box[(longest_edge_index + 1) % 4])

    dx, dy = longest_edge[1][0] - longest_edge[0][0], longest_edge[1][1] - longest_edge[0][1]
    angle_center = np.degrees(np.arctan2(dy, dx))

    # rotation angle based on bottom box
    rect = cv2.minAreaRect(bottom_box)
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    edge_lengths = [np.linalg.norm(box[i] - box[(i + 1) % 4]) for i in range(4)]
    longest_edge_index = np.argmax(edge_lengths)
    longest_edge = (box[longest_edge_index], box[(longest_edge_index + 1) % 4])

    dx, dy = longest_edge[1][0] - longest_edge[0][0], longest_edge[1][1] - longest_edge[0][1]
    angle_bottom = np.degrees(np.arctan2(dy, dx))

    # Average of the angles from the center box and bottom box
    angle = (angle_center + angle_bottom) / 2
    print("Rotation Angle: ", angle)

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

# input_path = 'exampleScans1\Image_3.jpg'
# center_box, bottom_box = find_boxes(input_path)

# if center_box is not None and bottom_box is not None:
#     rotated_image = rotate_image_based_on_boxes(input_path, center_box, bottom_box)
#     cv2.imshow('Rotated Image', rotated_image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

#     output_path = 'rotated_image_new.jpg'
#     cv2.imwrite(output_path, rotated_image)
# else:
#     print("Could not find both center box and bottom box to base the rotation on.")



def process_folder(folder_path):

    all_files = os.listdir(folder_path)
    
    image_files = [file for file in all_files if file.lower().endswith(('.jpg','.png'))]
    
    output_folder = os.path.join(folder_path, 'rotatedImages')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        print(f'Processing {image_path}')
        
        center_box, bottom_box = find_boxes(image_path)
        
        if center_box is not None and bottom_box is not None:
            rotated_image = rotate_image_based_on_boxes(image_path, center_box, bottom_box)
            
            # Saving the rotated image
            name, ext = os.path.splitext(image_file)
            output_path = os.path.join(output_folder, f'{name}_rotated{ext}')
            cv2.imwrite(output_path, rotated_image)
            print(f'Saved rotated image to {output_path}')
        else:
            print("Could not find both center box and bottom box to base the rotation on for image:", image_path)


folder_path = 'test'
process_folder(folder_path)
