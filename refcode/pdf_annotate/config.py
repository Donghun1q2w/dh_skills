"""Constants and presets for the pdf_annotate package."""

import os

from pypdf.constants import AnnotationFlag

DEFAULT_FONT = os.environ.get("PDF_ANNOTATE_FONT", r"C:\Windows\Fonts\malgun.ttf")
LABEL_MAX = 50

BORDER_W_PT = 2
LABEL_FONT_PT = 10.0
LABEL_GAP_PT = 4.0
LABEL_BOX_PAD = 2.0
AP_OVERSAMPLE = 4.0
CHIP_BORDER_W = 0.75
CHIP_BORDER_GRAY = 0.313725
ANNOT_AUTHOR = "pdf-annotate"
POPUP_W_PT, POPUP_H_PT = 180.0, 120.0
FREETEXT_FLAGS = AnnotationFlag.PRINT | AnnotationFlag.NO_ROTATE
VALID_ROTATIONS = frozenset({0, 90, 180, 270})

# Domain-neutral color presets. Hex values originate from a report-review
# use case (warning/neutral/critical highlight); any 6-digit hex is accepted.
PRESET_COLORS = {"warning": "FFEB9C", "neutral": "D9D9D9", "critical": "FFC7CE"}
