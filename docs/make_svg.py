import subprocess

import drawsvg as dw
from PIL import Image
from pathlib import Path
import math
import os

COLS = 10
INKSCAPE_PATH = r"C:\Program Files\Inkscape\bin\inkscape.exe"

FOLDERS_PAPERDOLLS = [
    Path('../Ultima Shields/Art/Paperdolls'),
    Path('../Ultima Armor/Art/Paperdolls'),
    Path('../Ultima Clothes/Art/Paperdolls'),
    Path('../Ultima Accessories/Art/Paperdoll'),
]


FOLDERS_SHAPES = [
    Path('../Ultima Shields/Art/Shapes'),
    Path('../Ultima Armor/Art/Shapes'),
    Path('../Ultima Clothes/Art/Shapes'),
    Path('../Ultima Accessories/Art/Shapes'),
]

svgs = []

for folder in FOLDERS_PAPERDOLLS:
    images = sorted(list(folder.glob('*.png')))
    widths = []
    heights = []
    for image in images:
        i = Image.open(image)
        width, height = i.size
        widths.append(width)
        heights.append(height)
        i.close()

    max_width = max(widths)
    max_height = max(heights)

    num_cols = 10
    page_width = max_width * num_cols
    page_height = max_height * math.ceil(len(images) / num_cols)

    drawing = dw.Drawing(page_width, page_height, origin=(0, 0), id_prefix="shields")
    rolling_xpos = 0
    rolling_ypos = 0

    for image, w, h in zip(images, widths, heights):
        drawing.append(
            dw.Image(rolling_xpos, rolling_ypos, w, h, image, embed=False, preserveAspectRatio=False)
        )
        rolling_xpos += max_width
        if rolling_xpos >= page_width:
            rolling_xpos = 0
            rolling_ypos += max_height

    png_path = Path('paperdolls_' + folder.parents[1].stem.split(' ')[1] + ".png")
    try:
        drawing.save_png(png_path) # Requires Cairo. If it fails
    except Exception as e: # Assuming 
        print(e)
        svg_path = png_path.with_suffix('.svg')
        drawing.save_svg(svg_path)
        a = subprocess.run([r"C:\Program Files\Inkscape\bin\inkscape.exe", "--export-type=png",  str(svg_path)], capture_output=True)
        if a.stderr:
            print(a.stderr)
            

for folder in FOLDERS_SHAPES:
    images = sorted(list(folder.glob('*.png')))
    widths = []
    heights = []
    for image in images:
        i = Image.open(image)
        width, height = i.size
        widths.append(width)
        heights.append(height)
        i.close()

    max_width = max(widths)
    max_height = max(heights)

    num_cols = 10
    page_width = max_width * num_cols
    page_height = max_height * math.ceil(len(images) / num_cols)

    drawing = dw.Drawing(page_width, page_height, origin=(0, 0), id_prefix="shields")
    rolling_xpos = 0
    rolling_ypos = 0

    for image, w, h in zip(images, widths, heights):
        drawing.append(
            dw.Image(rolling_xpos, rolling_ypos, w, h, image, embed=False, preserveAspectRatio=False)
        )
        rolling_xpos += max_width
        if rolling_xpos >= page_width:
            rolling_xpos = 0
            rolling_ypos += max_height

    png_path = Path('shapes_' + folder.parents[1].stem.split(' ')[1] + ".png")
    try:
        drawing.save_png(png_path) # Requires Cairo. If it fails
    except Exception as e: # Assuming 
        print(e)
        svg_path = png_path.with_suffix('.svg')
        drawing.save_svg(svg_path)
        a = subprocess.run([r"C:\Program Files\Inkscape\bin\inkscape.exe", "--export-type=png",  str(svg_path)], capture_output=True)
        if a.stderr:
            print(a.stderr)