from typing import Union
from os import PathLike, getenv, remove
from random import getrandbits
from PIL import Image
import deflate

__version__ = '1.0'
__all__ = ['ZCIFile', 'DamagedEntry', 'NonValidZCI', 'IncorrectZCISize', 'bytes2zci']
__author__ = 'Discord: ZeroBossSq#5132'
FILE_START = '‰ZCI||'.encode()


class DamagedEntry(Exception):
    def __str__(self):
        return 'Unable to read ZCI entry: damaged'


class NonValidZCI(Exception):
    def __str__(self):
        return 'Not a valid ZCI image'


class IncorrectZCISize(Exception):
    def __str__(self):
        return 'Incorrect image size'


class ZCIFile:
    def __init__(self, fp: Union[str, PathLike]):
        """Makes the ZCI image object. SPECIFY SIZE PARAMETER ONLY WHEN CREATING ZCI FROM BYTES (RGBA only)"""
        image = open(fp, 'rb').read()
        first_line = image.split(b'\n')[0]
        image = b'\n'.join(image.split(b'\n')[1:])  # without file start (‰ZCI<size>)

        # checking the file entry
        if FILE_START[:6] in first_line and FILE_START[-1].to_bytes(1, 'big') in first_line:  # FILE_START[:6] = ‰ZCI ; FILE_START[-1].to_bytes(1, 'big') = 
            first_line = first_line[6:-1]  # ‰ZCI<size> -> <size> (x.y)
            self.size = (int(first_line.split(b'.')[0]), int(first_line.split(b'.')[1]))  # 'x.y' -> (x, y)
        else:
            raise NonValidZCI

        try:  # decoding by deflate and raising DamagedEntry if it fails
            image = deflate.gzip_decompress(image)
        except BaseException:
            raise DamagedEntry

        # checking image mode (RGBA/RGB)
        try:  # PIL raises ValueError if image size is larger than byte data
            try:
                self.PIL_obj: Image.Image = Image.frombytes('RGBA', self.size, image)
            except ValueError:
                self.PIL_obj: Image.Image = Image.frombytes('RGB', self.size, image)
        except ValueError:
            raise IncorrectZCISize

    def edit_pix(self, pos: Union[tuple[int, int], list[int, int]], pixel: Union[tuple[int, int, int], list[int, int, int]]):
        """Edits the pixel. pos ex: [0, 0] | pixel ex: [255, 255, 255]"""
        self.PIL_obj.putpixel(pos, pixel)

    def get_pix(self, pos: Union[tuple[int, int], list[int, int]]):
        return self.PIL_obj.getpixel(pos)

    def get_pil(self):
        """Returns PIL image obj (PIL.Image.Image)"""
        return self.PIL_obj

    def to_bytes(self):
        """Returns raw image bytes"""
        return self.PIL_obj.tobytes()

    def show(self):
        self.PIL_obj.show()

    def save(self, fp: Union[str, PathLike]):
        size = [str(i).encode() for i in self.size]  # [16, 16] to [b'16', b'16']
        file_start = FILE_START.replace(b'||', b'.'.join(size)) + b'\n'  # b'‰ZCI<x.y>\n'
        out_image = file_start + deflate.gzip_compress(self.PIL_obj.tobytes())  # add some necessary data and encode image

        out_image_obj = open(fp, 'wb')
        out_image_obj.write(out_image)
        out_image_obj.close()


def bytes2zci(bytes_obj: bytes, size: Union[tuple, list]) -> ZCIFile:
    """Makes ZCI image from bytes. If the size is incorrect, calls IncorrectZCISize"""
    size = [str(i).encode() for i in size]  # [16, 16] to [b'16', b'16']
    fp = f'{getenv("tmp")}\\%016x' % getrandbits(64)  # file path
    compressed = deflate.gzip_compress(bytes_obj)
    file_start = FILE_START.replace(b'||', b'.'.join(size)) + b'\n'  # b'‰ZCI<x.y>\n'

    open(fp, 'wb').write(file_start + compressed)
    return_img = ZCIFile(fp)

    remove(fp)  # delete tmp file
    return return_img
