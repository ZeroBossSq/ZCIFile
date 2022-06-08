from random import choice
from os import listdir
from os.path import basename

from py7zr import SevenZipFile
from PIL import Image


def hex_to_rgb(value):
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


# get only .zeai (maybe "ZeroBossSq Experimental Archive Image") files from "view" dir
imgs = [f'view/{file}' for file in listdir('view') if file.endswith(".zeai")]

# if imgs list is empty - close the program
if not imgs:
    exit(0)

# get the basic info from file
img = choice(imgs)
img_name = basename(img)
clear_img_name = '.'.join(img_name.split('.')[:-1])

# open and read all files from archive (selected .zeai)
img_archive = SevenZipFile(img, password='Quick2ZeraBossSq')
img_archive_files = img_archive.read()

img_archive.close()

# get a content from .zi (ZeroBossSq Image) from .zeai file (ex. stick.zeai -> stick.zi)
gotten_img_bytes = img_archive_files[f'{clear_img_name}.zi'].read()
gotten_img_str = gotten_img_bytes.decode('utf8')

# remove the unnecessary '\r' that was left behind during decoding
gotten_img_str = gotten_img_str.replace('\r', '')

# remove the empty lines (add line, if it's don't contain '' (nothing) in it) and set this data to "image lines" var
image_lines = [line for line in gotten_img_str.split('\n') if line != '']

# checking image
image_colour_vars = {}
lines_only_with_colours = []
image_scale = None  # line №52
image_size = None  # would be 1:1 : 16x16, 32x32, 9x9...

for line in image_lines:
    # line = "scale 16"
    if image_lines.index(line) == 0 and line.startswith('scale'):
        """ Determines the magnification of a pixel by a factor of N times. For example: "scale 16" means that 1 pixel will be magnified 16 times """
        image_scale = int(line.split(' ')[1])  # "scale 16" -> "16" -> 16
        
        # protection against heavy loads due to the sheer scale
        if image_scale > 32:
            image_scale = 32
    
    # line = "def black = #000000"
    elif line.startswith('def'):
        clear_colour_line = line.replace('def ', '')  # "black = #000000"
        colour_dict = clear_colour_line.split(' = ')  # ["black", "#000000"]
        colour_dict = {colour_dict[0]: colour_dict[1]}
        
        image_colour_vars |= colour_dict  # {'black': '#000000'} + {'green': '#01a205'} = {'black': '#000000', 'green': '#01a205'}
    
    else:
        lines_only_with_colours.append(line)

# calculate x and y of image
image_x_size = len(lines_only_with_colours[0].split(' '))  # count of colours (pixels) in first line
image_y_size = len(lines_only_with_colours)

# create img var
output_image = Image.new('RGB', (image_x_size, image_y_size), '#000000')

y = -1
for line in lines_only_with_colours:
    # move by y cord
    x = -1
    y += 1
    
    # Move by x cord (split line to pixels)
    for colour in line.split(' '):
        x += 1
        
        # retrieve a colour from the colour dict, or leave the current colour
        fill_colour = image_colour_vars[colour] if colour in image_colour_vars.keys() else colour
        
        # set pixel/colour/block to the his place (x, y)
        output_image.putpixel((x, y), hex_to_rgb(fill_colour))

image_out = output_image.resize((image_x_size * image_scale, image_y_size * image_scale), Image.NEAREST)

image_out.show()
