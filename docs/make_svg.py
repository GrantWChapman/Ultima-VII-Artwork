import subprocess
import drawsvg as dw
from PIL import Image
from pathlib import Path
import math

N_COLS = 10 # Default number of columns in the merged images
N_COLS_GUMPS = 3 # Number of columns for the Gumps, which are wider than the other images
INKSCAPE_PATH = r"C:\Program Files\Inkscape\bin\inkscape.exe"

FOLDERS_PAPERDOLLS = [
    Path("../Ultima Accessories/Art/Paperdoll"),
    Path("../Ultima Armor/Art/Paperdolls"),
    Path("../Ultima Clothes/Art/Paperdolls"),
    Path("../Ultima Shields/Art/Paperdolls"),
]


FOLDERS_SHAPES = [
    Path("../Ultima Accessories/Art/Shapes"),
    Path("../Ultima Armor/Art/Shapes"),
    Path("../Ultima Clothes/Art/Shapes"),
    Path("../Ultima Shields/Art/Shapes"),
]

FOLDERS_WEAPON_PAPERDOLLS = list(Path("../Ultima Weapons/Art/Paperdolls").glob("*"))
FOLDERS_WEAPON_SPRITES = list(Path("../Ultima Weapons/Art/Sprites").glob("*"))

FOLDER_GUMPS = Path('../Ultima Gumps/Art')

FOLDER_BODIES = Path('../Ultima Bodies - Combined/Art/Paperdoll')


def create_drawing(images_paths: list[Path], n_cols=N_COLS):
    widths = []
    heights = []
    for image in images_paths:
        i = Image.open(image)
        width, height = i.size
        widths.append(width)
        heights.append(height)
        i.close()

    max_width = max(widths)
    max_height = max(heights)

    page_width = max_width * n_cols
    page_height = max_height * math.ceil(len(images_paths) / n_cols)

    drawing = dw.Drawing(page_width, page_height, origin=(0, 0))
    rolling_xpos = 0
    rolling_ypos = 0

    for image, w, h in zip(images_paths, widths, heights):
        drawing.append(
            dw.Image(
                rolling_xpos,
                rolling_ypos,
                w,
                h,
                image,
                embed=False,
                preserveAspectRatio=False,
            )
        )
        rolling_xpos += max_width
        if rolling_xpos >= page_width:
            rolling_xpos = 0
            rolling_ypos += max_height

    return drawing


def try_to_save(output_image_path: Path, drawing: dw.Drawing):
    try:
        drawing.save_png(output_image_path.with_suffix(".png"))  # Requires Cairo. 
    except Exception as e:  # Assuming the only error thrown is Cairo not being found
        print(
            "Problem when saving png, probably related to Cairo not being found. "
            "Switching to inkscape and saving SVGs for later conversion"
        )
        svg_path = output_image_path.with_suffix(".svg")
        drawing.save_svg(svg_path)
        if not Path(INKSCAPE_PATH).exists():
            print("Inkscape not found. Only saving the svgs")
            return
        a = subprocess.run([INKSCAPE_PATH, "--export-type=png", str(svg_path)], capture_output=True)
        if a.stderr:
            print("Inkscape error: ", a.stderr)


def process_folder(folder: Path, output_path: Path, n_cols=N_COLS, clean_svg: bool = False):
    images = sorted(list(folder.glob("*.png")))
    drawing = create_drawing(images, n_cols)
    try_to_save(output_path, drawing)
    if clean_svg:
        output_path.with_suffix(".svg").unlink(missing_ok=True)


def main():
    for folder in FOLDERS_PAPERDOLLS:
        process_folder(
            folder,
            Path("paperdolls_" + folder.parents[1].stem.split(" ")[1] + ".png"),
            clean_svg=True,
        )
    for folder in FOLDERS_SHAPES:
        process_folder(
            folder,
            Path("shapes_" + folder.parents[1].stem.split(" ")[1] + ".png"),
            clean_svg=True,
        )
    for folder in FOLDERS_WEAPON_PAPERDOLLS:
        process_folder(folder, Path("paperdolls_" + folder.stem + ".png"), clean_svg=True)
    for folder in FOLDERS_WEAPON_SPRITES:
        process_folder(folder, Path("sprites_" + folder.stem + ".png"), clean_svg=True)

    process_folder(FOLDER_GUMPS, Path("gumps.png"), clean_svg=True, n_cols=N_COLS_GUMPS)
    process_folder(FOLDER_BODIES, Path("bodies.png"), clean_svg=True)
    


if __name__ == "__main__":
    main()
