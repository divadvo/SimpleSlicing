# def alt_else():
    # # Case 3a. Two points below layer.
    # if len(punkte_unter_schicht) == 2:
    #     px, py, pz = punkte_uber_schicht[0].x, punkte_uber_schicht[0].y, punkte_uber_schicht[0].z
    #     x1, y1, z1 = punkte_unter_schicht[0].x, punkte_unter_schicht[0].y, punkte_unter_schicht[0].z
    #     x2, y2, z2 = punkte_unter_schicht[1].x, punkte_unter_schicht[1].y, punkte_unter_schicht[1].z
    #
    # # Case 3b. Two points above layer.
    # else:
    #     px, py, pz = punkte_unter_schicht[0].x, punkte_unter_schicht[0].y, punkte_unter_schicht[0].z
    #     x1, y1, z1 = punkte_uber_schicht[0].x, punkte_uber_schicht[0].y, punkte_uber_schicht[0].z
    #     x2, y2, z2 = punkte_uber_schicht[1].x, punkte_uber_schicht[1].y, punkte_uber_schicht[1].z
    #
    # # Generate parametric equations for the two lines and solve for x, y coordinates.
    # t1 = (aktuelle_hohe - pz) / (z1 - pz)
    # t2 = (aktuelle_hohe - pz) / (z2 - pz)
    #
    # # Calculate the intercepts of the lines with the z = z_ind plane.
    # # strecken.append((
    # #     ((x1 - px) * t1 + px, (y1 - py) * t1 + py, aktuelle_hohe),
    # #     ((x2 - px) * t2 + px, (y2 - py) * t2 + py, aktuelle_hohe),
    # # ))




# horiz = []
# h = Hexagon(unit)
# for x_off in np.arange(0, max_x + unit * 1.5, unit * 1.5):
#     horiz += [          ((h.mr[0] + x_off, h.mr[1]), (h.br[0] + x_off, h.br[1])),
#                         ((h.bl[0] + x_off, h.bl[1]), (h.ml[0] + x_off, h.ml[1])),
#                         ((h.ml[0] + x_off, h.ml[1]), (h.tl[0] + x_off, h.tl[1])),
#                         ((h.tl[0] + x_off, h.tl[1]), (h.tr[0] + x_off, h.tr[1])),
#                         ((h.tr[0] + x_off, h.tr[1]), (h.mr[0] + x_off, h.mr[1])),
#                         ((h.mr[0] + x_off, h.mr[1]), (h.mr[0] + x_off + unit / 2, h.mr[1]))
#              ]
#
# vert = []
# for y_off in np.arange(0, max_y + unit * 0.5 * math.sqrt(3), unit * 0.5 * math.sqrt(3)):
#     raw_tessellation = [((x1, y1 + y_off), (x2, y2 + y_off)) for ((x1, y1), (x2, y2)) in horiz]
#
#     strict_in = [seg for seg in raw_tessellation if
#                  0 <= seg[0][0] <= max_x and 0 <= seg[1][0] <= max_x and
#                  0 <= seg[0][1] <= max_y and 0 <= seg[1][1] <= max_y]
#     almost_in = [seg for seg in raw_tessellation if seg not in strict_in and
#                  ((0 <= seg[0][0] <= max_x and 0 <= seg[0][1] <= max_y) or
#                   (0 <= seg[1][0] <= max_x and 0 <= seg[1][1] <= max_y))]
#
#     for ((x1, y1), (x2, y2)) in almost_in:
#         x1, x2 = min(max(0, x1), max_x), min(max(0, x2), max_x)
#         y1, y2 = min(max(0, y1), max_y), min(max(0, y2), max_x)
#         vert.append(((x1, y1), (x2, y2)))
#
#     vert += strict_in






# innen = [strecke for strecke in strecken if
#                  0 <= strecke[0][0] <= max_x and 0 <= strecke[1][0] <= max_x and
#                  0 <= strecke[0][1] <= max_y and 0 <= strecke[1][1] <= max_y]
#
# almost_in = [strecke for strecke in strecken if strecke not in innen and
#                   ((0 <= strecke[0][0] <= max_x and 0 <= strecke[0][1] <= max_y) or
#                    (0 <= strecke[1][0] <= max_x and 0 <= strecke[1][1] <= max_y))]
# beide = []
# beide += innen
#
# for ((x1, y1), (x2, y2)) in almost_in:
#          x1, x2 = min(max(0, x1), max_x), min(max(0, x2), max_x)
#          y1, y2 = min(max(0, y1), max_y), min(max(0, y2), max_x)
#          beide.append(((x1, y1), (x2, y2)))

#beide = innen + almost_in
#print strecken
