#!/usr/bin/env python
# $URL$
# $Rev$
# reproject.py
# David Jones, Climate Code Foundation, 2011-08-22

import math

import tosvg

def dline(ps):
    """Transform list of points by reprojecting."""

    # Great half-circle starting at (+40-050) and going SE through
    # Q (-40+000), terminating at (-40+130).  R is the point that is
    # halfway along the arc.

    # An alternate.
    up = (45,-45)
    up = cart(*up)
    ux,uy,uz = up

    Q = (-45,15)
    Q = cart(*Q)
    Qx,Qy,Qz = Q

    R = resolve_perp(up, Q)

    # T is the unit vector perpendicular to *up* and *Q* (such that
    # *up*, *Q*, *T* form a right-hand system).
    T = crossVV(up, Q)

    if 0:
        print(up)
        # print Q
        print(R)
        print(T)
        print([math.sqrt(dotVV(V,V)) for V in [up, R, T]])
        print([dotVV(up, R), dotVV(R, T), dotVV(T, up)])
        return

    for lon,lat in ps:
        p = cart(lat, lon)

        Z = dotVV(up, p)
        X = dotVV(R, p)
        Y = dotVV(T, p)

        tlat = math.degrees(math.asin(Z)) + 90
        tlon = math.degrees(math.atan2(Y, X)) % 360

        assert 0 <= tlat <= 180
        assert 0 <= tlon <= 360

        tlat *= 2
        tlon *= 2

        yield tlon,tlat

def resolve_perp(u, v):
    """Component of *v* that is perpendicular to *u* (and in the plane
    formed by *u* and *v*).  Assumes *u* and *v* are unit length.
    """

    p = dotVV(u, v)
    para = [p*t for t in u]
    perp = [x-y for x,y in zip(v,para)]
    l = math.sqrt(dotVV(perp, perp))
    perp = [t/l for t in perp]
    return perp


def cart(lat, lon):
    """Convert to cartesian coordinates.  *lat*, *lon* in degrees.

    X,Y,Z cartesian coordinates (right-hand).  Z-axis is +ve at North
    Pole; X-axis is +ve at (+00+000); Y-axis is +ve at (+00+090).
    """

    lon,lat = [math.radians(t) for t in (lon,lat)]
    z = math.sin(lat)
    x = math.cos(lon)
    y = math.sin(lon)
    x,y = [math.cos(lat)*t for t in (x,y)]
    return x,y,z

        
def dotVV(a, b):
    """Dot product."""

    return sum(x*y for x,y in zip(a,b))

def crossVV(a, b):
    """Cross product."""
    
    return [ a[1]*b[2] - a[2]*b[1],
             a[2]*b[0] - a[0]*b[2],
             a[0]*b[1] - a[1]*b[0],
           ]



def reproject(fname):
    return tosvg.tosvg(fname, transform=dline)

def main(argv=None):
    import sys

    if argv is None:
        argv = sys.argv
    arg = argv[1:]

    return reproject(arg[0])

if __name__ == '__main__':
    main()
