"""PIL label rasterisation and PDF appearance-stream construction."""

import math

from PIL import Image, ImageDraw, ImageFont
from pypdf.generic import (
    ArrayObject,
    DecodedStreamObject,
    DictionaryObject,
    FloatObject,
    NameObject,
    NumberObject,
)

from .config import (
    AP_OVERSAMPLE,
    CHIP_BORDER_GRAY,
    CHIP_BORDER_W,
    LABEL_BOX_PAD,
    LABEL_FONT_PT,
)


def load_font(font_path):
    """Load the Hangul-capable TTF. Never falls back silently - Korean must render."""
    size = int(round(LABEL_FONT_PT * AP_OVERSAMPLE))
    try:
        return ImageFont.truetype(str(font_path), size)
    except Exception as e:
        raise OSError(
            f"Korean label font not loadable: {font_path!r} ({e}). "
            "Set PDF_ANNOTATE_FONT or install a Hangul-capable TTF."
        ) from e


def render_label_image(label, font, bg_rgb255):
    """Rasterise the label as black glyphs on the annotation colour."""
    bg = tuple(bg_rgb255)
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1), bg))
    left, top, right, bottom = probe.textbbox((0, 0), label, font=font)
    w = max(1, int(math.ceil(right - left)))
    h = max(1, int(math.ceil(bottom - top)))
    img = Image.new("RGB", (w, h), bg)
    ImageDraw.Draw(img).text((-left, -top), label, font=font, fill=(0, 0, 0))
    return img


def chip_size_pt(img):
    """Rasterised label size in PDF points."""
    return (img.size[0] / AP_OVERSAMPLE, img.size[1] / AP_OVERSAMPLE)


def rgb01(rgb255):
    return ArrayObject([FloatObject(c / 255.0) for c in rgb255])


def image_xobject(writer, img):
    """Register the rasterised label as a flate-compressed /Image XObject."""
    st = DecodedStreamObject()
    st.set_data(img.tobytes())
    st[NameObject("/Type")] = NameObject("/XObject")
    st[NameObject("/Subtype")] = NameObject("/Image")
    st[NameObject("/Width")] = NumberObject(img.size[0])
    st[NameObject("/Height")] = NumberObject(img.size[1])
    st[NameObject("/ColorSpace")] = NameObject("/DeviceRGB")
    st[NameObject("/BitsPerComponent")] = NumberObject(8)
    return writer._add_object(st.flate_encode())


def label_ap(writer, img, rgb255, tw, th):
    """Build the label /AP /N Form XObject: filled chip, grey border, label image.

    tw/th are the caller's already-computed chip_size_pt(img) - passed in rather
    than recomputed so the /Rect placement and the /AP /BBox can never diverge.
    """
    img_ref = image_xobject(writer, img)
    w = tw + 2 * LABEL_BOX_PAD
    h = th + 2 * LABEL_BOX_PAD
    r, g, b = (c / 255.0 for c in rgb255)
    half = CHIP_BORDER_W / 2.0
    content = (
        "q\n"
        f"{r:.6f} {g:.6f} {b:.6f} rg\n"
        f"0 0 {w:.4f} {h:.4f} re f\n"
        f"{CHIP_BORDER_GRAY:.6f} {CHIP_BORDER_GRAY:.6f} {CHIP_BORDER_GRAY:.6f} RG\n"
        f"{CHIP_BORDER_W:g} w\n"
        f"{half:.4f} {half:.4f} {w - CHIP_BORDER_W:.4f} {h - CHIP_BORDER_W:.4f} re S\n"
        "Q\n"
        "q\n"
        f"{tw:.4f} 0 0 {th:.4f} {LABEL_BOX_PAD:.4f} {LABEL_BOX_PAD:.4f} cm\n"
        "/Im0 Do\n"
        "Q\n"
    )
    form = DecodedStreamObject()
    # Appearance operators are ASCII-only; Hangul travels via the raster and /Contents.
    form.set_data(content.encode("latin-1"))
    form[NameObject("/Type")] = NameObject("/XObject")
    form[NameObject("/Subtype")] = NameObject("/Form")
    form[NameObject("/FormType")] = NumberObject(1)
    # No /Matrix: with NoRotate the /BBox maps identically onto /Rect at every rotation.
    form[NameObject("/BBox")] = ArrayObject(
        [FloatObject(0), FloatObject(0), FloatObject(w), FloatObject(h)]
    )
    form[NameObject("/Resources")] = DictionaryObject(
        {NameObject("/XObject"): DictionaryObject({NameObject("/Im0"): img_ref})}
    )
    return writer._add_object(form)
