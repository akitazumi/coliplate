import cv2
import numpy as np
import random
import argparse
import os
import statistics

#seed
random.seed(123)

#message
print(f"im v3! fixed the RGB reverse order, output format is tab delim for RGB and takes in number of points to pick and filename from users\nrun me like $python v02.py pic1.jpg -points 500")
print('for the test, i run it $for i in {1..6}; do python v03.py -points 500 pic${i}.jpg ;done')
#flags
parser = argparse.ArgumentParser(description="this will crop from clean picture, divide into 98 wells and extract colors")
parser.add_argument('image_path', type=str, help='path to your image')
parser.add_argument('-points', type=int, default=100, help='number of picks from each wells, specify if not 100')
args = parser.parse_args()

#import image, hopefully same size (cropped at the edge of plate)
image_path = args.image_path
image = cv2.imread(image_path)
base_name = os.path.splitext(os.path.basename(image_path))[0]

#get dimensions
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

#pull out the clean one and two output
image = cv2.imread('pic1_cropped.jpg')

image_grid = image.copy()
image_picked = image.copy()

#dimensions
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

#RGB to HTML
def rgb_to_html_color(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

#BGR to RGB
def bgr_to_rgb(bgr): return (bgr[2], bgr[1], bgr[0])

#average of 100
def average_color(pixels):
    return tuple(np.mean(pixels, axis=0).astype(int))

#user-specified
num_points = args.points

#for all wells
center_colors = []

#v03: for all wells, average and SD
all_reds = []
all_greens = []
all_blues = []

#v03: for left and right wells, average and SD
left_reds, right_reds = [], []
left_greens, right_greens = [], []
left_blues, right_blues = [], []

for i in range(grid_rows):
    current_x = 0
    for j in range(grid_cols):
        #size per well
        cell_width = well_width + (1 if j < remaining_width else 0)
        cell_height = well_height + (1 if i < remaining_height else 0)
        
        #coords per well
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
        
        #random pick while avoiding margins
        selected_points = [
            (random.randint(inner_x1, inner_x2 - 1), random.randint(inner_y1, inner_y2 - 1))
            for _ in range(num_points)
        ]
        
        #v03 color per pick and store per layout
        try:
            adjacent_colors = [bgr_to_rgb(well[pt[1], pt[0]]) for pt in selected_points]
            for r, g, b in adjacent_colors:
                all_reds.append(r)
                all_greens.append(g)
                all_blues.append(b)
                if j < 4:  # Left wells
                    left_reds.append(r)
                    left_greens.append(g)
                    left_blues.append(b)
                elif j >= 8:  # Right wells
                    right_reds.append(r)
                    right_greens.append(g)
                    right_blues.append(b)
        except IndexError:
            print(f"Skipping well at ({i}, {j}) due to indexing error.")
            continue
        
        #average of 100 picks or user-specified number
        average_center_color = average_color(adjacent_colors)
        
        #RGB to html per well
        html_color = rgb_to_html_color(average_center_color)
        
        #save wells and colors
        well_label = f'{chr(65 + i)}{j + 1}'
        center_colors.append((image_path, well_label, average_center_color[0], average_center_color[1], average_center_color[2], html_color))
        
        #draw boundary for check
        cv2.rectangle(image_grid, (x1, y1), (x2, y2), (0, 0, 255), 2)
        
        #draw the picks to make sure it didn't pick from edge or red centers
        for pt in selected_points:
            cv2.circle(image_picked, (x1 + pt[0], y1 + pt[1]), 1, (0, 0, 0), -1)
        
        #next column
        current_x = x2

    #next row
    current_y += cell_height

#calculate stats for all, left, and right
def calculate_stats(reds, greens, blues):
    avg_red = statistics.mean(reds)
    avg_green = statistics.mean(greens)
    avg_blue = statistics.mean(blues)
    avg_rgb = (int(avg_red), int(avg_green), int(avg_blue))
    avg_html_color = rgb_to_html_color(avg_rgb)
    
    reds = list(map(int, reds))
    greens = list(map(int, greens))
    blues = list(map(int, blues))
    
    std_red = statistics.stdev(reds)
    std_green = statistics.stdev(greens)
    std_blue = statistics.stdev(blues)
    
    avg_red_minus_2sd = avg_red - 2 * std_red
    avg_red_plus_2sd = avg_red + 2 * std_red
    avg_green_minus_2sd = avg_green - 2 * std_green
    avg_green_plus_2sd = avg_green + 2 * std_green
    avg_blue_minus_2sd = avg_blue - 2 * std_blue
    avg_blue_plus_2sd = avg_blue + 2 * std_blue
    
    low_rgb = (int(avg_red_minus_2sd), int(avg_green_minus_2sd), int(avg_blue_minus_2sd))
    high_rgb = (int(avg_red_plus_2sd), int(avg_green_plus_2sd), int(avg_blue_plus_2sd))
    low_html_color = rgb_to_html_color(low_rgb)
    high_html_color = rgb_to_html_color(high_rgb)
    
    return (avg_red, avg_green, avg_blue, avg_html_color,
            avg_red_minus_2sd, avg_red_plus_2sd,
            avg_green_minus_2sd, avg_green_plus_2sd,
            avg_blue_minus_2sd, avg_blue_plus_2sd,
            low_html_color, high_html_color)

#all
all_stats = calculate_stats(all_reds, all_greens, all_blues)
#left
left_stats = calculate_stats(left_reds, left_greens, left_blues)
#right
right_stats = calculate_stats(right_reds, right_greens, right_blues)

#get two img outputs
cv2.imwrite(f'{base_name}_wells.jpg', image_grid)
cv2.imwrite(f'{base_name}_points.jpg', image_picked)

#stdout
print(f"################")
for item in center_colors:
    print(f'{item[0]}\tpoints={num_points}\t{item[1]}\t{item[2]}\t{item[3]}\t{item[4]}\t"{item[5]}"')

#stdout, stat, all
print(f'{base_name}.jpg\tAverage.RGB\tall\t{all_stats[0]:.0f}\t{all_stats[1]:.0f}\t{all_stats[2]:.0f}\t"{all_stats[3]}"')
print(f'{base_name}.jpg\tStdev, -2SD\tall\t{all_stats[4]:.0f}\t{all_stats[6]:.0f}\t{all_stats[8]:.0f}\t"{all_stats[10]}"')
print(f'{base_name}.jpg\tStdev, +2SD\tall\t{all_stats[5]:.0f}\t{all_stats[7]:.0f}\t{all_stats[9]:.0f}\t"{all_stats[11]}"')

#left
print(f'{base_name}.jpg\tAverage.RGB\tleft\t{left_stats[0]:.0f}\t{left_stats[1]:.0f}\t{left_stats[2]:.0f}\t"{left_stats[3]}"')
print(f'{base_name}.jpg\tStdev, -2SD\tleft\t{left_stats[4]:.0f}\t{left_stats[6]:.0f}\t{left_stats[8]:.0f}\t"{left_stats[10]}"')
print(f'{base_name}.jpg\tStdev, +2SD\tleft\t{left_stats[5]:.0f}\t{left_stats[7]:.0f}\t{left_stats[9]:.0f}\t"{left_stats[11]}"')

#right
print(f'{base_name}.jpg\tAverage.RGB\tright\t{right_stats[0]:.0f}\t{right_stats[1]:.0f}\t{right_stats[2]:.0f}\t"{right_stats[3]}"')
print(f'{base_name}.jpg\tStdev, -2SD\tright\t{right_stats[4]:.0f}\t{right_stats[6]:.0f}\t{right_stats[8]:.0f}\t"{right_stats[10]}"')
print(f'{base_name}.jpg\tStdev, +2SD\tright\t{right_stats[5]:.0f}\t{right_stats[7]:.0f}\t{right_stats[9]:.0f}\t"{right_stats[11]}"')


#per well
with open(f'{base_name}_cols.txt', 'w') as f:
    for item in center_colors:
        f.write(f'{item[0]}\tpoints={num_points}\t{item[1]}\t{item[2]}\t{item[3]}\t{item[4]}\t"{item[5]}"\n')

#just stats
with open(f'{base_name}_stats.txt', 'w') as f:
    #ave, -2SD, 2SD
    def write_stats(stat_type, stats):
        f.write(f'{base_name}.jpg\tAverage.RGB\t{stat_type}\t{stats[0]:.0f}\t{stats[1]:.0f}\t{stats[2]:.0f}\t"{stats[3]}"\n')
        f.write(f'{base_name}.jpg\tStdev, -2SD\t{stat_type}\t{stats[4]:.0f}\t{stats[6]:.0f}\t{stats[8]:.0f}\t"{stats[10]}"\n')
        f.write(f'{base_name}.jpg\tStdev, +2SD\t{stat_type}\t{stats[5]:.0f}\t{stats[7]:.0f}\t{stats[9]:.0f}\t"{stats[11]}"\n')

    #all
    write_stats('all', all_stats)
    #left
    write_stats('left', left_stats)
    #right
    write_stats('right', right_stats)

print(f"################\ndone with {image_path} saved as '{base_name}_wells.jpg' and '{base_name}_points.jpg',\nplease check well borders and picked positions are not too off.\nNumber of points picked: {num_points}")
