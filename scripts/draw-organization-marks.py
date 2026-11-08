#!/usr/bin/env python3
"""Build transparent monochrome SVG marks from the site's existing logo assets.

Pillow reads the original pixels for silhouette tracing; originals are never changed.
Greyparrot's symbol retains the paths from its official SVG.
"""
from collections import defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'images' / 'organizations'
INK = '#655f55'


def area(points):
    return abs(sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(points, points[1:] + points[:1]))) / 2


def simplify(points, tolerance):
    if len(points) <= 2:
        return points
    a, b = points[0], points[-1]
    dx, dy = b[0] - a[0], b[1] - a[1]
    denom = dx * dx + dy * dy
    furthest, distance = 0, 0
    for i, p in enumerate(points[1:-1], 1):
        t = max(0, min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / denom)) if denom else 0
        d = (p[0] - a[0] - t * dx) ** 2 + (p[1] - a[1] - t * dy) ** 2
        if d > distance:
            furthest, distance = i, d
    if distance <= tolerance * tolerance:
        return [a, b]
    return simplify(points[:furthest + 1], tolerance)[:-1] + simplify(points[furthest:], tolerance)


def contours(mask, width, height):
    edges = defaultdict(list)
    for y in range(height):
        for x in range(width):
            if not mask[y * width + x]:
                continue
            if y == 0 or not mask[(y - 1) * width + x]:
                edges[x, y].append((x + 1, y))
            if x == width - 1 or not mask[y * width + x + 1]:
                edges[x + 1, y].append((x + 1, y + 1))
            if y == height - 1 or not mask[(y + 1) * width + x]:
                edges[x + 1, y + 1].append((x, y + 1))
            if x == 0 or not mask[y * width + x - 1]:
                edges[x, y + 1].append((x, y))
    result = []
    while edges:
        start = next(iter(edges))
        point, polygon = start, [start]
        while True:
            following = edges[point].pop()
            if not edges[point]:
                del edges[point]
            point = following
            if point == start:
                break
            polygon.append(point)
        if len(polygon) > 8 and area(polygon) > 12:
            # Split the closed contour into two open curves before simplifying.
            far = max(range(len(polygon)), key=lambda i: (polygon[i][0] - start[0]) ** 2 + (polygon[i][1] - start[1]) ** 2)
            simplified = simplify(polygon[:far + 1], .85)[:-1] + simplify(polygon[far:] + [start], .85)[:-1]
            if len(simplified) > 2:
                result.append(simplified)
    return result


def write(name, title, body):
    (DEST / (name + '.svg')).write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="96" height="96" viewBox="0 0 96 96" role="img" aria-labelledby="title">\n'
        f'<title id="title">{title}</title>\n'
        f'<g fill="{INK}" fill-rule="evenodd">{body}</g>\n</svg>\n'
    )


def trace(name, title, source, predicate, crop=None):
    im = Image.open(ROOT / 'images' / source).convert('RGBA')
    if crop:
        im = im.crop(crop)
    mask = [bool(predicate(*pixel)) for pixel in im.getdata()]
    width, height = im.size
    polygons = contours(mask, width, height)
    if not polygons:
        raise ValueError('No mark silhouette found: ' + source)
    xmin = min(x for p in polygons for x, _ in p)
    xmax = max(x for p in polygons for x, _ in p)
    ymin = min(y for p in polygons for _, y in p)
    ymax = max(y for p in polygons for _, y in p)
    scale = min(78 / (xmax - xmin), 78 / (ymax - ymin))
    offset_x = (96 - (xmax - xmin) * scale) / 2 - xmin * scale
    offset_y = (96 - (ymax - ymin) * scale) / 2 - ymin * scale
    paths = []
    for polygon in polygons:
        points = [(x * scale + offset_x, y * scale + offset_y) for x, y in polygon]
        paths.append('M' + ' L'.join(f'{x:.2f} {y:.2f}' for x, y in points) + ' Z')
    write(name, title, '<path d="' + ' '.join(paths) + '"/>')


def main():
    DEST.mkdir(exist_ok=True, parents=True)
    trace('agendia', 'Agendia fingerprint mark', 'Agendia.png',
          lambda r, g, b, a: a > 128 and max(r, g, b) - min(r, g, b) > 50)
    trace('tu-eindhoven', 'Eindhoven University of Technology mark', 'TUE.png',
          lambda r, g, b, a: a > 128)
    trace('quva', 'QUvA laboratory emblem', 'QUVA.png',
          lambda r, g, b, a: max(r, g, b) < 128, crop=(114, 36, 416, 338))
    trace('huawei', 'Huawei flower mark', 'Huawei.jpg',
          lambda r, g, b, a: r > g + 45 and r > b + 45)
    official = ET.parse(DEST / 'source' / 'greyparrot.svg').getroot()
    ns = {'s': 'http://www.w3.org/2000/svg'}
    paths = official.find('s:g', ns).findall('s:path', ns)
    if len(paths) != 4:
        raise ValueError('The official Greyparrot SVG changed; inspect its paths before rebuilding.')
    # First path is the wordmark; the other three are the parrot symbol.
    body = ''.join('<path d="' + p.attrib['d'] + '"/>' for p in paths[1:])
    write('greyparrot', 'Greyparrot parrot mark',
          '<g transform="translate(22 12) scale(1.5) translate(-166 0)">' + body + '</g>')
    print('Wrote five transparent monochrome organization marks to ' + str(DEST))


if __name__ == '__main__':
    main()
