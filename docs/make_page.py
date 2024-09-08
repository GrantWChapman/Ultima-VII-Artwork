from pathlib import Path

html_header_and_style = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Gallery</title>
    <link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>

<h1>Ultima-VII-Artwork</h1>

<div id="table-of-contents">
  <h2>Table of Contents</h2>
  <ul id="toc-list">
    <li><a href="#paperdolls"><em>Paperdolls</em></a></li>
    <li><a href="#paperdolls_shields">Ultima Shields</a></li>
    <li><a href="#paperdolls_armor">Ultima Armor</a></li>
    <li><a href="#paperdolls_clothes">Ultima Clothes</a></li>
    <li><a href="#paperdolls_accessories">Ultima Accessories</a></li>
    <li><a href="#paperdolls_ammo">Ammo</a></li>
    <li><a href="#paperdolls_arrows">Arrows</a></li>
    <li><a href="#paperdolls_axes">Axes</a></li>
    <li><a href="#paperdolls_blowguns">Blowguns</a></li>
    <li><a href="#paperdolls_bolts">Bolts</a></li>
    <li><a href="#paperdolls_bows">Bows</a></li>
    <li><a href="#paperdolls_crossbows">Crossbows</a></li>
    <li><a href="#paperdolls_daggers">Daggers</a></li>
    <li><a href="#paperdolls_firearms">Firearms</a></li>
    <li><a href="#paperdolls_flails">Flails</a></li>
    <li><a href="#paperdolls_maces">Maces</a></li>
    <li><a href="#paperdolls_polearms">Polearms</a></li>
    <li><a href="#paperdolls_slings">Slings</a></li>
    <li><a href="#paperdolls_swords">Swords</a></li>
    <li><a href="#paperdolls_thrown">Thrown</a></li>
    <li><a href="#paperdolls_wands">Wands</a></li>
    <li><a href="#shapes"><em>Shapes</em></a></li>
    <li><a href="#shapes_shields">Ultima Shields</a></li>
    <li><a href="#shapes_armor">Ultima Armor</a></li>
    <li><a href="#shapes_clothes">Ultima Clothes</a></li>
    <li><a href="#shapes_accessories">Ultima Accessories</a></li>
    <li><a href="#shapes_ammo">Ammo</a></li>
    <li><a href="#shapes_arrows">Arrows</a></li>
    <li><a href="#shapes_axes">Axes</a></li>
    <li><a href="#shapes_blowguns">Blowguns</a></li>
    <li><a href="#shapes_bolts">Bolts</a></li>
    <li><a href="#shapes_bows">Bows</a></li>
    <li><a href="#shapes_crossbows">Crossbows</a></li>
    <li><a href="#shapes_daggers">Daggers</a></li>
    <li><a href="#shapes_firearms">Firearms</a></li>
    <li><a href="#shapes_flails">Flails</a></li>
    <li><a href="#shapes_maces">Maces</a></li>
    <li><a href="#shapes_polearms">Polearms</a></li>
    <li><a href="#shapes_slings">Slings</a></li>
    <li><a href="#shapes_swords">Swords</a></li>
    <li><a href="#shapes_thrown">Thrown</a></li>
    <li><a href="#shapes_wands">Wands</a></li></ul>
</div>

"""

# This is a generic TOC for the script below
# <div id="table-of-contents">
#   <h1>Table of Contents</h1>
#   <ul id="toc-list"></ul>
# </div>


html_footer = r"""

</body>
</html>
"""
# This script is supposed to generate the HTML TOC I hardcoded above.
# <script>
#   // Get all h1 and h2 elements on the page
#   const headings = document.querySelectorAll('h2, h3');

#   // Create a table of contents list
#   const tocList = document.getElementById('toc-list');

#   // Loop through each heading and add a link to the table of contents
#   headings.forEach((heading) => {
#     const link = document.createElement('a');
#     link.textContent = heading.textContent;
#     link.href = `#${heading.id}`;

#     // If the heading is an h1, add a class to indicate it's a top-level heading
#     if (heading.tagName === 'h2') {
#       link.classList.add('top-level');
#     }

#     const listItem = document.createElement('li');
#     listItem.appendChild(link);
#     tocList.appendChild(listItem);
#   });

# </script>

def create_image_box(path: Path):
    template = """<div class="image-box"> <img src="{path}" alt="Image 1"> <a href="{path}" target="_blank">{filename}</a></div>"""
    return template.format(path='../' + str(path).replace('\\', '/'), filename=path.stem)

def add_gallery_container(title: str, images: list[str], id_: str):
    template = """\n<h3 id={id_}>{title}</h3>\n<div class="gallery-container">{images}\n</div>"""
    return template.format(images="\n\t".join(images), title=title, id_=id_)

folders_paperdolls = [
    Path('Ultima Shields/Art/Paperdolls'),
    Path('Ultima Armor/Art/Paperdolls'),
    Path('Ultima Clothes/Art/Paperdolls'),
    Path('Ultima Accessories/Art/Paperdoll'),
]


folders_shapes = [
    Path('Ultima Shields/Art/Shapes'),
    Path('Ultima Armor/Art/Shapes'),
    Path('Ultima Clothes/Art/Shapes'),
    Path('Ultima Accessories/Art/Shapes'),
]

assert all([i.exists() for i in folders_paperdolls])
assert all([i.exists() for i in folders_shapes])

html = html_header_and_style

html += '\n<h2 id="paperdolls">Paperdolls</h2>\n'
for folder in folders_paperdolls:
    html += add_gallery_container(folder.parents[1].stem, [create_image_box(path) for path in folder.glob('*.png')], 'paperdolls_' + folder.parents[1].stem.split(' ')[1].lower())
for folder in Path('Ultima Weapons/Art/Paperdolls').glob('*'):
    html += add_gallery_container(folder.stem, [create_image_box(path) for path in folder.glob('*.png')], 'paperdolls_' + folder.stem.lower())

html += '\n<h2 id="shapes">Shapes</h2>\n'
for folder in folders_shapes:
    html += add_gallery_container(folder.parents[1].stem, [create_image_box(path) for path in folder.glob('*.png')], 'shapes_' + folder.parents[1].stem.split(' ')[1].lower())
for folder in Path('Ultima Weapons/Art/Sprites').glob('*'):
    html += add_gallery_container(folder.stem, [create_image_box(path) for path in folder.glob('*.png')], 'shapes_' + folder.stem.lower())
html += html_footer

with open('docs/index.html', 'w') as f:
    f.write(html)