import cv2
import numpy as np
import random
import argparse
import os

#seed
random.seed(123)


#message
print(f"im v2! fixed the RGB reverse order, output format is tab delim for RGB and takes in number of points to pick and filename from users\nrun me like $python v02.py pic1.jpg -points 500")

#flags 
parser = argparse.ArgumentParser(description="this will crop from clean picture, divide into 98 wells and extract colors") 
parser.add_argument('image_path', type=str, help='path to your image') 
parser.add_argument('-points', type=int, default=100, help='number of picks from each wells, specify if not 100') 
args = parser.parse_args()


#import image, hopefully same size (cropped at the edge of plate)
image_path = args.image_path
image = cv2.imread(image_path)
base_name = os.path.splitext(os.path.basename(image_path))[0]

#get dim
height, width = image.shape[:2]

#removing the space between edge and wells
top_crop = int(height * 0.05)
bottom_crop = int(height * 0.05)
left_crop = int(width * 0.06)
right_crop = int(width * 0.06)

#clean
cropped_image = image[top_crop:height - bottom_crop, left_crop:width - right_crop]

#save it for check
cv2.imwrite('pic1_cropped.jpg', cropped_image)

print("cropped as 'pic1_cropped.jpg'. please check.")

###################



#pull out the clean one and two output
image = cv2.imread('pic1_cropped.jpg')

image_grid = image.copy()
image_picked = image.copy()

#dim
height, width = image.shape[:2]

#96 wells
grid_rows = 8
grid_cols = 12

#size per well
well_height = height // grid_rows
well_width = width // grid_cols

#mergin2
remaining_width = width % grid_cols
remaining_height = height % grid_rows

#init
current_x, current_y = 0, 0

#rgb2html
def rgb_to_html_color(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

#BGR to RGB!!
def bgr_to_rgb(bgr): return (bgr[2], bgr[1], bgr[0])

#ave of 100
def average_color(pixels):
    return tuple(np.mean(pixels, axis=0).astype(int))

#user-specified
num_points = args.points

#for all wells
center_colors = []

for i in range(grid_rows):
    current_x = 0
    for j in range(grid_cols):
        #size per well
        cell_width = well_width + (1 if j < remaining_width else 0)
        cell_height = well_height + (1 if i < remaining_height else 0)
        
        #coord per well
        x1 = current_x
        y1 = current_y
        x2 = x1 + cell_width
        y2 = y1 + cell_height
        
        #well extract
        well = image[y1:y2, x1:x2]
        
        #avoid the edge
        margin = int(min(cell_width, cell_height) * 0.25)  # 25% margin, adjust if needed
        inner_x1 = margin
        inner_y1 = margin
        inner_x2 = cell_width - margin
        inner_y2 = cell_height - margin
        
        #100 or specified random pick to avoid mergins
        selected_points = [
            (random.randint(inner_x1, inner_x2 - 1), random.randint(inner_y1, inner_y2 - 1))
            for _ in range(num_points)
        ]
        
        #color per pick
        try:
            adjacent_colors = [bgr_to_rgb(well[pt[1], pt[0]]) for pt in selected_points]
        except IndexError:
            print(f"Skipping well at ({i}, {j}) due to indexing error.")
            continue
        
        #average of 100 picks as defined
        average_center_color = average_color(adjacent_colors)
        
        #rgb2html as defined
        html_color = rgb_to_html_color(average_center_color)
        
        #save wells and colors
        well_label = f'{chr(65 + i)}{j + 1}'
        #center_colors[well_label] = (tuple(average_center_color), html_color)
        #center_colors.append((image_path, well_label, *average_center_color, html_color))
        center_colors.append((image_path, well_label, average_center_color[0], average_center_color[1],average_center_color[2], html_color))
        #draw the boundary for check
        cv2.rectangle(image_grid, (x1, y1), (x2, y2), (0, 0, 255), 2)
        
        #draw the picks to make sure it didn't pick from edge or red centers
        for pt in selected_points:
            cv2.circle(image_picked, (x1 + pt[0], y1 + pt[1]), 1, (0, 0, 0), -1)
        
        #next col
        current_x = x2

    #next row
    current_y += cell_height

#get two outputs
cv2.imwrite(f'{base_name}_wells.jpg', image_grid)
cv2.imwrite(f'{base_name}_points.jpg', image_picked)

#stdout
for item in center_colors:
    print(f'{item[0]}\tpoints={num_points}\t{item[1]}\t{item[2]}\t{item[3]}\t{item[4]}\t"{item[5]}"')

#tab ver for excel import
with open(f'{base_name}_cols.txt', 'w') as f:
    for item in center_colors:
        f.write(f'{item[0]}\tpoints={num_points}\t{item[1]}\t{item[2]}\t{item[3]}\t{item[4]}\t"{item[5]}"\n')



print(f"done with {image_path} saved as '{base_name}_wells.jpg' and '{base_name}_points.jpg', please check well borders and picked positions are not too off. Number of points picked: {num_points}")
