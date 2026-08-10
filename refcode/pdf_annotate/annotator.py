"""Data model, annotation builders and the annotate_pdf() entry point."""

from __future__ import annotations

import time
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.annotations import FreeText, Popup, Rectangle
from pypdf.constants import AnnotationFlag
from pypdf.generic import DictionaryObject, NameObject, NumberObject, TextStringObject

from .appearance import chip_size_pt, label_ap, load_font, render_label_image, rgb01
from .config import (
    ANNOT_AUTHOR,
    BORDER_W_PT,
    DEFAULT_FONT,
    FREETEXT_FLAGS,
    LABEL_FONT_PT,
    LABEL_GAP_PT,
    POPUP_H_PT,
    POPUP_W_PT,
    VALID_ROTATIONS,
)
from .geometry import (
    bbox_to_display_box,
    bbox_to_user_rect,
    display_page_size,
    hex_to_rgb,
    label_rect_for_norotate,
    pad_rect,
    place_label,
    truncate_label,
)


@dataclass(frozen=True)
class BoxAnnotation:
    """One highlight: a coloured border box plus its popup and label."""

    page: int                                   # 1-based
    bbox: tuple[float, float, float, float]     # display-space fractional (l, t, r, b), top-left origin
    label: str                                  # Hangul allowed; truncated past 50 chars
    color: str = "FFC7CE"                       # hex RGB (ARGB / leading '#' accepted)
    subject: str = ""                           # /Subj (omitted when empty)

    def __post_init__(self):
        if not isinstance(self.page, int) or isinstance(self.page, bool) or self.page < 1:
            raise ValueError(f"page must be int >= 1: {self.page!r}")
        bb = tuple(float(v) for v in self.bbox)
        if len(bb) != 4:
            raise ValueError(f"bbox must have 4 values: {self.bbox!r}")
        l, t, r, b = bb
        if not (0.0 <= l < r <= 1.0 and 0.0 <= t < b <= 1.0):
            raise ValueError(f"bbox must satisfy 0<=l<r<=1, 0<=t<b<=1: {bb}")
        object.__setattr__(self, "bbox", bb)
        if not str(self.label).strip():
            raise ValueError("label must be non-empty")
        object.__setattr__(self, "_rgb", hex_to_rgb(self.color))


@dataclass(frozen=True)
class AnnotateResult:
    out_path: Path
    drawn: int          # one Square+Popup+FreeText bundle == 1
    page_count: int
    skipped_oob: int


def _pdf_now():
    now = time.localtime()
    offset = -(time.altzone if now.tm_isdst else time.timezone)
    sign = "+" if offset >= 0 else "-"
    offset = abs(offset)
    stamp = time.strftime("%Y%m%d%H%M%S", now)
    return TextStringObject(f"D:{stamp}{sign}{offset // 3600:02d}'{(offset % 3600) // 60:02d}'")


def _set_common_meta(annot, nm, subject, stamp):
    """Shared /T, /Subj, /NM, /M, /CreationDate fields for Square and FreeText."""
    annot[NameObject("/T")] = TextStringObject(ANNOT_AUTHOR)
    if subject:
        annot[NameObject("/Subj")] = TextStringObject(subject)
    annot[NameObject("/NM")] = TextStringObject(nm)
    annot[NameObject("/M")] = stamp
    annot[NameObject("/CreationDate")] = stamp


def _build_square(rect_pt, rgb255, label, subject, nm, stamp):
    sq = Rectangle(rect=rect_pt, interior_color=None)  # no /IC -> border only, no fill
    sq[NameObject("/C")] = rgb01(rgb255)
    sq[NameObject("/BS")] = DictionaryObject(
        {NameObject("/W"): NumberObject(BORDER_W_PT), NameObject("/S"): NameObject("/S")}
    )
    sq[NameObject("/F")] = NumberObject(int(AnnotationFlag.PRINT))
    sq[NameObject("/Contents")] = TextStringObject(label)
    _set_common_meta(sq, nm, subject, stamp)
    return sq


def _popup_rect(sq_rect, mx0, my0, wp, hp):
    """Popup box to the right of the square, clamped inside the CropBox."""
    x0 = min(max(sq_rect[2], mx0), mx0 + wp - POPUP_W_PT)
    y1 = min(max(sq_rect[3], my0 + POPUP_H_PT), my0 + hp)
    return (x0, y1 - POPUP_H_PT, x0 + POPUP_W_PT, y1)


def _build_popup(square, rect_pt, nm, stamp):
    pop = Popup(rect=rect_pt, parent=square, open=False)
    pop[NameObject("/NM")] = TextStringObject(f"{nm}-popup")
    pop[NameObject("/M")] = stamp
    return pop


def _build_label_annot(writer, rect_pt, rgb255, label, subject, img, tw, th, nm, stamp):
    # border_color must not be passed at all: a truthy value corrupts /DA and
    # None injects /BS with W=0.
    ft = FreeText(
        text=label,
        rect=rect_pt,
        font_size=f"{LABEL_FONT_PT:g}pt",
        background_color="{:02x}{:02x}{:02x}".format(*rgb255),
    )
    # pypdf 6.6.2 writes a colour operator into /DA; replace it with a real text state.
    ft[NameObject("/DA")] = TextStringObject(f"/Helv {LABEL_FONT_PT:g} Tf 0 g")
    ft[NameObject("/F")] = NumberObject(int(FREETEXT_FLAGS))
    ft[NameObject("/AP")] = DictionaryObject({NameObject("/N"): label_ap(writer, img, rgb255, tw, th)})
    _set_common_meta(ft, f"{nm}-label", subject, stamp)
    return ft


def annotate_pdf(pdf_path, annotations, out_pdf, font_path=DEFAULT_FONT, dedupe=True) -> AnnotateResult:
    """Attach a Square + Popup + Korean FreeText label bundle per annotation."""
    pdf_path, out_pdf = Path(pdf_path), Path(out_pdf)
    if pdf_path.resolve() == out_pdf.resolve():
        raise ValueError("out_pdf must differ from pdf_path (in-place overwrite is not allowed)")
    reader = PdfReader(str(pdf_path))
    if reader.is_encrypted:
        raise ValueError(f"Encrypted PDF not supported: {pdf_path}")
    n_pages = len(reader.pages)

    by_page: dict[int, list[BoxAnnotation]] = defaultdict(list)
    for ann in annotations:
        by_page[ann.page].append(ann)
    oob = sum(len(v) for p, v in by_page.items() if not 1 <= p <= n_pages)
    has_valid = any(1 <= p <= n_pages for p in by_page)

    font = load_font(font_path) if has_valid else None
    writer = PdfWriter(clone_from=reader)  # page bytes cloned verbatim; only /Annots grows
    stamp = _pdf_now()
    drawn = 0
    for p in sorted(by_page):
        if not 1 <= p <= n_pages:
            continue
        page = reader.pages[p - 1]
        box = page.cropbox
        mx0, my0 = float(box.left), float(box.bottom)
        wp, hp = float(box.width), float(box.height)
        r = int(page.get("/Rotate") or 0) % 360
        if r not in VALID_ROTATIONS:
            r = 0
        ws, hs = display_page_size(wp, hp, r)
        placed, seen, seq = [], set(), 0
        for ann in by_page[p]:
            rgb = ann._rgb  # validated + parsed once in BoxAnnotation.__post_init__
            label = truncate_label(ann.label)
            rect = bbox_to_user_rect(ann.bbox, mx0, my0, wp, hp, r)
            key = (tuple(round(v, 2) for v in rect), ann.color, label)
            if dedupe and key in seen:
                continue
            seen.add(key)
            seq += 1
            nm = f"pdf-annotate-p{p:02d}-{seq:02d}"
            sq = _build_square(rect, rgb, label, ann.subject, nm, stamp)
            writer.add_annotation(p - 1, sq)
            pop = _build_popup(sq, _popup_rect(rect, mx0, my0, wp, hp), nm, stamp)
            writer.add_annotation(p - 1, pop)
            sq[NameObject("/Popup")] = pop.indirect_reference
            img = render_label_image(label, font, rgb)
            tw, th = chip_size_pt(img)
            box_disp = bbox_to_display_box(ann.bbox, ws, hs)
            lx, ly = place_label(box_disp, tw, th, ws, hs, placed, pad=LABEL_GAP_PT)
            chip = pad_rect(lx, ly, tw, th)
            placed.append(chip)
            label_rect = label_rect_for_norotate(
                (chip[0] / ws, chip[1] / hs),
                (chip[2] - chip[0], chip[3] - chip[1]),
                mx0, my0, wp, hp, r,
            )
            ft = _build_label_annot(writer, label_rect, rgb, label, ann.subject, img, tw, th, nm, stamp)
            writer.add_annotation(p - 1, ft)
            drawn += 1
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    with open(out_pdf, "wb") as fh:
        writer.write(fh)
    return AnnotateResult(out_pdf, drawn, n_pages, oob)
