import math
from typing import List
from PIL import Image


class ImgToAscii:
    def downscale_image(self, old_image: Image.Image, new_width: int) -> Image.Image:
        old_width, old_height = old_image.size
        aspect_ratio = old_height / old_width

        new_height = int(aspect_ratio * new_width)
        new_width = int(new_width * 2)

        return old_image.resize((new_width, new_height))

    def get_ascii_from_pixel_intensity(
        self, pixel_intensity: int, ramp_choice: str
    ) -> str:
        RAMPS = {
            "block": "░▒▓█",
            "detailed": "`.',-~:;-=+*#%@MW",
            "smooth": "▁▂▃▄▅▆▇█",
            "basic": ".°:oO8@",
            "geometric": "○◌─│┌┐└┘├┤┬┴┼▁▂▃▄▅▆▇▀█",
        }

        selected_ramp = RAMPS[ramp_choice]

        map_length = len(selected_ramp)

        # map_index = math.ceil(((map_length - 1) * pixel_intensity) / 255)
        map_index = min(map_length - 1, math.floor((map_length * pixel_intensity) / 256))

        return selected_ramp[map_index]

    def ascii_html_string(self, buffer: List[List[dict]]) -> str:
        rows = []
        for row in buffer:
            row_chars = "".join(
                f"<span style='color: {pixel['color']};'>{pixel['char']}</span>"
                for pixel in row
            )
            rows.append(row_chars)
        return "<br>".join(rows)

    def ascii_raw_string(self, buffer: List[List[int]]) -> str:
        return "\n".join(["".join(row) for row in buffer])

    def generate_ascii(
        self,
        source_image: Image.Image,
        ramp_choice: str,
        colored: bool,
        image_width: int,
    ) -> List[List[dict]]:
        if source_image.width > image_width:
            source_image = self.downscale_image(source_image, image_width)

        grayscale_image = source_image.convert("L")

        width, height = grayscale_image.size

        # 2D buffer
        result_buffer = []

        for y in range(height):
            row = []
            for x in range(width):
                pixel_coordinate = (x, y)
                pixel_intensity = grayscale_image.getpixel(pixel_coordinate)
                ascii_char = self.get_ascii_from_pixel_intensity(
                    pixel_intensity, ramp_choice
                )

                if colored:
                    red, green, blue = source_image.convert("RGB").getpixel(
                        pixel_coordinate
                    )
                    pixel_hex = "#{:02x}{:02x}{:02x}".format(red, green, blue)
                    pixel_data = {"char": ascii_char, "color": pixel_hex}
                else:
                    pixel_data = ascii_char

                row.append(pixel_data)
            result_buffer.append(row)

        if colored:
            return self.ascii_html_string(result_buffer)
        else:
            return self.ascii_raw_string(result_buffer)

img_to_ascii = ImgToAscii()
