import cv2
import numpy as np
import random


#import image, hopefully same size (cropped at the edge of plate)

############
import io
import numpy as np
import cv2
import PIL.Image
import PIL.ImageCms

img = PIL.Image.open('pic1.jpg')
img_profile = PIL.ImageCms.ImageCmsProfile(io.BytesIO(img.info.get('icc_profile')))
rgb_profile = PIL.ImageCms.createProfile('sRGB')
trans = PIL.ImageCms.buildTransform(img_profile, rgb_profile, 'RGB', 'RGB')
image = PIL.ImageCms.applyTransform(img, trans)

cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

#############
image_path = 'pic1'
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

#yohaku
remaining_width = width % grid_cols
remaining_height = height % grid_rows

#init
current_x, current_y = 0, 0

#rgb2html
def rgb_to_html_color(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

#ave of 100
def average_color(pixels):
    return tuple(np.mean(pixels, axis=0).astype(int))

#for all wells
center_colors = {}

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
        
        #100 random pick avoid mergins
        selected_points = [
            (random.randint(inner_x1, inner_x2 - 1), random.randint(inner_y1, inner_y2 - 1))
            for _ in range(100)
        ]
        
        #color per pick
        try:
            adjacent_colors = [well[pt[1], pt[0]] for pt in selected_points]
        except IndexError:
            print(f"Skipping well at ({i}, {j}) due to indexing error.")
            continue
        
        #average of 100 picks as defined
        average_center_color = average_color(adjacent_colors)
        
        #rgb2html as defined
        html_color = rgb_to_html_color(average_center_color)
        
        #save wells and colors
        well_label = f'{chr(65 + i)}{j + 1}'
        center_colors[well_label] = (tuple(average_center_color), html_color)
        
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
cv2.imwrite('pic1_wells.jpg', image_grid)
cv2.imwrite('pic1_picked.jpg', image_picked)

#stdout
for well, (color, html_color) in center_colors.items():
    print(f'Well {well}: Center RGB color {color}, HTML color "{html_color}"')

#tab ver for excel import
with open('pic1_cols.txt', 'w') as f:
    for well, (color, html_color) in center_colors.items():
        f.write(f'{image_path}\t{well}\t{color}\t"{html_color}"\n')

print("done with pic1.jpg! please check well borders and picked positions are not too off")
