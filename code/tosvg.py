#!/usr/bin/env python3
# $URL: http://amberfrog.googlecode.com/svn/trunk/mapsvg/code/tosvg.py $
# $Rev: 164 $
# Convert Shapefile to SVG
# David Jones, Climate Code Foundation, 2011-08-13

"""tosvg shapefile

Convert the shapefile to SVG.
"""

import sys

# http://geospatialpython.com/2010/11/introducing-python-shapefile-library.html
import shapefile

def equir2(ps):
    """Transform list of (x,y) pairs, by scaling by 2."""

    for x,y in ps:
        x += 180
        y += 90
        x *= 2.0
        y *= 2.0
        yield x,y

def tosvg(fname, out=sys.stdout, transform=equir2):
    
    out.write("""<svg
      xmlns="http://www.w3.org/2000/svg"
      xmlns:xlink="http://www.w3.org/1999/xlink"
      version="1.1">
""")
    out.write("""<defs>
  <style type="text/css">
    g.land { stroke: none; stroke-width: 0.7; stroke-linecap: round;
      fill: olive }
    text { fill: black; font-family: Verdana }
  </style></defs>
""")
    out.write("""<g class='land' transform='translate(0,360) scale(1,-1)'>
  <!-- Within this group longitude goes from 0 (at 180 West) to 720 (at 180
  East); latitude goes from 0 (at 90 South) to 360 (at 90 North).
  -->
""")
    shapr = shapefile.Reader(fname)
    for shape in shapr.shapes():
        points = transform(shape.points)
        startpoint = next(points)
        out.write("<path d='M %.2f %.2f L" % tuple(startpoint))
        for point in points:
            out.write(" %.2f %.2f" % tuple(point))
        out.write("' />\n")
    out.write("</g>\n")
    out.write("</svg>\n")

def main(argv=None):
    import sys
    if argv is None:
        argv = sys.argv

    return tosvg(argv[1])

if __name__ == '__main__':
    main()
