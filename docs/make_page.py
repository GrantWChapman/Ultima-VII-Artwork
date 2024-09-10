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
    <div class="toc-columns">
       <div class="toc-column">
           <h3><a href="#paperdolls">Paperdolls</a></h3>
           <a class="toc-link" href="#paperdolls_accessories">Accessories</a>
           <a class="toc-link" href="#paperdolls_ammo">Ammo</a>
           <a class="toc-link" href="#paperdolls_armor">Armor</a>
           <a class="toc-link" href="#paperdolls_arrows">Arrows</a>
           <a class="toc-link" href="#paperdolls_axes">Axes</a>
           <a class="toc-link" href="#paperdolls_blowguns">Blowguns</a>
           <a class="toc-link" href="#paperdolls_bolts">Bolts</a>
           <a class="toc-link" href="#paperdolls_bows">Bows</a>
           <a class="toc-link" href="#paperdolls_clothes">Clothes</a>
           <a class="toc-link" href="#paperdolls_crossbows">Crossbows</a>
           <a class="toc-link" href="#paperdolls_daggers">Daggers</a>
           <a class="toc-link" href="#paperdolls_firearms">Firearms</a>
           <a class="toc-link" href="#paperdolls_flails">Flails</a>
           <a class="toc-link" href="#paperdolls_maces">Maces</a>
           <a class="toc-link" href="#paperdolls_polearms">Polearms</a>
           <a class="toc-link" href="#paperdolls_shields">Shields</a>
           <a class="toc-link" href="#paperdolls_slings">Slings</a>
           <a class="toc-link" href="#paperdolls_swords">Swords</a>
           <a class="toc-link" href="#paperdolls_thrown">Thrown</a>
           <a class="toc-link" href="#paperdolls_wands">Wands</a>
       </div>
        <div class="toc-column">
            <h3><a href="#shapes">Shapes and sprites</a></h3>
            <a class="toc-link" href="#shapes_accessories">Accessories</a>
            <a class="toc-link" href="#shapes_armor">Armor</a>
            <a class="toc-link" href="#shapes_clothes">Clothes</a>
            <a class="toc-link" href="#shapes_shields">Shields</a>
            <a class="toc-link" href="#shapes_ammo">Ammo</a>
            <a class="toc-link" href="#shapes_arrows">Arrows</a>
            <a class="toc-link" href="#shapes_axes">Axes</a>
            <a class="toc-link" href="#shapes_blowguns">Blowguns</a>
            <a class="toc-link" href="#shapes_bolts">Bolts</a>
            <a class="toc-link" href="#shapes_bows">Bows</a>
            <a class="toc-link" href="#shapes_crossbows">Crossbows</a>
            <a class="toc-link" href="#shapes_daggers">Daggers</a>
            <a class="toc-link" href="#shapes_firearms">Firearms</a>
            <a class="toc-link" href="#shapes_flails">Flails</a>
            <a class="toc-link" href="#shapes_maces">Maces</a>
            <a class="toc-link" href="#shapes_polearms">Polearms</a>
            <a class="toc-link" href="#shapes_slings">Slings</a>
            <a class="toc-link" href="#shapes_swords">Swords</a>
            <a class="toc-link" href="#shapes_thrown">Thrown</a>
            <a class="toc-link" href="#shapes_wands">Wands</a>
        </div>
    </div>
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

# To auto-generate a toc in case I change stuff
# <script>
# // Get all h1 and h2 elements on the page
# const headings = document.querySelectorAll('h2, h3');
#
# // Create a table of contents list
# const tocList = document.getElementById('toc-list');
#
# // Loop through each heading and add a link to the table of contents
# headings.forEach((heading) => {
#     const link = document.createElement('a');
# link.textContent = heading.textContent;
# link.href = `#${heading.id}`;
#
#             // If the heading is an h1, add a class to indicate it's a top-level heading
# if (heading.tagName === 'h2') {
# link.classList.add('top-level');
# }
#
# const listItem = document.createElement('li');
# listItem.appendChild(link);
# tocList.appendChild(listItem);
# });
#
# </script>


def create_image_box(path: Path):
    template = """<div class="image-box"> <img src="{path}" alt="{filename}"> <a href="{path}" target="_blank"></a></div>"""
    return template.format(path=str(path), filename=path.stem)


def add_gallery_container(title: str, images: list[str], html_id: str):
    template = """\n<h3 id={id_}>{title}</h3>\n<div class="gallery-container">{images}\n</div>"""
    return template.format(images="\n\t".join(images), title=title, id_=html_id)


images_paperdolls = list(Path(".").glob("paperdolls*png"))
images_shapes_sprites = list(Path(".").glob("shapes*png")) + list(Path(".").glob("sprites*png"))

assert all([i.exists() for i in images_paperdolls])
assert all([i.exists() for i in images_shapes_sprites])

html = html_header_and_style


def get_name(path: Path):
    t1 = str(path)
    second_half = t1.split("_")[1]
    name_itself = second_half.split(".")[0]
    return name_itself


html += '\n<h2 id="paperdolls">Paperdolls</h2>\n'
for image in images_paperdolls:
    html += add_gallery_container(
        get_name(image),
        [create_image_box(image)],
        "paperdolls_" + get_name(image).lower(),
    )

html += '\n<h2 id="shapes">Shapes and sprites</h2>\n'
for image in images_shapes_sprites:
    html += add_gallery_container(
        get_name(image), [create_image_box(image)], "shapes_" + get_name(image).lower()
    )
html += html_footer

with open("index.html", "w") as f:
    f.write(html)
