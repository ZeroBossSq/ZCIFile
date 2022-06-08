from os.path import exists

from PIL import Image
from py7zr import SevenZipFile

NAME = input("Enter the art name\n>>> ")


def rgb2hex(r, g, b):
    return '#%02x%02x%02x' % (r, g, b)


IMAGE = Image.open("png2zeai.png")
IMAGE_SIZE = IMAGE.size
IMAGE_SCALE = 16
output_num = 1
variables = {}

# If the image exists, put the version that does not exist in brackets (e.g. "mario (2)") otherwise just the file name
if exists(f'view/{NAME}.zeai'):
    while exists(f'view/{NAME} ({str(output_num)}).zeai'):
        output_num += 1
    output_image_name = f'{NAME} ({str(output_num)})'
else:
    output_image_name = f'{NAME}'

# create the quick image sketch (without variables)
colours_lines = ''
for y in range(IMAGE_SIZE[1]):
    # Create an empty line, where the colours will then be written and merged into a solid line using .join
    line = []

    for x in range(IMAGE_SIZE[0]):
        colours = IMAGE.getpixel((x, y))
        colour = rgb2hex(colours[0], colours[1], colours[2])

        line.append(colour)

    line = ' '.join(line)
    colours_lines += f'{line}\n'

# resize
resized_lines = colours_lines

for colour in resized_lines.split(' '):
    # if the current colour occurs more than 3 times - replaced by a variable
    if resized_lines.count(colour) >= 3:
        # Take the number of variables in the list + 1 to create a new one (so if there are 3 variables in the list, 4 will be created, or if there are already 291, 292 will be created)
        variables[str(len(variables.keys()) + 1)] = colour

        resized_lines = resized_lines.replace(colour, str(len(variables.keys())))

# preparing to ending
connected_variables = '\n'.join([f'def {key} = {value}' for key, value in variables.items()])

connected_lines = f'scale {IMAGE_SCALE}\n' \
                  f'{connected_variables}\n' \
                  f'{resized_lines}'

output = SevenZipFile(f'view/{output_image_name}.zeai', mode='w', password='Quick2ZeraBossSq')
output.writestr(connected_lines, f'{NAME}.zi')  # create file "{NAME}.zi" in the archive with the content ({connected_lines})
output.close()
