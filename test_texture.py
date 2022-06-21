import random

import cv2
import numpy as np

field_height = 6
field_width = 9
goal_depth = 0.6
goal_width = 2.6
goal_height = 1.2
goal_area_length = 1
goal_area_width = 3
penalty_mark_distance = 1.5
centre_circle_diameter = 1.5
minimum_border_strip_width = 1
maximum_border_strip_width = 2
penalty_area_length = 2
penalty_area_width = 5

line_width_range = [0.04, 0.06]

resolution_scale = 100

savepath = "/home/fiborobotlab/15-06-2022FootballF/imageFBF/"
savegreenpath = "/home/fiborobotlab/15-06-2022FootballF/greenFBF/"

base_lines = [[(0, 0), (field_width, 0)],
               [(0, 0), (0, field_height)],
               [(0, field_height), (field_width, field_height)],
               [(field_width, 0), (field_width, field_height)],
               [(-goal_depth, (field_height-goal_width)/2), (-goal_depth, (field_height+goal_width)/2)],
               [(-goal_depth, (field_height-goal_width)/2), (0, (field_height-goal_width)/2)],
               [(-goal_depth, (field_height+goal_width)/2), (0, (field_height+goal_width)/2)],
               [(field_width+goal_depth, (field_height-goal_width)/2), (field_width+goal_depth, (field_height+goal_width)/2)],
               [(field_width, (field_height-goal_width)/2), (field_width+goal_depth, (field_height-goal_width)/2)],
               [(field_width, (field_height+goal_width)/2), (field_width+goal_depth, (field_height+goal_width)/2)],
               [(goal_area_length, (field_height-goal_area_width)/2), (goal_area_length, (field_height+goal_area_width)/2)],
               [(0, (field_height-goal_area_width)/2), (goal_area_length, (field_height-goal_area_width)/2)],
               [(0, (field_height+goal_area_width)/2), (goal_area_length, (field_height+goal_area_width)/2)],
               [(field_width-goal_area_length, (field_height-goal_area_width)/2), (field_width-goal_area_length, (field_height+goal_area_width)/2)],
               [(field_width, (field_height-goal_area_width)/2), (field_width-goal_area_length, (field_height-goal_area_width)/2)],
               [(field_width, (field_height+goal_area_width)/2), (field_width-goal_area_length, (field_height+goal_area_width)/2)],
               [(field_width/2, 0), (field_width/2, field_height)]
               ]

def gen_texture(color, offset_height, offset_width):
    base_texture = np.zeros((int(resolution_scale*(field_height+offset_height*2)), int(resolution_scale*(field_width+offset_width*2)), 4))
    for line in base_lines:
        start = (int((line[0][0]+offset_width)*resolution_scale), int((line[0][1]+offset_height)*resolution_scale))
        stop = (int((line[1][0]+offset_width)*resolution_scale), int((line[1][1]+offset_height)*resolution_scale))
        line_width = line_width_range[0] + random.random() * (line_width_range[1] - line_width_range[0])
        cv2.line(base_texture, start, stop, color=color, thickness=int(line_width*resolution_scale))
    line_width = line_width_range[0] + random.random() * (line_width_range[1] - line_width_range[0])
    cv2.circle(base_texture,
               (int(resolution_scale*(field_width/2+offset_width)), int(resolution_scale*(field_height/2+offset_height))),
               radius=int(resolution_scale*(centre_circle_diameter/2)),
               color=color,
               thickness=int(line_width*resolution_scale))
    return base_texture

def hsv_to_rgb(h, s, v):
    """Converts HSV value to RGB values
    Hue is in range 0-359 (degrees), value/saturation are in range 0-1 (float)

    Direct implementation of:
    http://en.wikipedia.org/wiki/HSL_and_HSV#Conversion_from_HSV_to_RGB
    """
    h, s, v = [float(x) for x in (h, s, v)]
    hi = (h / 60) % 6
    hi = int(round(hi))

    f = (h / 60) - (h / 60)
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)

    if hi == 0:
        return v, t, p
    elif hi == 1:
        return q, v, p
    elif hi == 2:
        return p, v, t
    elif hi == 3:
        return p, q, v
    elif hi == 4:
        return t, p, v
    elif hi == 5:
        return v, p, q

def greenTexture(num, offset_height, offset_width):
    """Generate 50 random RGB colours, and create some simple coloured HTML
    span tags to verify them.
    """
    # test() # Run simple test suite
    img = np.ones((offset_height ,offset_width,3),np.uint8)
    im_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    for i in range(len(im_rgb)):
        for j in range(len(im_rgb[0])):
            h = random.randint(80, 150) # Select random green'ish hue from hue wheel
            s = random.uniform(0.2, 1)
            v = random.uniform(0.3, 1)

            r, g, b = hsv_to_rgb(h, s, v)
            r, g, b = [x*255 for x in (r, g, b)]

            im_rgb[i][j][0] = r
            im_rgb[i][j][1] = g
            im_rgb[i][j][2] = b
    return im_rgb
    # print("randomGreenS_%i.png"%num)


#while True:
for a in range(1000):
    border_strip_width = minimum_border_strip_width + random.random()*(maximum_border_strip_width-minimum_border_strip_width)
    border_strip_height = minimum_border_strip_width + random.random()*(maximum_border_strip_width-minimum_border_strip_width)

    rand_intensity = random.randint(200, 255)
    rand_color = (rand_intensity, rand_intensity, rand_intensity, 0)
    line_texture = gen_texture(offset_height=border_strip_height,
                               offset_width=border_strip_width,
                               color=rand_color)

    imgShape = line_texture.shape
    im_rgb = greenTexture(num=a, offset_height=imgShape[0], offset_width=imgShape[1])
    print(imgShape)
    for i in range(len(line_texture)):
        for j in range(len(line_texture[0])):
            # for k in range(len(line_texture[[0][0]])):
            if line_texture[i][j][0] > 200:
                line_texture[i][j][-1] = random.randint(50,200)
                # if line_texture[i][j][k]
    print("================ footballF_"+str(a)+".png ==================")
    cv2.imwrite(savepath+"footballF_%i.png" % a,line_texture)
    cv2.imwrite(savegreenpath+"randomGreenS_%i.png" % a, im_rgb)
    print("================ footballF_"+str(a)+".png ==================")


