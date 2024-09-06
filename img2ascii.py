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
        ASCII_RAMP = "▒▓█"
        # ASCII_RAMP = r".-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"
        map_length = len(ASCII_RAMP)

        map_index = math.ceil(((map_length - 1) * pixel_intensity) / 255)

        return ASCII_RAMP[map_index]

    def ascii_html_string(self, buffer: List[List[dict]]) -> str:
        output = []
        for row in buffer:
            for pixel in row:
                output.append(f"<span style='color: {pixel['color']};'>{pixel['char']}</span>")
            output.append("<br>")

        return ''.join(output)


    def generate_ascii(self, source_image: Image.Image) -> List[List[dict]]:
        if source_image.width > self.MAX_WIDTH:
            source_image = self.downscale_image(source_image, self.MAX_WIDTH)

        grayscale_image = source_image.convert("L")

        width, height = grayscale_image.size

        # 2D buffer
        result_buffer = []

        for y in range(height):
            row = []
            for x in range(width):
                pixel_coordinate = (x, y)
                pixel_intensity = grayscale_image.getpixel(pixel_coordinate)
                red, green, blue = source_image.convert("RGB").getpixel(pixel_coordinate)

                pixel_hex = '#{:02x}{:02x}{:02x}'.format(red, green, blue)
                ascii_char = self.get_ascii_from_pixel_intensity(pixel_intensity)

                pixel_data = {"char": ascii_char, "color": pixel_hex}
                row.append(pixel_data)
            result_buffer.append(row)

        return self.ascii_html_string(result_buffer)


img_to_ascii = ImgToAscii()
