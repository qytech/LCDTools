import argparse
import os
import sys
from textwrap import wrap

import langid
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from bmp2hex import bmp2hex

mode_to_bpp = {'1': 1, 'L': 8, 'P': 8, 'RGB': 24,
               'RGBA': 32, 'CMYK': 32, 'YCbCr': 24, 'I': 32, 'F': 32}


class ImageGenerate():
    def __init__(self):
        self.width = 32
        self.height = 48
        self.chart_limit = 4
        self.real_path = getattr(
            sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

    def get_y_and_heights(self, text_wrapped, dimensions, margin, font):
        """Get the first vertical coordinate at which to draw text and the height of each line of text"""
        # https://stackoverflow.com/a/46220683/9263761
        ascent, descent = font.getmetrics()

        # Calculate the height needed to draw each line of text (including its bottom margin)
        line_heights = [
            font.getmask(text_line).getbbox()[3] + descent + margin
            for text_line in text_wrapped
        ]
        # The last line doesn't have a bottom margin
        line_heights[-1] -= margin

        # Total height needed
        height_text = sum(line_heights)

        # Calculate the Y coordinate at which to draw the first line of text
        y = (dimensions[1] - height_text) // 2

        # Return the first Y coordinate and a list with the height of each line
        return (y, line_heights)

    def get_font_family(self, lang):
        return {
            'zh': 'msyh.ttc',
            'ko': 'gulim.ttf',
            'ja': 'msmincho.TTF'
        }.get(lang, 'HackRegularNerdFontComplete.ttf')

    def get_font_size(self, lang, text):
        length = len(text)
        default = {1: 22, 2: 20, 3: 18, 4: 16}
        big = {1: 22, 2: 20, 3: 15, 4: 11}
        big_font = ['ja', 'zh', 'ko']
        if lang in big_font:
            return big.get(length, 16)
        else:
            return default.get(length, 16)

    def generate(self, text, font_family=None, font_size=None):
        if not font_family or not font_size:
            lang = langid.classify(text)[0]
        if not font_family:
            font_family = f'{self.real_path}/fontFamily/{self.get_font_family(lang)}'
        if not font_size:
            font_size = self.get_font_size(lang, text)

        print(f'{len(text)}  {font_family} {font_size}')

        font = ImageFont.truetype(font_family, font_size)
        image_name = f'res/image_{text}.bmp'
        image = Image.new('1', (self.width, self.height), (255))
        draw = ImageDraw.Draw(image)
        # draw.text((0, 8), text, font=font, fill=(0))
        w =0
        h = 0 
        x  = 0
        for index,item in enumerate(text):
            if index ==0:
                w,h= font.getsize(item)
                x = (self.width - w)/2
            draw.text((x, h*index), item, font=font, fill=(0))
        # Wrap the `text` string into a list of `CHAR_LIMIT`-character strings
        # text_lines = wrap(text, self.chart_limit)
        # print(text_lines)
        # # Get the first vertical coordinate at which to draw text and the height of each line of text
        # y, line_heights = self.get_y_and_heights(
        #     text_lines, (self.width, self.height), 0, font
        # )

        # # Draw each line of text
        # for i, line in enumerate(text_lines):
        #     # Calculate the horizontally-centered position at which to draw this line
        #     line_width = font.getmask(line).getbbox()[2]
        #     x = ((self.width - line_width) // 2)

        #     # Draw this line
        #     draw.text((x, y), line, font=font, fill=(0))

        #     # Move on to the height at which the next line should be drawn at
        #     y += line_heights[i]

        image.save(image_name, 'bmp')
        return image_name


def main():
    parser = argparse.ArgumentParser(description='text to image')
    parser.add_argument('text', metavar='N', type=str,
                        nargs='+', help='please input text  convert to array')

    args = parser.parse_args()
    gen = ImageGenerate()
    for text in args.text:

        gen.generate(text)

        bmp2hex.bmp2hex(f'res/image_{text}.bmp', 16, 0,
                        False, False, False, False, False)


# if __name__ == '__main__':
#     main()
