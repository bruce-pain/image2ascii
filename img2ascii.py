import math
from typing import List
from PIL import Image


class ImgToAscii:
    MAX_WIDTH = 150

    def downscale_image(self, old_image: Image.Image, new_width: int) -> Image.Image:
        old_width, old_height = old_image.size
        aspect_ratio = old_height / old_width

        new_height = int(aspect_ratio * new_width)
        new_width = int(new_width * 2)

        return old_image.resize((new_width, new_height))

    def get_ascii_from_pixel_intensity(self, pixel_intensity: int) -> str:
        # ASCII_RAMP = r".-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"
        ASCII_RAMP = " ░▒▓█"
        map_length = len(ASCII_RAMP)

        map_index = math.ceil(((map_length - 1) * pixel_intensity) / 255)

        return ASCII_RAMP[map_index]

    def ascii_string(self, buffer: List[List[int]]) -> str:
        return "\n".join(["".join(row) for row in buffer])

    def generate_ascii(self, grayscale_image: Image.Image) -> str:
        if grayscale_image.width > self.MAX_WIDTH:
            grayscale_image = self.downscale_image(grayscale_image, self.MAX_WIDTH)
        grayscale_image = grayscale_image.convert("L")

        width, height = grayscale_image.size

        # 2D buffer
        result_buffer = []

        for y in range(height):
            row = []
            for x in range(width):
                pixel_coordinate = (x, y)
                pixel_intensity = grayscale_image.getpixel(pixel_coordinate)

                ascii_char = self.get_ascii_from_pixel_intensity(pixel_intensity)
                row.append(ascii_char)
            result_buffer.append(row)

        return self.ascii_string(result_buffer)


img_to_ascii = ImgToAscii()
