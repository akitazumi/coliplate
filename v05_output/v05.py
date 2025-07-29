import cv2
import numpy as np
import random
import pandas as pd

#test image
img = cv2.imread("image.jpg")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#greenish for cropping borders
lower_green = np.array([45, 60, 50])
upper_green = np.array([85, 255, 255])
mask = cv2.inRange(hsv, lower_green, upper_green)

#rolling from four ways, until greenish area occupies over threas
band, threshold = 5, 0.12
height, width = mask.shape
top = next(i for i in range(0, height, band) if np.count_nonzero(mask[i:i+band, :]) / (band * width) > threshold)
bottom = next(i for i in range(height, 0, -band) if np.count_nonzero(mask[i-band:i, :]) / (band * width) > threshold)
left = next(i for i in range(0, width, band) if np.count_nonzero(mask[top:bottom, i:i+band]) / (band * (bottom - top)) > threshold)
right = next(i for i in range(width, 0, -band) if np.count_nonzero(mask[top:bottom, i-band:i]) / (band * (bottom - top)) > threshold)

#crop
final_img = img[top:bottom, left:right]
ch, cw, _ = final_img.shape

#well mesh
rows, cols = 8, 12
cell_h, cell_w = ch // rows, cw // cols

#reading init
readings = []
vis_points = []

random.seed(123)

for r in range(rows):
    for c in range(cols):
        well_label = chr(65 + r) + f"{c+1:02d}"
        cx = int((c + 0.5) * cell_w)
        cy = int((r + 0.5) * cell_h)
        radius = int(min(cell_w, cell_h) * 0.35)

        count = 0
        while count < 500:
            rx = random.randint(cx - radius, cx + radius)
            ry = random.randint(cy - radius, cy + radius)
            if (rx - cx)**2 + (ry - cy)**2 <= radius**2:
                b, g, r_val = final_img[ry, rx]
                readings.append([well_label, f"point{count+1}", r_val, g, b])
                vis_points.append((rx, ry))
                count += 1

#RGB to tsv
df = pd.DataFrame(readings, columns=["Well", "Point", "R", "G", "B"])
df.to_csv("image.jpg_RGB.tsv", sep="\t", index=False)

#confirm where points are taken
for x, y in vis_points:
    cv2.circle(final_img, (x, y), 4, (255, 0, 255), -1)

#add the grid and circles, make sure magenta points are not outside
for r in range(rows):
    for c in range(cols):
        x_start = int(c * cell_w)
        y_start = int(r * cell_h)
        x_end = int((c + 1) * cell_w)
        y_end = int((r + 1) * cell_h)
        cx = int((c + 0.5) * cell_w)
        cy = int((r + 0.5) * cell_h)
        radius = int(min(cell_w, cell_h) * 0.35)

        cv2.rectangle(final_img, (x_start, y_start), (x_end, y_end), (255, 255, 0), 2)       # Yellow grid
        cv2.circle(final_img, (cx, cy), radius, (0, 255, 255), 2)                           # Cyan circle
        label = chr(65 + r) + f"{c+1:02d}"
        cv2.putText(final_img, label, (x_start + 4, y_start + 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)         # Well ID

#save it for check
cv2.imwrite("image.jpg-cropped.jpg", final_img)

