"""Pure coordinate transforms and label placement (no pypdf imports)."""

from .config import LABEL_BOX_PAD, LABEL_GAP_PT, LABEL_MAX


def hex_to_rgb(h):
    """'FFFFC7CE'(ARGB)/'FFC7CE'/'#FFC7CE' -> (r, g, b). ValueError on bad input."""
    s = str(h).lstrip("#")
    if len(s) == 8:
        s = s[2:]
    if len(s) != 6:
        raise ValueError(f"bad hex colour: {h!r}")
    return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))


def truncate_label(text, limit=LABEL_MAX):
    collapsed = " ".join(str(text).split())
    if len(collapsed) <= limit:
        return collapsed
    return collapsed[: limit - 1] + "…"


def rects_overlap(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def pad_rect(x, y, w, h, pad=LABEL_BOX_PAD):
    """Bounding rect for a w x h box anchored at (x, y), expanded by pad on every side."""
    return (x - pad, y - pad, x + w + pad, y + h + pad)


def display_to_page_frac(u, v, r):
    """display-space fractional (top-left origin) -> unrotated page fractional.

    r = page /Rotate (0/90/180/270).
    """
    if r == 0:
        return (u, v)
    if r == 90:
        return (v, 1.0 - u)
    if r == 180:
        return (1.0 - u, 1.0 - v)
    if r == 270:
        return (1.0 - v, u)
    raise ValueError(f"unsupported rotation: {r}")


def display_page_size(wp, hp, r):
    """Displayed page size in pt - width/height swap at 90/270."""
    return (hp, wp) if r in (90, 270) else (wp, hp)


def bbox_to_user_rect(bbox, mx0, my0, wp, hp, r):
    """fractional display bbox (l, t, r, b) -> user-space /Rect (pt, bottom-left origin).

    Both corners are transformed, then min/max normalised: at 90/270 the
    minimum corner changes identity.
    """
    l, t, rr, b = bbox
    corners = [display_to_page_frac(l, t, r), display_to_page_frac(rr, b, r)]
    xs = [mx0 + xf * wp for xf, _ in corners]
    ys = [my0 + (1.0 - yf) * hp for _, yf in corners]
    return (min(xs), min(ys), max(xs), max(ys))


def bbox_to_display_box(bbox, ws, hs):
    """fractional bbox -> display-space pt box (top-left origin, y-down). Label placement only."""
    l, t, r, b = bbox
    return (l * ws, t * hs, r * ws, b * hs)


def label_rect_for_norotate(chip_topleft_frac, chip_size_pt, mx0, my0, wp, hp, r):
    """/Rect for a NoRotate FreeText.

    Only the top-left point is transformed - do not min/max normalise two
    corners, or the label unfolds in the opposite direction at 90/270.
    """
    u, v = chip_topleft_frac
    xf, yf = display_to_page_frac(u, v, r)
    px = mx0 + xf * wp
    py = my0 + (1.0 - yf) * hp
    w, h = chip_size_pt
    return (px, py - h, px + w, py)


def place_label(box_disp, tw, th, page_w, page_h, placed, pad=LABEL_GAP_PT):
    """Find a non-overlapping label slot: above, below, then right; else stack downwards.

    Within the candidate and stack (max 40 steps) capacity the placement is
    overlap-free; once exhausted it is best-effort - the last attempted slot is
    returned, which may overlap but is always clamped inside the page.
    """
    left, top, right, bottom = box_disp
    candidates = [
        (left, top - th - pad),
        (left, bottom + pad),
        (right + pad, top),
    ]
    for cx, cy in candidates:
        x = max(0, min(cx, page_w - tw))
        y = max(0, min(cy, page_h - th))
        rect = pad_rect(x, y, tw, th)
        if not any(rects_overlap(rect, p) for p in placed):
            return x, y
    x = max(0, min(left, page_w - tw))
    y = max(0, min(bottom + pad, page_h - th))
    for _ in range(40):
        rect = pad_rect(x, y, tw, th)
        if not any(rects_overlap(rect, p) for p in placed):
            break
        y = min(y + th + pad, page_h - th)
    return x, y
