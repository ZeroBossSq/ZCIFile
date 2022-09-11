# ZCIFile

A small library that can open and save ZCI images.
The library works by compressing the raw image data using the deflate algorithm.

## Setup and Dependencies
* Clone the repository:
```
git clone https://github.com/ZeroBossSq/ZCIFile
```

* Install the dependencies:
```
pip install -r requirements.txt
```

## Usage
### Opening
You can open the existing ZCI:
```python
from zcifile import *

my_image = ZCIFile('my image.zci')  # Open "my image.zci"

print(my_image.size)  # Shows the image size
```
Or make new from bytes (PIL example):
```python
from PIL import Image
from zcifile import *

pil_img = Image.open('my_image.png')
zci_img = bytes2zci(pil_img.tobytes(), pil_img.size)  # First arg = image bytes data, second = image size

zci_img.show()  # Open the image in external viewer
```

### Saving
The ZCI can be exported as a file:
```python
from zcifile import *

zci_img = ZCIFile('my_zci.zci')  # Open existing ZCI
zci_img.save('new_zci.zci')  # Saving into "new_zci.zci"
```
Or receive as bytes:
```python
from zcifile import *

zci_img = ZCIFile('my_zci.zci')  # Open existing ZCI
zci_bytes = zci_img.to_bytes()
```
## Modifying and retrieving information
You can change any pixel in the image as follows:
```python
from zcifile import *

zci_img = ZCIFile('my_zci.zci')  # Open existing ZCI
zci_img.edit_pixel(pos=(0, 0), pixel=(255, 255, 255))
```
###### Options
`pos` is a required parameter, is a list of two int's indicating the x and y of the pixel

`pixel` is a required parameter, is a list of 3 int's indicating the rgb colour of the pixel (rrr, ggg, bbb)

You can also recognise any pixel in the image:
```python
from zcifile import *

zci_img = ZCIFile('my_zci.zci')  # Open existing ZCI
zci_img.get_pixel(pos=(0, 0))  # Returns the rgb array of 3 ints (rrr, ggg, bbb)
```
## License

This project is under the [MIT license](./LICENSE).
