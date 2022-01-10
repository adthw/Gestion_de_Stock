#!/usr/bin/env python
# encoding: utf-8
# Généré par Mocodo 2.3.9 le Mon, 10 Jan 2022 11:25:36

from __future__ import division
from math import hypot

import time, codecs

(width,height) = (692,380)
cx = {
    u"Produits"  :  203,
    u"Commander" :  377,
    u"Factures"  :  539,
    u"Produire"  :  203,
    u"Dater"     :  377,
    u"Facturer"  :  539,
    u"Usines"    :   61,
    u"Calendrier":  203,
    u"Clients"   :  377,
    u"Etre"      :  539,
    u"Types"     :  640,
}
cy = {
    u"Produits"  :   73,
    u"Commander" :   73,
    u"Factures"  :   73,
    u"Produire"  :  190,
    u"Dater"     :  190,
    u"Facturer"  :  190,
    u"Usines"    :  307,
    u"Calendrier":  307,
    u"Clients"   :  307,
    u"Etre"      :  307,
    u"Types"     :  307,
}
shift = {
    u"Commander,Produits":    0,
    u"Commander,Factures":    0,
    u"Produire,Usines"   :    0,
    u"Produire,Produits" :    0,
    u"Dater,Factures"    :    0,
    u"Dater,Calendrier"  :    0,
    u"Facturer,Factures" :    0,
    u"Facturer,Clients"  :    0,
    u"Etre,Clients"      :    0,
    u"Etre,Types"        :    0,
}
colors = {
    u"annotation_color"                : '#060707',
    u"annotation_text_color"           : '#E2EED0',
    u"association_attribute_text_color": '#607734',
    u"association_cartouche_color"     : '#b2bba4',
    u"association_cartouche_text_color": '#27360c',
    u"association_color"               : '#ccd6ba',
    u"association_stroke_color"        : '#85956b',
    u"background_color"                : 'none',
    u"card_text_color"                 : '#726f83',
    u"entity_attribute_text_color"     : '#3e3c42',
    u"entity_cartouche_color"          : '#97b8ff',
    u"entity_cartouche_text_color"     : '#131114',
    u"entity_color"                    : '#c0d4ff',
    u"entity_stroke_color"             : '#578dff',
    u"label_text_color"                : '#726f83',
    u"leg_stroke_color"                : '#726f83',
    u"transparent_color"               : 'none',
}
card_max_width = 19
card_max_height = 14
card_margin = 5
arrow_width = 12
arrow_half_height = 6
arrow_axis = 8
card_baseline = 3

def cmp(x, y):
    return (x > y) - (x < y)

def offset(x, y):
    return (x + card_margin, y - card_baseline - card_margin)

def line_intersection(ex, ey, w, h, ax, ay):
    if ax == ex:
        return (ax, ey + cmp(ay, ey) * h)
    if ay == ey:
        return (ex + cmp(ax, ex) * w, ay)
    x = ex + cmp(ax, ex) * w
    y = ey + (ay-ey) * (x-ex) / (ax-ex)
    if abs(y-ey) > h:
        y = ey + cmp(ay, ey) * h
        x = ex + (ax-ex) * (y-ey) / (ay-ey)
    return (x, y)

def straight_leg_factory(ex, ey, ew, eh, ax, ay, aw, ah, cw, ch):
    
    def card_pos(twist, shift):
        compare = (lambda x1_y1: x1_y1[0] < x1_y1[1]) if twist else (lambda x1_y1: x1_y1[0] <= x1_y1[1])
        diagonal = hypot(ax-ex, ay-ey)
        correction = card_margin * 1.4142 * (1 - abs(abs(ax-ex) - abs(ay-ey)) / diagonal) - shift
        (xg, yg) = line_intersection(ex, ey, ew, eh + ch, ax, ay)
        (xb, yb) = line_intersection(ex, ey, ew + cw, eh, ax, ay)
        if compare((xg, xb)):
            if compare((xg, ex)):
                if compare((yb, ey)):
                    return (xb - correction, yb)
                return (xb - correction, yb + ch)
            if compare((yb, ey)):
                return (xg, yg + ch - correction)
            return (xg, yg + correction)
        if compare((xb, ex)):
            if compare((yb, ey)):
                return (xg - cw, yg + ch - correction)
            return (xg - cw, yg + correction)
        if compare((yb, ey)):
            return (xb - cw + correction, yb)
        return (xb - cw + correction, yb + ch)
    
    def arrow_pos(direction, ratio):
        (x0, y0) = line_intersection(ex, ey, ew, eh, ax, ay)
        (x1, y1) = line_intersection(ax, ay, aw, ah, ex, ey)
        if direction == "<":
            (x0, y0, x1, y1) = (x1, y1, x0, y0)
        (x, y) = (ratio * x0 + (1 - ratio) * x1, ratio * y0 + (1 - ratio) * y1)
        return (x, y, x1 - x0, y0 - y1)
    
    straight_leg_factory.card_pos = card_pos
    straight_leg_factory.arrow_pos = arrow_pos
    return straight_leg_factory


def curved_leg_factory(ex, ey, ew, eh, ax, ay, aw, ah, cw, ch, spin):
    
    def bisection(predicate):
        (a, b) = (0, 1)
        while abs(b - a) > 0.0001:
            m = (a + b) / 2
            if predicate(bezier(m)):
                a = m
            else:
                b = m
        return m
    
    def intersection(left, top, right, bottom):
       (x, y) = bezier(bisection(lambda p: left <= p[0] <= right and top <= p[1] <= bottom))
       return (int(round(x)), int(round(y)))
    
    def card_pos(shift):
        diagonal = hypot(ax-ex, ay-ey)
        correction = card_margin * 1.4142 * (1 - abs(abs(ax-ex) - abs(ay-ey)) / diagonal)
        (top, bot) = (ey - eh, ey + eh)
        (TOP, BOT) = (top - ch, bot + ch)
        (lef, rig) = (ex - ew, ex + ew)
        (LEF, RIG) = (lef - cw, rig + cw)
        (xr, yr) = intersection(LEF, TOP, RIG, BOT)
        (xg, yg) = intersection(lef, TOP, rig, BOT)
        (xb, yb) = intersection(LEF, top, RIG, bot)
        if spin > 0:
            if (yr == BOT and xr <= rig) or (xr == LEF and yr >= bot):
                return (max(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y >= bot) - correction + shift, bot + ch)
            if (xr == RIG and yr >= top) or yr == BOT:
                return (rig, min(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x >= rig) + correction + shift)
            if (yr == TOP and xr >= lef) or xr == RIG:
                return (min(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y <= top) + correction + shift - cw, TOP + ch)
            return (LEF, max(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x <= lef) - correction + shift + ch)
        if (yr == BOT and xr >= lef) or (xr == RIG and yr >= bot):
            return (min(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y >= bot) + correction + shift - cw, bot + ch)
        if xr == RIG or (yr == TOP and xr >= rig):
            return (rig, max(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x >= rig) - correction + shift + ch)
        if yr == TOP or (xr == LEF and yr <= top):
            return (max(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y <= top) - correction + shift, TOP + ch)
        return (LEF, min(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x <= lef) + correction + shift)
    
    def arrow_pos(direction, ratio):
        t0 = bisection(lambda p: abs(p[0] - ax) > aw or abs(p[1] - ay) > ah)
        t3 = bisection(lambda p: abs(p[0] - ex) < ew and abs(p[1] - ey) < eh)
        if direction == "<":
            (t0, t3) = (t3, t0)
        tc = t0 + (t3 - t0) * ratio
        (xc, yc) = bezier(tc)
        (x, y) = derivate(tc)
        if direction == "<":
            (x, y) = (-x, -y)
        return (xc, yc, x, -y)
    
    diagonal = hypot(ax - ex, ay - ey)
    (x, y) = line_intersection(ex, ey, ew + cw / 2, eh + ch / 2, ax, ay)
    k = (cw *  abs((ay - ey) / diagonal) + ch * abs((ax - ex) / diagonal))
    (x, y) = (x - spin * k * (ay - ey) / diagonal, y + spin * k * (ax - ex) / diagonal)
    (hx, hy) = (2 * x - (ex + ax) / 2, 2 * y - (ey + ay) / 2)
    (x1, y1) = (ex + (hx - ex) * 2 / 3, ey + (hy - ey) * 2 / 3)
    (x2, y2) = (ax + (hx - ax) * 2 / 3, ay + (hy - ay) * 2 / 3)
    (kax, kay) = (ex - 2 * hx + ax, ey - 2 * hy + ay)
    (kbx, kby) = (2 * hx - 2 * ex, 2 * hy - 2 * ey)
    bezier = lambda t: (kax*t*t + kbx*t + ex, kay*t*t + kby*t + ey)
    derivate = lambda t: (2*kax*t + kbx, 2*kay*t + kby)
    
    curved_leg_factory.points = (ex, ey, x1, y1, x2, y2, ax, ay)
    curved_leg_factory.card_pos = card_pos
    curved_leg_factory.arrow_pos = arrow_pos
    return curved_leg_factory


def upper_round_rect(x, y, w, h, r):
    return " ".join([str(x) for x in ["M", x + w - r, y, "a", r, r, 90, 0, 1, r, r, "V", y + h, "h", -w, "V", y + r, "a", r, r, 90, 0, 1, r, -r]])

def lower_round_rect(x, y, w, h, r):
    return " ".join([str(x) for x in ["M", x + w, y, "v", h - r, "a", r, r, 90, 0, 1, -r, r, "H", x + r, "a", r, r, 90, 0, 1, -r, -r, "V", y, "H", w]])

def arrow(x, y, a, b):
    c = hypot(a, b)
    (cos, sin) = (a / c, b / c)
    return " ".join([str(x) for x in [ "M", x, y, "L", x + arrow_width * cos - arrow_half_height * sin, y - arrow_half_height * cos - arrow_width * sin, "L", x + arrow_axis * cos, y - arrow_axis * sin, "L", x + arrow_width * cos + arrow_half_height * sin, y + arrow_half_height * cos - arrow_width * sin, "Z"]])

def safe_print_for_PHP(s):
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("utf8"))


lines = '<?xml version="1.0" standalone="no"?>\n<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"\n"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'
lines += '\n\n<svg width="%s" height="%s" view_box="0 0 %s %s"\nxmlns="http://www.w3.org/2000/svg"\nxmlns:link="http://www.w3.org/1999/xlink">' % (width,height,width,height)
lines += u'\\n\\n<desc>Généré par Mocodo 2.3.9 le %s</desc>' % time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
lines += '\n\n<rect id="frame" x="0" y="0" width="%s" height="%s" fill="%s" stroke="none" stroke-width="0"/>' % (width,height,colors['background_color'] if colors['background_color'] else "none")

lines += u"""\n\n<!-- Association Commander -->"""
(x,y) = (cx[u"Commander"],cy[u"Commander"])
(ex,ey) = (cx[u"Produits"],cy[u"Produits"])
leg=straight_leg_factory(ex,ey,71,64,x,y,74,37,19+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"Commander,Produits"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Futura" font-size="11">1,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"Factures"],cy[u"Factures"])
leg=straight_leg_factory(ex,ey,59,38,x,y,74,37,19+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(True,shift[u"Commander,Factures"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Futura" font-size="11">1,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
lines += u"""\n<g id="association-Commander">""" % {}
path = upper_round_rect(-74+x,-37+y,148,28,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_cartouche_color'], 'stroke_color': colors['association_cartouche_color']}
path = lower_round_rect(-74+x,-9.0+y,148,46,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_color'], 'stroke_color': colors['association_color']}
lines += u"""\n	<rect x="%(x)s" y="%(y)s" width="148" height="74" fill="%(color)s" rx="14" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -74+x, 'y': -37+y, 'color': colors['transparent_color'], 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x0': -74+x, 'y0': -9+y, 'x1': 74+x, 'y1': -9+y, 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Copperplate" font-size="18">Commander</text>""" % {'x': -53+x, 'y': -15.7+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">id_commander</text>""" % {'x': -67+x, 'y': 9.1+y, 'text_color': colors['association_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">quantite_commander</text>""" % {'x': -67+x, 'y': 26.1+y, 'text_color': colors['association_attribute_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Association Produire -->"""
(x,y) = (cx[u"Produire"],cy[u"Produire"])
(ex,ey) = (cx[u"Usines"],cy[u"Usines"])
leg=straight_leg_factory(ex,ey,52,55,x,y,50,29,19+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"Produire,Usines"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Futura" font-size="11">0,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"Produits"],cy[u"Produits"])
leg=straight_leg_factory(ex,ey,71,64,x,y,50,29,19+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"Produire,Produits"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Futura" font-size="11">1,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
lines += u"""\n<g id="association-Produire">""" % {}
path = upper_round_rect(-50+x,-29+y,100,28,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_cartouche_color'], 'stroke_color': colors['association_cartouche_color']}
path = lower_round_rect(-50+x,-1.0+y,100,30,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_color'], 'stroke_color': colors['association_color']}
lines += u"""\n	<rect x="%(x)s" y="%(y)s" width="100" height="58" fill="%(color)s" rx="14" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -50+x, 'y': -29+y, 'color': colors['transparent_color'], 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x0': -50+x, 'y0': -1+y, 'x1': 50+x, 'y1': -1+y, 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Copperplate" font-size="18">Produire</text>""" % {'x': -43+x, 'y': -7.7+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Association Dater -->"""
(x,y) = (cx[u"Dater"],cy[u"Dater"])
(ex,ey) = (cx[u"Factures"],cy[u"Factures"])
leg=straight_leg_factory(ex,ey,59,38,x,y,34,29,18+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"Dater,Factures"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Futura" font-size="11">1,1</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"Calendrier"],cy[u"Calendrier"])
leg=straight_leg_factory(ex,ey,61,30,x,y,34,29,19+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"Dater,Calendrier"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Futura" font-size="11">0,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
lines += u"""\n<g id="association-Dater">""" % {}
path = upper_round_rect(-34+x,-29+y,68,28,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_cartouche_color'], 'stroke_color': colors['association_cartouche_color']}
path = lower_round_rect(-34+x,-1.0+y,68,30,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_color'], 'stroke_color': colors['association_color']}
lines += u"""\n	<rect x="%(x)s" y="%(y)s" width="68" height="58" fill="%(color)s" rx="14" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -34+x, 'y': -29+y, 'color': colors['transparent_color'], 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x0': -34+x, 'y0': -1+y, 'x1': 34+x, 'y1': -1+y, 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Copperplate" font-size="18">Dater</text>""" % {'x': -27+x, 'y': -7.7+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Association Facturer -->"""
(x,y) = (cx[u"Facturer"],cy[u"Facturer"])
(ex,ey) = (cx[u"Factures"],cy[u"Factures"])
leg=straight_leg_factory(ex,ey,59,38,x,y,50,29,18+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"Facturer,Factures"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Futura" font-size="11">1,1</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"Clients"],cy[u"Clients"])
leg=straight_leg_factory(ex,ey,53,64,x,y,50,29,19+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"Facturer,Clients"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Futura" font-size="11">1,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
lines += u"""\n<g id="association-Facturer">""" % {}
path = upper_round_rect(-50+x,-29+y,100,28,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_cartouche_color'], 'stroke_color': colors['association_cartouche_color']}
path = lower_round_rect(-50+x,-1.0+y,100,30,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_color'], 'stroke_color': colors['association_color']}
lines += u"""\n	<rect x="%(x)s" y="%(y)s" width="100" height="58" fill="%(color)s" rx="14" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -50+x, 'y': -29+y, 'color': colors['transparent_color'], 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x0': -50+x, 'y0': -1+y, 'x1': 50+x, 'y1': -1+y, 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Copperplate" font-size="18">Facturer</text>""" % {'x': -43+x, 'y': -7.7+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Association Etre -->"""
(x,y) = (cx[u"Etre"],cy[u"Etre"])
(ex,ey) = (cx[u"Clients"],cy[u"Clients"])
leg=straight_leg_factory(ex,ey,53,64,x,y,29,29,18+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"Etre,Clients"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Futura" font-size="11">1,1</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"Types"],cy[u"Types"])
leg=straight_leg_factory(ex,ey,43,38,x,y,29,29,19+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"Etre,Types"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Futura" font-size="11">1,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
lines += u"""\n<g id="association-Etre">""" % {}
path = upper_round_rect(-29+x,-29+y,58,28,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_cartouche_color'], 'stroke_color': colors['association_cartouche_color']}
path = lower_round_rect(-29+x,-1.0+y,58,30,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_color'], 'stroke_color': colors['association_color']}
lines += u"""\n	<rect x="%(x)s" y="%(y)s" width="58" height="58" fill="%(color)s" rx="14" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -29+x, 'y': -29+y, 'color': colors['transparent_color'], 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x0': -29+x, 'y0': -1+y, 'x1': 29+x, 'y1': -1+y, 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Copperplate" font-size="18">Etre</text>""" % {'x': -22+x, 'y': -7.7+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity Produits -->"""
(x,y) = (cx[u"Produits"],cy[u"Produits"])
lines += u"""\n<g id="entity-Produits">""" % {}
lines += u"""\n	<g id="frame-Produits">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="142" height="30" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -71+x, 'y': -64+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="142" height="98" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -71+x, 'y': -34.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="142" height="128" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -71+x, 'y': -64+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x0': -71+x, 'y0': -34+y, 'x1': 71+x, 'y1': -34+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Copperplate" font-size="18">Produits</text>""" % {'x': -42+x, 'y': -42.7+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">id_produit</text>""" % {'x': -63+x, 'y': -16.9+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -63+x, 'y0': -14+y, 'x1': 4+x, 'y1': -14+y, 'stroke_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">ref_produit</text>""" % {'x': -63+x, 'y': 0.1+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">nom_produit</text>""" % {'x': -63+x, 'y': 17.1+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">description_produit</text>""" % {'x': -63+x, 'y': 34.0+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">statut_produit</text>""" % {'x': -63+x, 'y': 51.0+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity Factures -->"""
(x,y) = (cx[u"Factures"],cy[u"Factures"])
lines += u"""\n<g id="entity-Factures">""" % {}
lines += u"""\n	<g id="frame-Factures">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="118" height="30" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -59+x, 'y': -38+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="118" height="46" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -59+x, 'y': -8.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="118" height="76" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -59+x, 'y': -38+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x0': -59+x, 'y0': -8+y, 'x1': 59+x, 'y1': -8+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Copperplate" font-size="18">Factures</text>""" % {'x': -42+x, 'y': -16.7+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">id_facture</text>""" % {'x': -51+x, 'y': 9.1+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -51+x, 'y0': 12+y, 'x1': 13+x, 'y1': 12+y, 'stroke_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">numero_facture</text>""" % {'x': -51+x, 'y': 26.1+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity Usines -->"""
(x,y) = (cx[u"Usines"],cy[u"Usines"])
lines += u"""\n<g id="entity-Usines">""" % {}
lines += u"""\n	<g id="frame-Usines">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="104" height="30" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -52+x, 'y': -55+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="104" height="80" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -52+x, 'y': -25.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="104" height="110" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -52+x, 'y': -55+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x0': -52+x, 'y0': -25+y, 'x1': 52+x, 'y1': -25+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Copperplate" font-size="18">Usines</text>""" % {'x': -31+x, 'y': -33.7+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">id_usine</text>""" % {'x': -44+x, 'y': -7.9+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -44+x, 'y0': -5+y, 'x1': 9+x, 'y1': -5+y, 'stroke_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">nom_usine</text>""" % {'x': -44+x, 'y': 9.1+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">adresse_usine</text>""" % {'x': -44+x, 'y': 26.1+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">ville_usine</text>""" % {'x': -44+x, 'y': 43.0+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity Calendrier -->"""
(x,y) = (cx[u"Calendrier"],cy[u"Calendrier"])
lines += u"""\n<g id="entity-Calendrier">""" % {}
lines += u"""\n	<g id="frame-Calendrier">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="122" height="30" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -61+x, 'y': -30+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="122" height="30" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -61+x, 'y': 0.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="122" height="60" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -61+x, 'y': -30+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x0': -61+x, 'y0': 0+y, 'x1': 61+x, 'y1': 0+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Copperplate" font-size="18">Calendrier</text>""" % {'x': -53+x, 'y': -8.7+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">date_calendrier</text>""" % {'x': -53+x, 'y': 17.1+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -53+x, 'y0': 20+y, 'x1': 45+x, 'y1': 20+y, 'stroke_color': colors['entity_attribute_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity Clients -->"""
(x,y) = (cx[u"Clients"],cy[u"Clients"])
lines += u"""\n<g id="entity-Clients">""" % {}
lines += u"""\n	<g id="frame-Clients">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="106" height="30" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -53+x, 'y': -64+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="106" height="98" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -53+x, 'y': -34.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="106" height="128" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -53+x, 'y': -64+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x0': -53+x, 'y0': -34+y, 'x1': 53+x, 'y1': -34+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Copperplate" font-size="18">Clients</text>""" % {'x': -36+x, 'y': -42.7+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">id_client</text>""" % {'x': -45+x, 'y': -16.9+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -45+x, 'y0': -14+y, 'x1': 9+x, 'y1': -14+y, 'stroke_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">nom_client</text>""" % {'x': -45+x, 'y': 0.1+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">adresse_client</text>""" % {'x': -45+x, 'y': 17.1+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">ville_client</text>""" % {'x': -45+x, 'y': 34.0+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">pays_client</text>""" % {'x': -45+x, 'y': 51.0+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity Types -->"""
(x,y) = (cx[u"Types"],cy[u"Types"])
lines += u"""\n<g id="entity-Types">""" % {}
lines += u"""\n	<g id="frame-Types">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="86" height="30" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -43+x, 'y': -38+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="86" height="46" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -43+x, 'y': -8.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="86" height="76" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -43+x, 'y': -38+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x0': -43+x, 'y0': -8+y, 'x1': 43+x, 'y1': -8+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Copperplate" font-size="18">Types</text>""" % {'x': -26+x, 'y': -16.7+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">id_types</text>""" % {'x': -35+x, 'y': 9.1+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -35+x, 'y0': 12+y, 'x1': 18+x, 'y1': 12+y, 'stroke_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">nom_types</text>""" % {'x': -35+x, 'y': 26.1+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n</g>""" % {}
lines += u'\n</svg>'

with codecs.open(r"sandbox.svg", "w", "utf8") as f:
    f.write(lines)
safe_print_for_PHP(u'Fichier de sortie "sandbox.svg" généré avec succès.')