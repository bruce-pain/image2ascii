import math
from typing import List
from PIL import Image

class ImgToAscii:
    MAX_WIDTH = 75
    def downscale_image(self, old_image: Image.Image, new_width: int) -> Image.Image:
        old_width, old_height = old_image.size
        aspect_ratio = old_height / old_width

        new_height = int(aspect_ratio * new_width)
        new_width = int(new_width * 2.5)

        return old_image.resize((new_width, new_height))

    def get_ascii_from_pixel_intensity(self, pixel_intensity: int) -> str:
        ASCII_MAP = (
            r"$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
        )
        map_length = len(ASCII_MAP)

        map_index = math.ceil(((map_length - 1) * pixel_intensity) / 255)

        return ASCII_MAP[map_index]

    def ascii_string(self, buffer: List[List[int]]) -> str:
        return "\n".join(["".join(row) for row in buffer])

    def generate_ascii(self, source_image: Image.Image) -> str:
        source_image = source_image.convert("L")
        if source_image.width > self.MAX_WIDTH:
            source_image = self.downscale_image(source_image, self.MAX_WIDTH)

        width, height = source_image.size

        # 2D buffer
        result_buffer = []

        for y in range(height):
            row = []
            for x in range(width):
                pixel_coordinate = (x, y)
                pixel_intensity = source_image.getpixel(pixel_coordinate)

                ascii_char = self.get_ascii_from_pixel_intensity(pixel_intensity)
                row.append(ascii_char)
            result_buffer.append(row)

        return self.ascii_string(result_buffer)

img_to_ascii = ImgToAscii()
