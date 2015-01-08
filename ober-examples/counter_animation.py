#!/usr/bin/python
# Counter animated gif
# Inspired by http://willpython.blogspot.com/2013/03/top-in-animated-gif.html

from PIL import Image, ImageDraw, ImageFont
from images2gif import writeGif
import sys

FRAMES = 12
# FRAME_DELAY = 2  # 0.75
WIDTH, HEIGHT = 100, 100
# PIE_POS = (WIDTH - 50, 10, WIDTH - 10, 50)
FONT = ImageFont.truetype('C:/Python27/Lib/site-packages/matplotlib/mpl-data/fonts/ttf/LiberationMono-Regular.ttf', 12)
# FONT = ImageFont.load('arial.pil')

def make_frame(count, font=FONT):
    image = Image.new('RGBA', (WIDTH, HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    # fontsize = font.getsize('')[1]
    draw.text((0, 0), str(count), (0, 0, 0), font=font)
    return image

'''Main program'''
if __name__ == '__main__':
    frames = []
    max_count = int(sys.argv[1])
    frame_delay = float(sys.argv[2])
    for count in xrange(max_count + 1):
        frames.append(make_frame(count))
    writeGif('topmovie-%d.gif' % (max_count), frames, duration=frame_delay)
