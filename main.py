import argparse

import PIL.Image as Image


class ImageProcessing:
    def __init__(self, path):
        self.path = str(path)
        self._image_byte_array = None
        self._image = Image.open(path)

    def get_pixel(self, i, j):

        width, height = self._image.size
        if i > width or j > height:
            return None
        pixel = self._image.getpixel((int(i), int(j)))
        return pixel

    @staticmethod
    def create_image(i, j):
        image = Image.new("RGB", (i, j), "white")
        return image

    @staticmethod
    def open_image(path):
        new_image = Image.open(path)
        return new_image

    @staticmethod
    def save_image(image, path):
        image.save(f'{path}.jpg')

    def convert_grayscale(self):
        width, height = self._image.size

        new = self.create_image(width, height)
        pixels = new.load()

        for i in range(width):
            for y in range(height):
                pixel = self.get_pixel(i, y)

                red = pixel[0]
                green = pixel[1]
                blue = pixel[2]

                gray = (red * .299) + (green + .587) + (blue * .114)
                pixels[i, y] = (int(gray), int(gray), int(gray))
        self.save_image(new, f'{self.path.split(".")[0]}_gray')

    def invert(self):
        width, height = self._image.size

        new = self.create_image(width, height)
        pixels = new.load()

        for i in range(width):
            for y in range(height):
                pixel = self.get_pixel(i, y)

                red = 255 - pixel[0]
                green = 255 - pixel[1]
                blue = 255 - pixel[2]

                pixels[i, y] = (int(red), int(green), int(blue))

        self.save_image(new, f'{self.path.split(".")[0]}_invert')

    def set_brightness(self, brightness: int = 50):
        width, height = self._image.size

        new = self.create_image(width, height)
        pixels = new.load()

        for i in range(width):
            for y in range(height):
                pixel = self.get_pixel(i, y)

                red = pixel[0]
                green = pixel[1]
                blue = pixel[2]

                cr = red + brightness
                cg = green + brightness
                cb = blue + brightness

                if cr < 0:
                    cr = 1
                if cr > 255:
                    cr = 255

                if cg < 0:
                    cg = 1
                if cg > 255:
                    cg = 255

                if cb < 0:
                    cb = 1
                if cb > 255:
                    cb = 255

                pixels[i, y] = (int(cr), int(cg), int(cb))
        self.save_image(new, f'{self.path.split(".")[0]}_brightness_{brightness}')

    def color_filter(self, color: str):
        width, height = self._image.size

        new = self.create_image(width, height)
        pixels = new.load()

        for i in range(width):
            for y in range(height):
                pixel = self.get_pixel(i, y)

                red = pixel[0]
                green = pixel[1]
                blue = pixel[2]

                cr = 0
                cg = 0
                cb = 0

                if color.lower() == 'red':
                    cr = red
                    cg = green - 255
                    cb = blue - 255
                elif color.lower() == 'green':
                    cr = red - 255
                    cg = green
                    cb = blue - 255
                elif color.lower() == 'blue':
                    cr = red - 255
                    cg = green - 255
                    cb = blue
                pixels[i, y] = (int(cr), int(cg), int(cb))

        self.save_image(new, f'{self.path.split(".")[0]}_color_filter_{color.upper()}')

    def set_contrast(self, contrast) -> None:
        """

        :param contrast:
            0 to 4 in decimal numbers
        :alter the image contrast

        """
        contrast = float(contrast)
        width, height = self._image.size

        new = self.create_image(width, height)
        pixels = new.load()

        for i in range(width):
            for y in range(height):
                pixel = self.get_pixel(i, y)

                red = pixel[0]
                green = pixel[1]
                blue = pixel[2]

                cr = red / 255.0
                cr -= .5
                cr *= contrast
                cr += .5
                cr *= 255
                if cr < 0:
                    cr = 0
                if cr > 255:
                    cr = 255

                cg = green / 255.0
                cg -= .5
                cg *= contrast
                cg += .5
                cg *= 255
                if cg < 0:
                    cg = 0
                if cg > 255:
                    cg = 255

                cb = blue / 255.0
                cb -= .5
                cb *= contrast
                cb += .5
                cb *= 255
                if cb < 0:
                    cb = 0
                if cb > 255:
                    cb = 255

                pixels[i, y] = (int(cr), int(cg), int(cb))

        self.save_image(new, f'{self.path.split(".")[0]}_contrast_{contrast}')


if __name__ == '__main__':
    ip = None
    parser = argparse.ArgumentParser(prog='PROG', usage='%(prog)s [options]')
    sub_parser = parser.add_subparsers(dest='command', metavar='command')
    sub_parser.required = True

    sub_parser = sub_parser.add_parser('start', help='start work with image path')
    sub_parser.add_argument('path', nargs='+', metavar='path', help='Image path')
    sub_parser.add_argument('opt', nargs='+', metavar='opt',
                            help='Chose operation: 0 -> contrast, 1 -> Brightness, 2 -> Color Filter, ' +
                                 '3 -> Invert image, 4 -> Change image to gray scale')
    sub_parser.add_argument('-int', nargs='?', metavar='--int',
                            help='chose some intensity to contrast(0 to 4) or brightness(-255 to +255)' +
                                 ' or color filter(red, green and blue)')

    args = parser.parse_args()
    if args.command == 'start':
        print('Loading ...')
        ip = ImageProcessing(args.path[0])
        if args.opt[0] == '0':
            if args.int[0] is None:
                print('Please info intensity')
            else:
                ip.set_contrast(args.int[0])
        elif args.opt[0] == '1':
            if args.int[0] is None:
                print('Please info intensity')
            else:
                ip.set_brightness(args.int[0])
        elif args.opt[0] == '2':
            if args.int[0] is None:
                print('Please info intensity')
            else:
                ip.set_brightness(args.int[0])
        elif args.opt[0] == '3':
            ip.invert()
        elif args.opt[0] == '4':
            ip.convert_grayscale()

        print('Finished image processing!')
